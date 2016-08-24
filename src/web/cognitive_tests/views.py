from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .cognitive_test import CognitiveTest
from .models import Participant


PARTICIPANT_SESSION_KEY = 'participant_id'


def index(request):
    return render(request, 'index.html')


@csrf_protect
def start(request):
    participant = __get_participant(request)
    return render(request, 'start.html', {'participant': participant})

    if request.method == 'POST':
        participant = Participant()
        participant.name = request.POST['name']
        participant.age = request.POST['age']
        participant.gender = request.POST['gender'] == 1
        participant.allow_info_usage = request.POST['allow'] == 'on'
        request.session.create()
        participant.session = request.session.session_key
        participant.save()

        request.session[PARTICIPANT_SESSION_KEY] = request.session.session_key
        return redirect(check)


def list(request):
    return render(request, 'list.html', {'tests': CognitiveTest.all.values()})


def first(request):
    participant = __get_participant(request)
    if not participant:
        return redirect(start)

    return redirect(test, next(iter(CognitiveTest.all.values())).name)


def check(request):
    participant = __get_participant(request)
    if not participant:
        return redirect(start)

    return render(request, 'check.html', {
        'participant': participant,
    })


def result(request):
    participant = __get_participant(request)
    if not participant:
        return redirect(start)

    return render(request, 'results.html')


@csrf_exempt
def test(request, test_name):
    participant = __get_participant(request)
    if not participant:
        return redirect(start)

    if request.method == "GET":
        return render(request, 'test.html', {
            'test': CognitiveTest.get(test_name),
            'participant': participant
        })
    elif request.method == "POST":
        request.QueryDict
        print('test passed')

    redirect(test)


def __get_participant(request):
    if PARTICIPANT_SESSION_KEY not in request.session:
        return None
    try:
        return Participant.objects.get(session=request.session.session_key)
    except:
        del request.session[PARTICIPANT_SESSION_KEY]
        return None
