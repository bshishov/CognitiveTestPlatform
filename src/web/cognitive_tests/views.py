import mimetypes

from django.core import urlresolvers
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_http_methods

from cognitive_tests.api.serializers import ParticipantSerializer
from .models import *
from .utils import participant_required, redirect_with_args


def context_processor(request):
    return {
        'participant': Participant.from_request(request),
        'surveys': Survey.objects.active(),
    }


@require_GET
def index(request):
    return render(request, 'index.html', {'tests': Test.objects.active_web()})


@csrf_protect
@require_http_methods(['GET', 'POST'])
def participant_new(request):
    if request.method == 'GET':
        return render(request, 'participant_new.html', {})

    if request.method == 'POST':
        serializer = ParticipantSerializer(data={
            'name': request.POST['name'],
            'age': request.POST['age'],
            'gender': request.POST['gender'],
            'allow_info_usage': request.POST.get('allow', None) == 'on'
        }, context={'request': request, 'assign': True})

        if serializer.is_valid():
            serializer.save()
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
            else:
                return redirect(surveys)

        return render(request, 'participant_new.html', {'errors': serializer.errors})


@require_GET
def surveys(request):
    return render(request, 'surveys.html', {'tests': Test.objects.active_web()})


@require_GET
def survey_view(request, survey_pk):
    survey = get_object_or_404(Survey, pk=survey_pk)
    participant = Participant.from_request(request)
    return render(request, 'survey_view.html', {
        'survey': survey,
        'participant': participant,
        'result': survey.get_result_for(participant),
        'results': survey.get_all_results_for(participant),
    })


@require_GET
@participant_required(redirect_to=participant_new, next_view_name='survey-start')
def survey_start(request, participant, survey_pk):
    survey = get_object_or_404(Survey, pk=survey_pk)
    audio = survey.web_record_audio
    video = survey.web_record_video

    # delete incomplete results
    SurveyResult.objects.filter(survey=survey, participant=participant, is_completed=False).delete()

    result = SurveyResult(survey=survey, participant=participant)
    result.save()

    first_test = result.incomplete_tests.first()

    if audio or video:
        next_url = urlresolvers.reverse(survey_test, kwargs={'survey_result_pk': result.pk, 'test_pk': first_test.pk})
        return redirect_with_args(survey_check, {'next': next_url,},
                                    kwargs={'survey_pk': survey_pk})

    return redirect(survey_test, survey_result_pk=result.pk, test_pk=first_test.pk)


@require_GET
@participant_required(redirect_to=participant_new, next_view_name='survey')
def survey_continue(request, participant, survey_result_pk):
    try:
        result = SurveyResult.objects.get(pk=survey_result_pk, participant=participant)
    except ObjectDoesNotExist:
        raise Http404

    if result.is_completed:
        logger.error('Trying to continue a completed survey')
        return redirect(survey_results, survey_result_pk=survey_result_pk)

    next_test = result.incomplete_tests.first()
    if next_test is None:
        logger.error('Trying to continue a completed survey')
        return redirect(survey_results, survey_result_pk=survey_result_pk)

    return redirect(survey_test, survey_result_pk=survey_result_pk, test_pk=next_test.pk)


@require_GET
@participant_required(redirect_to=participant_new, next_view_name='survey')
def survey_check(request, participant, survey_pk):
    return render(request, 'survey_check.html', {
        'survey': get_object_or_404(Survey, pk=survey_pk),
        'next': request.GET.get('next', ''),
    })


@require_GET
@participant_required(redirect_to=participant_new, next_view_name='survey')
def survey_test(request, participant, survey_result_pk, test_pk):
    try:
        result = SurveyResult.objects.get(pk=survey_result_pk, participant=participant)
        survey = result.survey
        test = survey.tests.get(pk=test_pk)
    except ObjectDoesNotExist:
        raise Http404

    next_test = result.incomplete_tests.exclude(pk=test_pk).first()
    test_result = result.test_results.filter(test=test).first()

    if next_test:
        next_url = urlresolvers.reverse(survey_test, kwargs={
                                      'survey_result_pk': survey_result_pk,
                                      'test_pk': next_test.pk
                                  })
    else:
        next_url = urlresolvers.reverse(survey_end, kwargs={'survey_result_pk': survey_result_pk})
    return render(request, 'test_run.html', {
        'test': test,
        'next': next_url,
        'result': result,
        'test_result': test_result,
        'survey': survey,
    })


@require_GET
@participant_required(redirect_to=participant_new, next_view_name='survey')
def survey_end(request, participant, survey_result_pk):
    result = get_object_or_404(SurveyResult, pk=survey_result_pk, participant=participant)  # type: SurveyResult
    if len(result.incomplete_tests) == 0 and not result.is_completed:
        result.is_completed = True
        result.save()
        result.process()
    return redirect(survey_results, survey_result_pk)


@require_http_methods(['GET', 'POST'])
@participant_required(redirect_to=participant_new, next_view_name='survey')
def survey_results(request, participant, survey_result_pk):
    result = get_object_or_404(SurveyResult, pk=survey_result_pk, participant=participant)
    return render(request, 'survey_results.html', {'survey': result.survey,
                                                   'result': result})


@require_GET
def test_view(request, test_pk):
    test = get_object_or_404(Test, pk=test_pk)
    participant = Participant.from_request(request)
    return render(request, 'test_view.html', {
        'test': test,
        'participant': participant,
        'result': test.get_result_for(participant),
        'results': test.get_all_results_for(participant),
    })


@require_GET
@participant_required(redirect_to=participant_new, next_view_name='test-start')
def test_start(request, participant, test_pk):
    test = get_object_or_404(Test, pk=test_pk)
    audio = test.web_record_audio
    video = test.web_record_video

    if audio or video:
        next_url = urlresolvers.reverse(test_run, kwargs={'test_pk': test_pk})
        return redirect_with_args(test_check, {'next': next_url,}, kwargs={'test_pk': test_pk})
    return redirect(test_run, test_pk=test_pk)


@require_GET
@participant_required(redirect_to=participant_new, next_view_name='test')
def test_check(request, participant, test_pk):
    test = get_object_or_404(Test, pk=test_pk)
    next_url = urlresolvers.reverse(test_run, kwargs={'test_pk': test_pk})
    return render(request, 'test_check.html', {
        'test': test,
        'participant': participant,
        'next': next_url,
    })


@require_GET
@participant_required(redirect_to=participant_new, next_view_name='test')
def test_run(request, participant, test_pk):
    test = get_object_or_404(Test, pk=test_pk)
    next_url = urlresolvers.reverse(test_results, kwargs={'test_pk': test_pk})
    return render(request, 'test_run.html', {
        'test': test,
        'participant': participant,
        'next': next_url,
        'result': test.get_result_for(participant)
    })


@require_GET
@participant_required(redirect_to=participant_new, next_view_name='test')
def test_results(request, participant, test_pk):
    test = get_object_or_404(Test, pk=test_pk)
    return render(request, 'test_results.html', {
        'test': test,
        'participant': participant,
        'result': test.get_result_for(participant)
    })


@require_GET
def test_stats(request, test_pk):
    test = get_object_or_404(Test, pk=test_pk)
    participant = Participant.from_request(request)
    return render(request, 'test_stats.html', {
        'test': test,
        'participant': participant,
        'result': test.get_result_for(participant)
    })


@require_GET
def test_embed(request, test_pk, path):
    test = get_object_or_404(Test, pk=test_pk)

    abs_path = os.path.join(test.get_web_directory_path(), path)
    file = open(abs_path, 'rb')
    content = file.read()
    file.close()

    mime_type = mimetypes.guess_type(abs_path)[0]
    if mime_type is None:
        mime = 'application/octet-stream'
    else:
        mime = mime_type

    return HttpResponse(content, content_type=mime)
