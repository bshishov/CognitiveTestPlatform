from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'name', 'age', 'gender', 'email', 'allow_info_usage')


class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'name', 'description', 'enabled', 'created')


class WebTestSerializer(serializers.HyperlinkedModelSerializer):
    test = TestSerializer()

    class Meta:
        model = WebTest
        fields = ('id', 'test', 'record_audio', 'record_video', 'record_mouse', 'created')


class TestFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestFile


class TestTextDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestTextData


class TestResultSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    files = TestFileSerializer(read_only=True, many=True)  # TODO: create TEST FILES SERIALIZER
    text_data = TestTextDataSerializer(read_only=True, many=True)  # TODO: create TEST DATA SERIALIZER

    class Meta:
        model = TestResult
        fields = ('id', 'participant', 'test', 'created', 'text_data', 'files',)

    def create(self, validated_data):
        return TestResult.objects.create(participant=validated_data['participant'], test=validated_data['test'])
        return self._test_result

    def save_data(self, data):
        text_data = TestTextData.objects.create(test_result=self.get_object(), data=data['events'])
        pass

    def save_files(self, files):
        pass



