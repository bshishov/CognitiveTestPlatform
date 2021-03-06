from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cognitive_tests import models
from cognitive_tests import utils
from cognitive_tests.api import permissions
from cognitive_tests.api import serializers

from django.core.handlers.wsgi import WSGIRequest
import numpy as np


class FilteredModelViewSet(viewsets.ModelViewSet):
    """
    The actions provided by the ModelViewSet class are:
        .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy().
    """
    NESTED_LIST_MAPPING = {
        'get': 'list',
        'post': 'create'
    }
    filter_kwargs = None  # required by ModelViewSet

    def __init__(self, queryset=None, filter_kwargs=None, **kwargs):
        super(FilteredModelViewSet, self).__init__(**kwargs)
        if queryset:
            self.queryset = queryset
        elif filter_kwargs:
            self.queryset = self.queryset.filter(**filter_kwargs)
            self.filter_kwargs = filter_kwargs

    @classmethod
    def as_filtered_view(cls, mapping=NESTED_LIST_MAPPING, queryset=None, **kwargs):
        return cls.as_view(mapping, queryset=queryset, filter_kwargs=kwargs)

    @classmethod
    def proceed_filtered(cls, request, mapping=NESTED_LIST_MAPPING, queryset=None, **kwargs):
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            """
            For some reason we can't directly redirect POST-like methods to cls.as_view because of
            csrf_excempt and other stuff so request body become touched.
            We need to construct the request handler ourselves.
            """
            viewset = cls(queryset=queryset, filter_kwargs=kwargs)
            viewset.request = request
            if str.lower(request.method) not in mapping:
                raise RuntimeError('Method %s can\'t be proceeded' % request.method)
            action = getattr(viewset, mapping[str.lower(request.method)])
            return action(request)

        # Backward compatibility hack: since Django in newer versions asserts that
        # the request is actually a django http request and not a DRF one
        # Thus we get internal WSGI request from DRF to exec the view
        request: WSGIRequest = request._request
        return cls.as_view(mapping, queryset=queryset, filter_kwargs=kwargs)(request)


class ParticipantFiltered(viewsets.ModelViewSet):
    def __check(self, request, *args, **kwargs):
        if not request.user or not request.user.is_staff:
            participant = models.Participant.from_request(request)
            self.queryset = self.queryset.filter(participant=participant)

    def list(self, request, *args, **kwargs):
        self.__check(request, *args, **kwargs)
        return super(ParticipantFiltered, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.__check(request, *args, **kwargs)
        return super(ParticipantFiltered, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.__check(request, *args, **kwargs)
        return super(ParticipantFiltered, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.__check(request, *args, **kwargs)
        return super(ParticipantFiltered, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.__check(request, *args, **kwargs)
        return super(ParticipantFiltered, self).partial_update(request, *args, **kwargs)


class TestResultValueViewSet(FilteredModelViewSet):
    queryset = models.TestResultValue.objects.all()
    serializer_class = serializers.TestResultValueSerializer
    permission_classes = [permissions.IsParticipantOrStaff, ]


class MarkViewSetMixin(viewsets.ModelViewSet):
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        mark = self.get_object()
        values = mark.values.all()
        raw = [val.value for val in values]
        if mark.data_type == models.Mark.NUMERIC and len(raw) > 0:
            hist_values, hist_edges = np.histogram(raw, bins=10)
            return Response({'values': raw,
                             'min': min(raw),
                             'max': max(raw),
                             'mean': np.mean(raw),
                             'len': len(raw),
                             'histogram': {
                                 'values': hist_values,
                                 'edges': hist_edges
                             },
                             'std': np.std(raw)})
        return Response({'values': raw, 'len': len(raw)})

    @action(detail=True, methods=['get'])
    def percentile(self, request, pk=None):
        mark = self.get_object()
        score = request.GET.get('score', None)
        if score is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            score = float(score)
        except Exception as err:
            return Response({'message': 'Score should be numeric'}, status=status.HTTP_400_BAD_REQUEST)
        values = [val.value for val in mark.values.all()]
        if mark.data_type != models.Mark.NUMERIC or len(values) == 0:
            return Response({'message': 'Score should be provided'}, status=status.HTTP_400_BAD_REQUEST)

        if mark.cmp == mark.CMP_HIGHER_IS_BETTER:
            percentile = len([i for i in values if i <= score]) / float(len(values)) * 100
            return Response({'percentile': percentile, 'cmp': mark.cmp})
        elif mark.cmp == mark.CMP_LOWER_IS_BETTER:
            percentile = len([i for i in values if i >= score]) / float(len(values)) * 100
            return Response({'percentile': percentile, 'cmp': mark.cmp})

        return Response({'message': 'No comparison for this mark'}, status=status.HTTP_400_BAD_REQUEST)


class TestMarkViewSet(MarkViewSetMixin, FilteredModelViewSet):
    queryset = models.TestMark.objects.all()
    serializer_class = serializers.TestMarkSerializer
    permission_classes = [permissions.IsStaffOrReadOnly, ]

    @action(detail=True, methods=['get'])
    def values(self, request, pk=None):
        return TestResultValueViewSet.proceed_filtered(request, mark=self.get_object())


class TestResultViewSet(ParticipantFiltered, FilteredModelViewSet):
    queryset = models.TestResult.objects.all()
    serializer_class = serializers.TestResultSerializer
    permission_classes = [permissions.IsParticipantOrStaff, ]

    def create(self, request, *args, **kwargs):
        participant = models.Participant.from_request(request)
        survey_result_pk = request.POST.get('survey_result', None)
        survey_result = None
        if survey_result_pk:
            survey_result = models.SurveyResult.objects.get(pk=survey_result_pk)
        if not participant:
            return Response({'detail': 'No participant'}, status=status.HTTP_400_BAD_REQUEST)

        result = models.TestResult.objects.create(participant=participant,
                                                  survey_result=survey_result,
                                                  **self.filter_kwargs)

        result_serializer = serializers.TestResultSerializer(result, partial=True, data={},
                                                                 context={'request': request})
        if result_serializer.is_valid():
            result = result_serializer.save()

            for file_arg in request.FILES:
                for raw_file in request.FILES.getlist(file_arg):
                    file_serializer = serializers.TestResultFileSerializer(models.TestResultFile(result=result),
                                                                               data={'name': raw_file.name,
                                                                                     'file': raw_file},
                                                                               partial=True)
                    if file_serializer.is_valid():
                        file_serializer.save()
                    else:
                        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            for arg in request.data:
                # TODO: TO VALIDATE
                if arg in models.TestResultTextData.RESTRICTED_NAMES or arg in result_serializer.fields or arg in request.FILES:
                    continue
                text_data_serializer = serializers.TestResultTextDataSerializer(
                    models.TestResultTextData(result=result),
                    data={'name': arg, 'data': request.data[arg]},
                    partial=True)
                if text_data_serializer.is_valid():
                    text_data_serializer.save()
                else:
                    return Response(text_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            result.process()
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestViewSet(FilteredModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = serializers.TestSerializer
    permission_classes = [permissions.IsParticipantOrStaff, ]

    @action(detail=True, methods=['get', 'post', 'options'])
    def results(self, request, pk=None):
        return TestResultViewSet.proceed_filtered(request, test=self.get_object())

    @action(detail=True, methods=['get', 'options'])
    def marks(self, request, pk=None):
        return TestMarkViewSet.proceed_filtered(request, test=self.get_object())


class TestResultTextDataViewSet(viewsets.ModelViewSet):
    queryset = models.TestResultTextData.objects.all()
    serializer_class = serializers.TestResultTextDataSerializer
    permission_classes = [permissions.IsStaff, ]


class TestResultFileViewSet(viewsets.ModelViewSet):
    queryset = models.TestResultFile.objects.all()
    serializer_class = serializers.TestResultFileSerializer
    permission_classes = [permissions.IsStaff, ]


class SurveyResultValueViewSet(FilteredModelViewSet):
    queryset = models.SurveyResultValue.objects.all()
    serializer_class = serializers.SurveyResultValueSerializer
    permission_classes = [permissions.IsParticipantOrStaff, ]


class SurveyResultViewSet(ParticipantFiltered, FilteredModelViewSet):
    queryset = models.SurveyResult.objects.all()
    serializer_class = serializers.SurveyResultSerializer
    permission_classes = [permissions.IsParticipantOrStaff, ]


class SurveyMarkViewSet(MarkViewSetMixin, FilteredModelViewSet):
    queryset = models.SurveyMark.objects.all()
    serializer_class = serializers.SurveyMarkSerializer
    permission_classes = [permissions.IsStaffOrReadOnly, ]

    @action(detail=True, methods=['get', 'options'])
    def values(self, request, pk=None):
        return SurveyResultValueViewSet.proceed_filtered(request, mark=self.get_object())


class SurveyViewSet(FilteredModelViewSet):
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveySerializer
    permission_classes = [permissions.IsStaffOrReadOnly, ]

    @action(detail=True, methods=['get', 'options'])
    def results(self, request, pk=None):
        return SurveyResultViewSet.proceed_filtered(request, survey=self.get_object())

    @action(detail=True, methods=['get', 'options'])
    def tests(self, request, pk=None):
        return TestViewSet.proceed_filtered(request, queryset=self.get_object().tests)

    @action(detail=True, methods=['get', 'options'])
    def marks(self, request, pk=None):
        return SurveyMarkViewSet.proceed_filtered(request, survey=self.get_object())


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = models.Module.objects.all()
    serializer_class = serializers.ModuleSerializer
    permission_classes = [permissions.IsStaff, ]

    @action(detail=True, methods=['get', 'options'])
    def tests(self, request, pk=None):
        return TestViewSet.proceed_filtered(request, module=self.get_object())

    @action(detail=True, methods=['get', 'options'])
    def surveys(self, request, pk=None):
        return SurveyViewSet.proceed_filtered(request, module=self.get_object())


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = models.Participant.objects.all()
    serializer_class = serializers.ParticipantSerializer
    permission_classes = [permissions.IsParticipantOrStaff, ]

    @action(detail=True, methods=['get', 'options'])
    def testresults(self, request, pk=None):
        return TestResultViewSet.proceed_filtered(request, participant=self.get_object())

    @action(detail=True, methods=['get', 'options'])
    def surveyresults(self, request, pk=None):
        return SurveyResultViewSet.proceed_filtered(request, participant=self.get_object())

    @action(detail=False, methods=['get', 'post', 'delete'])
    def current(self, request):
        participant = models.Participant.from_request(request)
        if request.method == 'GET':
            if not participant:
                return Response({'detail': 'you must sign up as a participant using POST'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = serializers.ParticipantSerializer(participant, context={'request': request})
            return Response(serializer.data)

        if request.method == 'POST':
            if participant:
                return Response({'detail': 'participant already set'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = serializers.ParticipantSerializer(data=request.data, context={'request': request,
                                                                                       'assign': True})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            if not participant:
                return Response({'detail': 'you must sign up as a participant using POST'},
                                status=status.HTTP_400_BAD_REQUEST)
            participant.unassign_from_request(request)
            return Response({'detail': 'participant unset successfully'}, status=status.HTTP_202_ACCEPTED)
