from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class ParticipantSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(Participant.GENDER_CHOICES)

    class Meta:
        model = Participant
        fields = ('id', 'name', 'age', 'gender', 'email', 'allow_info_usage')

    def create(self, validated_data):
        request = self.context['request']

        if not request.session.session_key:
            request.session.create()

        validated_data['session'] = request.session.session_key
        return Participant.objects.create(**validated_data)


class TestResultValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultValue


class TestMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestMark


class TestSerializer(serializers.HyperlinkedModelSerializer):
    results = serializers.HyperlinkedIdentityField(view_name='test-results', read_only=True)
    marks = serializers.HyperlinkedIdentityField(view_name='test-marks', read_only=True)
    #marks = TestMarkSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'url', 'created', 'updated', 'key', 'name',
                  'description', 'active', 'created', 'results', 'marks',)
        #exclude = ('module',)


class TestFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultFile


class TestTextDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultTextData


class TestResultValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultValue


class TestResultSerializer(serializers.HyperlinkedModelSerializer):
    participant = ParticipantSerializer(read_only=True)

    # Files and Text Data are hyperlinked
    #files = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='testresultfile-detail')
    #text_data = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='testresulttextdata-detail')

    # Values are embedded
    values = TestResultValueSerializer(many=True, read_only=True)

    class Meta:
        model = TestResult
        fields = ('id', 'participant', 'test', 'created', 'text_data', 'files', 'values')

    def create(self, validated_data):
        return TestResult.objects.create(participant=validated_data['participant'], test=validated_data['test'])




