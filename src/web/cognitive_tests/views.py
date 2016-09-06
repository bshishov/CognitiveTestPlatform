from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from .models import *
from .utils import participant_required, get_participant


PARTICIPANT_SESSION_KEY = 'participant_id'


@require_GET
def index(request):
    return render(request, 'index.html')


@csrf_protect
@require_http_methods(['GET','POST'])
def start(request):
    participant = get_participant(request)
    if request.method == 'GET':
        return render(request, 'start.html', {'participant': participant})

    if request.method == 'POST':
        participant = Participant()
        participant.name = request.POST['name']
        participant.age = request.POST['age']
        participant.gender = request.POST['gender'] == 1
        participant.allow_info_usage = request.POST.get('allow', None) == 'on'
        request.session.create()
        participant.session = request.session.session_key
        participant.save()

        request.session[PARTICIPANT_SESSION_KEY] = request.session.session_key
        print(participant)
        return redirect(check)


@require_GET
def list(request):
    return render(request, 'list.html', {'tests': Test.objects.all()})


@require_GET
@participant_required(redirect_to=start)
def first(request, participant):
    return redirect(web_test, Test.objects.all()[0].id)


@require_GET
@participant_required(redirect_to=start)
def check(request, participant):
    return render(request, 'check.html', {
        'participant': participant,
    })


@require_GET
@participant_required(redirect_to=start)
def result(request, participant):
    return render(request, 'results.html')


@require_GET
@participant_required(redirect_to=start)
def web_test(request, participant, test_id):
    return render(request, 'test.html', {
        'test': WebTest.objects.get(id=test_id),
        'participant': participant
    })
