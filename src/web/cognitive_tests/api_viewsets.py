from rest_framework import viewsets, status, renderers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from .api_serializers import *
from .models import Participant


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all().order_by('-created')
    serializer_class = ParticipantSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all().order_by('-created')
    serializer_class = TestSerializer

    @detail_route(methods=['GET', 'POST'])
    def results(self, request, pk=None, *args, **kwargs):
        if request.method == 'GET':
            results = TestResult.objects.filter(pk=pk)
            serializer = TestResultSerializer(results, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = TestResultSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                serializer.save_data(data=request.data)
                serializer.save_files(files=request.FILES)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    def active(self, request):
        tests = Test.objects.filter(enabled=True)
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)


class WebTestViewSet(viewsets.ModelViewSet):
    queryset = WebTest.objects.all().order_by('-created')
    serializer_class = WebTestSerializer


class TestResultsViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all().order_by('-created')
    serializer_class = TestResultSerializer
