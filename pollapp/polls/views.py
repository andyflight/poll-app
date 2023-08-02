from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, Candidate, Vote
from .forms import AddPollForm, CandidateForm
from django.contrib import messages


def index(request):
    active_polls = Poll.objects.filter(is_active=1).order_by('-id')
    finished_polls = Poll.objects.filter(is_active=0).order_by('-id')
    context = {
        'active_polls': active_polls,
        'finished_polls': finished_polls
    }
    return render(request, 'polls/index.html', context)

def about(request):
    return render(request, 'polls/about.html')


@login_required
def add_poll(request):
    if request.method == "POST":
        form = AddPollForm(request.POST, instance=Poll())
        candidates = [CandidateForm(request.POST, prefix=str(x), instance=Candidate()) for x in range(0, 2)]

        if form.is_valid() and all([c.is_valid() for c in candidates]):
            poll = form.save(commit=False)
            poll.owner = request.user
            poll.save()
            for c in candidates:
                new_c = c.save(commit=False)
                new_c.poll = poll
                new_c.save()

            messages.success(
                request, "Poll & Candidates added successfully",
                extra_tags='alert alert-success alert-dismissible fade show')

            return redirect('home')

    else:
        form = AddPollForm()
        candidates = [CandidateForm(prefix=str(x), instance=Candidate()) for x in range(0,2)]

    context = {
        'form': form,
        'candidates': candidates
    }
    return render(request, 'polls/poll_add.html', context)

def poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user
    if not poll.is_active:
        return redirect('results', poll_id)
    if not user.is_authenticated or not poll.can_vote(user):
        return render(request, 'polls/poll_detail.html', {'poll': poll, 'user':user})
    else:
        if request.method == 'POST':
            candidate_id = request.POST.get('candidate')
            if candidate_id:
                candidate = Candidate.objects.get(pk=candidate_id)
                vote = Vote(user=request.user, poll=poll, candidate=candidate)
                vote.save()
                return redirect('detail', poll_id)
            else:
                messages.error(
                    request, "No choice selected", extra_tags='alert alert-warning alert-dismissible fade show')
        return render(request, 'polls/poll_vote.html', {'poll':poll, 'user':user})




def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    candidates = poll.candidate_set.all()
    if candidates[0].vote_set.count() == candidates[1].vote_set.count():
        winner = "DRAW"
    else:
        winner = (candidates[0], candidates[1])[candidates[0].vote_set.count() < candidates[1].vote_set.count()]
    return render(request, 'polls/poll_results.html', {'poll': poll, 'candidates':candidates, 'winner': winner} )


@login_required
def my_polls(request):
    user = request.user
    polls = Poll.objects.filter(owner=user).order_by('-is_active')
    context = {
        'polls': polls
    }
    return render(request, 'polls/my_polls.html', context)

@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.delete()
    return redirect('my polls')

@login_required
def stop_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.is_active = not poll.is_active
    poll.save()
    return redirect('my polls')



def PageNotFound(request, exception):
    return render(request, 'polls/PageNotFound.html')
