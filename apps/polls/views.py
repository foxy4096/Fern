from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import QuestionCreationForm, ChoiceCreationForm
from .models import Choice, Question

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
            messages.success(request, "Your question has been created!")
            return redirect("polls:poll_edit", question.id)
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
    return render(
        request, "polls/poll_detail.html", {"question": question, "is_voted": is_voted}
    )


@login_required
def poll_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        qform = QuestionCreationForm(request.POST, instance=question)
        if qform.is_valid():
            qform.save()
            messages.success(request, "Your question has been updated!")
            return redirect("polls:poll_edit", pk)
    qform = QuestionCreationForm(instance=question)
    return render(
        request, "polls/poll_edit.html", {"qform": qform, "question": question}
    )


@login_required
def poll_choice_create(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        cform = ChoiceCreationForm(request.POST)
        if cform.is_valid():
            choice = cform.save(commit=False)
            choice.question = question
            choice.save()
            messages.success(request, "Your choice has been created!")
            if request.POST.get("save_and_continue"):
                return redirect("polls:poll_choice_create", pk)
            return redirect("polls:poll_edit", pk)

    cform = ChoiceCreationForm()
    return render(
        request, "polls/poll_choice_create.html", {"cform": cform, "question": question}
    )


@login_required
def poll_choice_delete(request, pk):
    choice = get_object_or_404(Choice, pk=pk, question__created_by=request.user)
    if request.method == "POST":
        choice.delete()
        messages.success(request, "Your choice has been deleted!")
    return redirect("polls:poll_edit", choice.question.id)


@login_required
def poll_delete(request, pk):
    question = get_object_or_404(Question, pk=pk, created_by=request.user)
    if request.method == "POST":
        question.delete()
        messages.success(request, "Your question has been deleted!")
    return redirect("polls:index")


@login_required
def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST" and not question.has_user_voted(request.user):
        choice_id = request.POST.get("choice")
        choice = get_object_or_404(Choice, pk=choice_id)
        choice.votes += 1
        choice.voted_by.add(request.user)
        question.voted_by.add(request.user)
        choice.save()
        messages.success(request, "Your vote has been recorded!")
    return redirect("polls:poll_detail", pk)
