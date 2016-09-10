from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class ParticipantSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(Participant.GENDER_CHOICES)

    class Meta:
        model = Participant
        fields = ('name', 'age', 'gender', 'email', 'allow_info_usage')

    def create(self, validated_data):
        request = self.context['request']
        request.session.create()

        validated_data['session'] = request.session.session_key
        return Participant.objects.create(**validated_data)


class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'name', 'description', 'active', 'created')


class WebTestSerializer(serializers.HyperlinkedModelSerializer):
    test = TestSerializer()

    class Meta:
        model = WebTest
        fields = ('id', 'test', 'record_audio', 'record_video', 'record_mouse', 'created')


class TestFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestFile
        exclude = ('id','test_result',)


class TestTextDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestTextData
        exclude = ('id', 'test_result',)


class TestResultSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    files = TestFileSerializer(read_only=True, many=True)  # TODO: create TEST FILES SERIALIZER
    text_data = TestTextDataSerializer(read_only=True, many=True)  # TODO: create TEST DATA SERIALIZER

    class Meta:
        model = TestResult
        fields = ('id', 'participant', 'test', 'created', 'text_data', 'files',)

    def create(self, validated_data):
        return TestResult.objects.create(participant=validated_data['participant'], test=validated_data['test'])

    def save_data(self, data):
        text_data = TestTextData.objects.create(test_result=self.get_object(), data=data['events'])
        pass

    def save_files(self, files):
        pass



