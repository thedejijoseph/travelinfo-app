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
    if request.method == 'POST':
        form = TerminalForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            terminal = Terminal()
            terminal.save()
            try:
                terminal.name = data['name']
                terminal.mode = data['mode']
                terminal.description = data['description']
                terminal.state = State.objects.get(state_id=data['state'])

                dest_terminals = [Terminal.objects.get(terminal_id=terminal_id) for terminal_id in data['dest_terminals']]
                for dest_terminal in dest_terminals:
                    terminal.dest_terminals.add(dest_terminal)
                
                terminal.save()
                return HttpResponseRedirect('/')
            except:
                # ensure incomplete records are not written to db
                terminal.delete()
    else:
        form = TerminalForm()

    return render(request, 'browser/terminals_new.html', {'form': form})

def terminals_edit(request, terminal_id):
    terminal = Terminal.objects.get(terminal_id=terminal_id)

    if request.method == 'POST':
        form = TerminalForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            terminal.name = data['name']
            terminal.mode = data['mode']
            terminal.description = data['description']
            terminal.state = State.objects.get(state_id=data['state'])

            terminal.dest_terminals.clear() # avoid incremental addition
            dest_terminals = [Terminal.objects.get(terminal_id=terminal_id) for terminal_id in data['dest_terminals']]
            for dest_terminal in dest_terminals:
                terminal.dest_terminals.add(dest_terminal)
            
            terminal.save()
            return HttpResponseRedirect(f'/terminals/{terminal_id}')
    else:
        existing_data = {
            'name': terminal.name,
            'mode': terminal.mode,
            'state': terminal.state.state_id,
            'description': terminal.description,
            'dest_terminals': [dest_terminal.terminal_id for dest_terminal in terminal.dest_terminals.all()]
        }
        form = TerminalForm(initial=existing_data)
    
    context = {'terminal': terminal, 'form': form}
    return render(request, 'browser/terminals_edit.html', context)

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

