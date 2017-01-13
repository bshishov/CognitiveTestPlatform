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

        if not request.session.session_key:
            request.session.create()

        validated_data['session'] = request.session.session_key
        return Participant.objects.create(**validated_data)


class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'name', 'description', 'active', 'created')


class TestFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultFile
        exclude = ('id', 'result',)


class TestTextDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultTextData
        exclude = ('id', 'result',)


class TestResultSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    files = TestFileSerializer(read_only=True, many=True)
    text_data = TestTextDataSerializer(read_only=True, many=True)

    class Meta:
        model = TestResult
        fields = ('id', 'participant', 'test', 'created', 'text_data', 'files',)

    def create(self, validated_data):
        return TestResult.objects.create(participant=validated_data['participant'], test=validated_data['test'])




