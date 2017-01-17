from functools import wraps

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import viewsets
from rest_framework import views
from rest_framework import permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from . import models
from . import api_serializers
from . import api_permissions
from . import utils


class NestedModelViewSet(viewsets.ModelViewSet):
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
        super(NestedModelViewSet, self).__init__(**kwargs)
        if queryset:
            self.queryset = queryset
        elif filter_kwargs:
            self.queryset = self.queryset.filter(**filter_kwargs)
            self.filter_kwargs = filter_kwargs

    @classmethod
    def as_nested_view(cls, queryset=None, **kwargs):
        return cls.as_view(cls.NESTED_LIST_MAPPING, queryset=queryset, filter_kwargs=kwargs)


class ParticipantFiltered(viewsets.ModelViewSet):
    def __check(self, request, *args, **kwargs):
        if not request.user or not request.user.is_staff:
            participant = utils.get_participant(request)
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


class TestResultValueViewSet(NestedModelViewSet):
    queryset = models.TestResultValue.objects.all()
    serializer_class = api_serializers.TestResultValueSerializer
    permission_classes = [api_permissions.IsParticipantOrStaff, ]


class TestMarkViewSet(NestedModelViewSet):
    queryset = models.TestMark.objects.all()
    serializer_class = api_serializers.TestMarkSerializer
    permission_classes = [api_permissions.IsStaffOrReadOnly, ]

    @detail_route(methods=['get', 'options'])
    def values(self, request, pk=None):
        return TestResultValueViewSet.as_nested_view(mark=self.get_object())(request)


class TestResultViewSet(ParticipantFiltered, NestedModelViewSet):
    queryset = models.TestResult.objects.all()
    serializer_class = api_serializers.TestResultSerializer
    permission_classes = [api_permissions.IsParticipantOrStaff, ]

    def create(self, request, *args, **kwargs):
        print(self.queryset)
        participant = utils.get_participant(request)
        survey_result_pk = request.POST.get('survey_result', None)
        survey_result = None
        if survey_result_pk:
            survey_result = models.SurveyResult.objects.get(pk=survey_result_pk)
        if not participant:
            return Response({'detail': 'No participant'}, status=status.HTTP_400_BAD_REQUEST)

        result = models.TestResult.objects.create(participant=participant,
                                                  survey_result=survey_result,
                                                  **self.filter_kwargs)

        result_serializer = api_serializers.TestResultSerializer(result, partial=True, data={},
                                                                 context={'request': request})
        if result_serializer.is_valid():
            result = result_serializer.save()

            for file_arg in request.FILES:
                for raw_file in request.FILES.getlist(file_arg):
                    file_serializer = api_serializers.TestResultFileSerializer(models.TestResultFile(result=result),
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
                text_data_serializer = api_serializers.TestResultTextDataSerializer(
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


class TestViewSet(NestedModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = api_serializers.TestSerializer
    permission_classes = [api_permissions.IsParticipantOrStaff, ]

    @detail_route(methods=['get', 'post', 'options'])
    def results(self, request, pk=None):
        test = self.get_object()
        return TestResultViewSet.as_nested_view(test=test)(request)

    @detail_route(methods=['get', 'options'])
    def marks(self, request, pk=None):
        return TestMarkViewSet.as_nested_view(test=self.get_object())(request)


class TestResultTextDataViewSet(viewsets.ModelViewSet):
    queryset = models.TestResultTextData.objects.all()
    serializer_class = api_serializers.TestResultTextDataSerializer
    permission_classes = [api_permissions.IsStaff, ]


class TestResultFileViewSet(viewsets.ModelViewSet):
    queryset = models.TestResultFile.objects.all()
    serializer_class = api_serializers.TestResultFileSerializer
    permission_classes = [api_permissions.IsStaff, ]


class SurveyResultValueViewSet(NestedModelViewSet):
    queryset = models.SurveyResultValue.objects.all()
    serializer_class = api_serializers.SurveyResultValueSerializer
    permission_classes = [api_permissions.IsParticipantOrStaff, ]


class SurveyResultViewSet(ParticipantFiltered, NestedModelViewSet):
    queryset = models.SurveyResult.objects.all()
    serializer_class = api_serializers.SurveyResultSerializer
    permission_classes = [api_permissions.IsParticipantOrStaff, ]


class SurveyMarkViewSet(NestedModelViewSet):
    queryset = models.SurveyMark.objects.all()
    serializer_class = api_serializers.SurveyMarkSerializer
    permission_classes = [api_permissions.IsStaffOrReadOnly, ]

    @detail_route(methods=['get', 'options'])
    def values(self, request, pk=None):
        return SurveyResultValueViewSet.as_nested_view(mark=self.get_object())(request)


class SurveyViewSet(NestedModelViewSet):
    queryset = models.Survey.objects.all()
    serializer_class = api_serializers.SurveySerializer
    permission_classes = [api_permissions.IsStaffOrReadOnly, ]

    @detail_route(methods=['get', 'options'])
    def results(self, request, pk=None):
        return SurveyResultViewSet.as_nested_view(survey=self.get_object())(request)

    @detail_route(methods=['get', 'options'])
    def tests(self, request, pk=None):
        return TestViewSet.as_nested_view(queryset=self.get_object().tests)(request)

    @detail_route(methods=['get', 'options'])
    def marks(self, request, pk=None):
        return SurveyMarkViewSet.as_nested_view(survey=self.get_object())(request)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = models.Module.objects.all()
    serializer_class = api_serializers.ModuleSerializer
    permission_classes = [api_permissions.IsStaff, ]

    @detail_route(methods=['get', 'options'])
    def tests(self, request, pk=None):
        return TestViewSet.as_nested_view(module=self.get_object())(request)

    @detail_route(methods=['get', 'options'])
    def surveys(self, request, pk=None):
        return SurveyViewSet.as_nested_view(module=self.get_object())(request)


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = models.Participant.objects.all()
    serializer_class = api_serializers.ParticipantSerializer
    permission_classes = [api_permissions.IsParticipantOrStaff, ]

    @detail_route(methods=['get', 'options'])
    def testresults(self, request, pk=None):
        return TestResultViewSet.as_nested_view(participant=self.get_object())(request)

    @detail_route(methods=['get', 'options'])
    def surveyresults(self, request, pk=None):
        return SurveyResultViewSet.as_nested_view(participant=self.get_object())(request)

    @list_route(methods=['get', 'post', 'delete'])
    def current(self, request):
        participant = utils.get_participant(request)
        if request.method == 'GET':
            if not participant:
                return Response({'detail': 'you must sign up as a participant using POST'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = api_serializers.ParticipantSerializer(participant, context={'request': request})
            return Response(serializer.data)

        if request.method == 'POST':
            if participant:
                return Response({'detail': 'participant already set'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = api_serializers.ParticipantSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                request.session[models.Participant.PARTICIPANT_SESSION_KEY] = request.session.session_key
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            if not participant:
                return Response({'detail': 'you must sign up as a participant using POST'},
                                status=status.HTTP_400_BAD_REQUEST)
            del request.session[models.Participant.PARTICIPANT_SESSION_KEY]
            return Response({'detail': 'participant unset successfully'}, status=status.HTTP_202_ACCEPTED)
