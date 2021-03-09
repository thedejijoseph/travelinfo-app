from django.shortcuts import render

from .forms import TerminalForm

def index(request):
    return render(request, 'browser/index.html')

def terminals_new(request):
    form = TerminalForm()
    return render(request, 'browser/terminals_new.html', {'form': form})
