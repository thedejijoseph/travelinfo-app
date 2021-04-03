from django.shortcuts import render
from django.http import JsonResponse, response

from browser.models import Terminal, State


def make_error_response(message, errors=None):
    partial_response = {
        'success': False,
        'message': message,
        'errors': errors
    }
    return JsonResponse(partial_response)

def make_success_response(message, data=None):
    partial_response = {
        'success': True,
        'message': message,
        'data': data
    }
    return JsonResponse(partial_response)

def query(request):
    if not request.GET:
        response = make_error_response(
            "You need to provide from_state and dest_state URL parameters"
        )
        return response
    
    from_state_id = request.GET.get('from_state')
    dest_state_id = request.GET.get('dest_state')

    try:
        from_state = State.objects.get(state_id=from_state_id)
        if from_state.terminal_set.count() == 0:
            # state does not have any terminal
            response = make_error_response(
                f'We do not, currently, know of any terminal in {from_state.name}'
            )
            return response
    except State.DoesNotExist:
        response = make_error_response(f'"from" state with id "{from_state_id}" does not exist')
        return response
    
    try:
        dest_state = State.objects.get(state_id=dest_state_id)
        if dest_state.terminal_set.count() == 0:
            # state also does not have any connecting terminal
            response = make_error_response(
                f'We do not, currently, know of any terminal in {dest_state.name}'
            )
            return response
    except State.DoesNotExist:
        response = make_error_response(f'"dest" state with id "{dest_state_id}" does not exist')
        return response
    
    connected_terminals = {}
    for terminal in from_state.terminal_set.all():
        for dest_terminal in terminal.dest_terminals.all():
            if dest_terminal.state.state_id == dest_state_id:
                connected_terminals.setdefault(terminal, []).append(dest_terminal)
    
    if len(connected_terminals) > 0:
        response = make_success_response(
            f'These terminals in {from_state.name} travel to {dest_state.name}',
            data = [
                {
                    'terminal': terminal.name,
                    'description': terminal.description,
                    'connected': [t.name for t in connected_terminals[terminal]]
                }
                for terminal in connected_terminals
            ]
        )
        return response
    else:
        response = make_success_response(
            f'These terminals are in {from_state.name}, but we do not know if they travel to {dest_state.name}',
            data = [
                {
                    'terminal': terminal.name,
                    'description': terminal.description
                }
                for terminal in from_state.terminal_set.all()
            ]
        )
        return response

def state_id(request):
    """this endpoint searches/predicts the intended state and therefore
    state_id from a given query.

    for example, given a query of ikeja, the endpoint will return a state_id
    of -lagos-
    """

    pass
