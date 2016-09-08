from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, detail_route, list_route, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import authentication, permissions
from .api_serializers import *
from .api_permissions import *
from .models import *


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'tests': reverse('test-list', request=request, format=format),
    })


@api_view(['GET'])
def test_list(request, format=None):
    return Response(TestSerializer(Test.objects.all(), many=True).data)

def get_test(pk):
    try:
        return Test.objects.get(pk=pk)
    except Test.DoesNotExist:
        raise Http404


@api_view(['GET'])
def test_detail(request, pk, format=None):
    return Response(TestSerializer(get_test(pk)).data)


@api_view(['GET', 'POST'])
@permission_classes([IsParticipantOrReadOnly, ])
def test_results(request, test_pk, format=None):
    test = get_test(test_pk)

    if request.method == 'GET':
        results = TestResult.objects.filter(test=test)
        serializer = TestResultSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        participant = get_participant(request)
        if not participant:
            return Response({'detail': 'No participant'}, status=status.HTTP_400_BAD_REQUEST)

        result = TestResult(test=test, participant=participant)
        result.save()
        for file_arg in request.FILES:
            for raw_file in request.FILES.getlist(file_arg):
                test_file = TestFile(test_result=result, name=raw_file.name, file=raw_file)
                test_file.save()

        return Response(TestResultSerializer(result).data, status=status.HTTP_201_CREATED)

        serializer = TestResultSerializer(data=request.data, )
        if serializer.is_valid():
            serializer.save()
            serializer.save_data(data=request.data)
            serializer.save_files(files=request.FILES)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)