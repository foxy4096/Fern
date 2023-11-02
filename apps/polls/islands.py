from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ChoiceCreationForm


@login_required
def choice_create(request):
    if request.method == 'POST':
        form = ChoiceCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ChoiceCreationForm()
    return render(request, 'polls/islands/choice_create.html', {'form': form})