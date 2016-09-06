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


class TestResultSerializer(serializers.HyperlinkedModelSerializer):
    participant = ParticipantSerializer()
    test = TestSerializer()

    class Meta:
        model = TestResult
        fields = ('id', 'participant', 'test', 'created')

