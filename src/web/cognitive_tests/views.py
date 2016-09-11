from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from django.core import urlresolvers

from .api_serializers import ParticipantSerializer
from .models import *
from .utils import participant_required, get_participant, redirect_with_args, reverse_with_args


@require_GET
def index(request):
    return render(request, 'index.html', {
        'participant': get_participant(request),
    })


@csrf_protect
@require_http_methods(['GET', 'POST'])
def participant_new(request):
    participant = get_participant(request)
    if request.method == 'GET':
        return render(request, 'participant_new.html', {'participant': participant})

    if request.method == 'POST':
        serializer = ParticipantSerializer(data={
            'name': request.POST['name'],
            'age': request.POST['age'],
            'gender': request.POST['gender'] == 1,
            'allow_info_usage': request.POST.get('allow', None) == 'on',
        }, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            request.session[Participant.PARTICIPANT_SESSION_KEY] = request.session.session_key
            return redirect(web_group_list)

        return render(request, 'participant_new.html', {
            'participant': participant,
            'errors': serializer.errors
        })


@require_GET
@participant_required(redirect_to=participant_new)
def web_check(request, participant):
    return render(request, 'web_check.html', {
        'participant': participant,
        'next': request.GET.get('next', ''),
    })


@require_GET
def web_group_list(request):
    return render(request, 'web_group_list.html', {
        'groups': WebTestGroup.objects.all(),
        'participant': get_participant(request),
    })


@require_GET
@participant_required(redirect_to=participant_new)
def web_group_test(request, participant, group_pk, order):
    test = get_object_or_404(WebTest, group__pk=group_pk, order=order)
    next_test = WebTest.objects.filter(order=int(order) + 1).first()

    if next_test:
        next_url = urlresolvers.reverse(web_group_test, kwargs={
                                      'group_pk': group_pk,
                                      'order': order + 1
                                  })
    else:
        next_url = urlresolvers.reverse(web_group_results, kwargs={'group_pk': group_pk})
    return render(request, 'web_test.html', {
        'test': test,
        'participant': participant,
        'next': next_url
    })


@require_GET
@participant_required(redirect_to=participant_new)
def web_group_start(request, participant, group_pk):
    return render(request, 'web_group_start.html', {
        'participant': participant,
        'group': get_object_or_404(WebTestGroup, pk=group_pk),
        'next': reverse_with_args(web_check, {'next':
                                urlresolvers.reverse(web_group_test, kwargs={
                                      'group_pk': group_pk,
                                      'order': 1
                                  })
                                }),
    })


@require_http_methods(['GET', 'POST'])
@participant_required(redirect_to=participant_new)
def web_group_results(request, participant, group_pk):
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        participant.email = request.POST.get('email', '')
        participant.save()

    return render(request, 'web_group_results.html', {
        'participant': participant
    })


@require_GET
def web_test_list(request):
    return render(request, 'web_test_list.html', {
        'tests': WebTest.objects.filter(test__active=True),
        'participant': get_participant(request),
    })


@require_GET
@participant_required(redirect_to=participant_new)
def web_test(request, participant, test_pk):
    test = get_object_or_404(WebTest, pk=test_pk)
    return render(request, 'web_test.html', {
        'test': test,
        'participant': participant
    })
