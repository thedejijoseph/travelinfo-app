from django import forms

from .models import State, Terminal


def get_list_of_states():
    ALL_STATES = [(state.state_id, state.name) for state in State.objects.all()]
    return ALL_STATES

def get_supported_modes():
    AIR = "air"
    ROAD = "road"
    RAIL = "rail"
    SUPPORTED_MODES = (
        (AIR, 'Air'),
        (ROAD, 'Road'),
        (RAIL, 'Rail')
    )
    return SUPPORTED_MODES

def get_dest_terminals():
    ALL_TERMINALS = [(terminal.terminal_id, terminal.name) for terminal in Terminal.objects.all()]
    return ALL_TERMINALS

class TerminalForm(forms.Form):
    name = forms.CharField(label="Terminal's name")
    mode = forms.ChoiceField(choices=get_supported_modes)
    state = forms.ChoiceField(choices=get_list_of_states)
    description = forms.CharField(widget=forms.Textarea, help_text="Describe the physical characteristics of the terminal, plus how to get there.")
    dest_terminals = forms.MultipleChoiceField(choices=get_dest_terminals, label="Destination terminals", required=False)
