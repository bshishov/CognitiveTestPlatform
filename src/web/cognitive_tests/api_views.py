from django.http import Http404, HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, detail_route, list_route, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAdminUser
from rest_framework import authentication, permissions
from .api_serializers import *
from .api_permissions import *
from .models import *


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'tests': reverse('test-list', request=request, format=format),
        'participant': reverse('session-participant', request=request, format=format),
    })


@api_view(['GET'])
def test_list(request, format=None):
    return Response(TestSerializer(Test.objects.filter(active=True), many=True, context={'request': request}).data)


def get_test(pk):
    try:
        test = Test.objects.get(pk=pk)
        if not test.active:
            return Http404
        return test
    except Test.DoesNotExist:
        raise Http404


@api_view(['GET'])
def test_detail(request, pk, format=None):
    return Response(TestSerializer(get_test(pk), context={'request': request}).data)


@api_view(['GET', 'POST'])
@permission_classes([IsParticipantOrReadOnly, ])
def test_results(request, pk, format=None):
    test = get_test(pk)

    if request.method == 'GET':
        results = TestResult.objects.filter(test=test)
        serializer = TestResultSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        participant = get_participant(request)
        survey_result_pk = request.POST.get('survey_result', None)
        survey_result = None
        if survey_result_pk:
            survey_result = SurveyResult.objects.get(pk=survey_result_pk)
        if not participant:
            return Response({'detail': 'No participant'}, status=status.HTTP_400_BAD_REQUEST)
        result_serializer = TestResultSerializer(TestResult(test=test, participant=participant,
                                                            survey_result=survey_result), partial=True, data={})
        if result_serializer.is_valid():
            result = result_serializer.save()

            for file_arg in request.FILES:
                for raw_file in request.FILES.getlist(file_arg):
                    file_serializer = TestFileSerializer(TestResultFile(result=result),
                                                         data={'name': raw_file.name, 'file': raw_file},
                                                         partial=True)
                    if file_serializer.is_valid():
                        file_serializer.save()
                    else:
                        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            for arg in request.data:
                #TODO: TO VALIDATE
                if arg in TestResultTextData.RESTRICTED_NAMES or arg in result_serializer.fields or arg in request.FILES:
                    continue
                text_data_serializer = TestTextDataSerializer(TestResultTextData(result=result),
                                                              data={'name': arg, 'data': request.data[arg]},
                                                              partial=True)
                if text_data_serializer.is_valid():
                    text_data_serializer.save()
                else:
                    return Response(text_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            result.process()
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def test_marks(request, pk, format=None):
    return Response(TestMarkSerializer(get_test(pk).marks, many=True, context={'request': request}).data)


@api_view(['GET', 'POST', 'DELETE'])
def session_participant(request):
    participant = get_participant(request)
    if request.method == 'GET':
        if not participant:
            return Response({'detail': 'you must sign up as a participant using POST'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ParticipantSerializer(participant, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        if participant:
            return Response({'detail': 'participant already set'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ParticipantSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            request.session[Participant.PARTICIPANT_SESSION_KEY] = request.session.session_key
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if not participant:
            return Response({'detail': 'you must sign up as a participant using POST'},
                            status=status.HTTP_400_BAD_REQUEST)
        del request.session[Participant.PARTICIPANT_SESSION_KEY]
        return Response({'detail': 'participant unset successfully'}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAdminUser, ])
def test_result_text_data_detail(request, pk):
    return Response(TestTextDataSerializer(TestResultTextData.objects.get(pk=pk), context={'request': request}).data)


@api_view(['GET'])
@permission_classes([IsAdminUser, ])
def test_result_file_detail(request, pk):
    return Response(TestFileSerializer(TestResultFile.objects.get(pk=pk), context={'request': request}).data)
