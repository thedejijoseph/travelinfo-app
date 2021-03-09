from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import TerminalForm
from .models import Terminal, State

def index(request):
    states = State.objects.all()
    states = sorted(states, key=lambda s: s.terminal_set.count(), reverse=True)
    terminals = Terminal.objects.all()

    context = {'terminals': terminals, 'states': states[:12]}
    return render(request, 'browser/index.html', context)

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

def terminals_edit(request):
    return render(request, 'browser/terminals_edit.html')

def terminals_all(request):
    terminals = Terminal.objects.all()

    context = {'terminals': terminals}
    return render(request, 'browser/terminals_all.html', context)

def terminals_page(request, terminal_id):
    terminal = Terminal.objects.get(terminal_id=terminal_id)

    context = {'terminal': terminal}
    return render(request, 'browser/terminals_page.html', context)

def states_all(request):
    states = State.objects.all()

    context = {'states': states}
    return render(request, 'browser/states_all.html', context)

def states_page(request, state_id):
    state = State.objects.get(state_id=state_id)

    context = {'state': state}
    return render(request, 'browser/states_page.html', context)

