from django.contrib.auth.models import User, Group
from cognitive_tests import models
from rest_framework import serializers


class ModuleSerializer(serializers.ModelSerializer):
    tests = serializers.HyperlinkedIdentityField(view_name='api:module-tests', read_only=True)
    surveys = serializers.HyperlinkedIdentityField(view_name='api:module-surveys', read_only=True)

    class Meta:
        model = models.Module
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    testresults = serializers.HyperlinkedIdentityField(view_name='api:participant-testresults', read_only=True)
    surveyresults = serializers.HyperlinkedIdentityField(view_name='api:participant-surveyresults', read_only=True)
    gender = serializers.ChoiceField(models.Participant.GENDER_CHOICES)

    class Meta:
        model = models.Participant
        exclude = ('session', )

    def create(self, validated_data):
        request = self.context['request']

        if not request.session.session_key:
            request.session.create()

        validated_data['session'] = request.session.session_key
        return models.Participant.objects.create(**validated_data)


class TestResultValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestResultValue
        fields = '__all__'


class TestMarkSerializer(serializers.ModelSerializer):
    values = serializers.HyperlinkedIdentityField(view_name='api:testmark-values', read_only=True)
    stats = serializers.HyperlinkedIdentityField(view_name='api:testmark-stats', read_only=True)

    class Meta:
        model = models.TestMark
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    results = serializers.HyperlinkedIdentityField(view_name='api:test-results', read_only=True)
    marks = serializers.HyperlinkedIdentityField(view_name='api:test-marks', read_only=True)
    resource_uri = serializers.HyperlinkedIdentityField(view_name='api:test-detail', read_only=True)

    class Meta:
        model = models.Test
        #extra_kwargs = {'url': {'view_name': 'api:test-detail'}}
        exclude = ('module', 'processor', )


class TestResultFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestResultFile
        fields = '__all__'


class TestResultTextDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestResultTextData
        fields = '__all__'


class TestResultSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    files = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='api:testresultfile-detail')
    text_data = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='api:testresulttextdata-detail')

    # Values are embedded
    values = TestResultValueSerializer(many=True, read_only=True)

    class Meta:
        model = models.TestResult
        fields = '__all__'
        #extra_kwargs = {'url': {'view_name': 'api:testresult-detail'}}

    def create(self, validated_data):
        return models.TestResult.objects.create(participant=validated_data['participant'], test=validated_data['test'])


class SurveySerializer(serializers.ModelSerializer):
    results = serializers.HyperlinkedIdentityField(view_name='api:survey-results', read_only=True)
    marks = serializers.HyperlinkedIdentityField(view_name='api:survey-marks', read_only=True)
    tests = serializers.HyperlinkedIdentityField(view_name='api:survey-tests', read_only=True)

    class Meta:
        exclude = ('module', 'processor', )
        model = models.Survey


class SurveyMarkSerializer(serializers.ModelSerializer):
    values = serializers.HyperlinkedIdentityField(view_name='api:surveymark-values', read_only=True)
    stats = serializers.HyperlinkedIdentityField(view_name='api:surveymark-stats', read_only=True)

    class Meta:
        model = models.SurveyMark
        fields = '__all__'


class SurveyResultValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyResultValue
        fields = '__all__'


class SurveyResultSerializer(serializers.ModelSerializer):
    values = SurveyResultValueSerializer(many=True, read_only=True)

    class Meta:
        model = models.SurveyResult
        fields = '__all__'
