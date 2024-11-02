from dataclasses import field
from typing import List, Dict

from made.phase.entity.phase_states import PhaseStates


class ImplementationSequencingPhaseStates(PhaseStates):
    skeleton_code:str = ""
    initial_structure:str = ""