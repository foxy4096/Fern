from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuestionCreationForm
from .models import Question

from apps.core.utils import is_htmx, paginate
from django.shortcuts import get_object_or_404

@login_required
def index(request):
    qform = QuestionCreationForm()
    questions = paginate(request, Question.objects.all())
    return render(request, "polls/index.html", {"questions": questions, "qform": qform})


@login_required
def poll_create(request):
    if request.method == "POST":
        qform = QuestionCreationForm(request.POST)
        if qform.is_valid():
            question = qform.save(commit=False)
            question.created_by = request.user
            question.save()
            return redirect("polls:poll_detail", question.id)
    qform = QuestionCreationForm()
    return render(request, "polls/poll_create.html", {"qform": qform})


@login_required
def my_polls(request):
    questions = paginate(request, Question.objects.filter(created_by=request.user))
    return render(request, "polls/my_polls.html", {"questions": questions})


@login_required
def poll_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    is_voted = question.has_user_voted(request.user)
    return render(request, "polls/poll_detail.html", {"question": question, "is_voted": is_voted})
