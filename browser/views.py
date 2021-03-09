from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import TerminalForm
from .models import Terminal, State

def index(request):
    return render(request, 'browser/index.html')

def terminals_new(request):
    # return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = TerminalForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            terminal = Terminal()
            terminal.name = data['name']
            terminal.mode = data['mode']
            terminal.description = data['description']
            terminal.state = State.objects.get(state_id=data['state'])
            terminal.save() # saving here to generate id. id is needed to create manytomany relationship
            dest_terminals = [Terminal.objects.get(terminal_id=terminal_id) for terminal_id in data['dest_terminals']]
            for dest_terminal in dest_terminals:
                terminal.dest_terminals.add(dest_terminal)
            terminal.save()
            return HttpResponseRedirect('/')
    else:
        form = TerminalForm()

    return render(request, 'browser/terminals_new.html', {'form': form})
