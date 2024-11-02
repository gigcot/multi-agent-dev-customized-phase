from dataclasses import field
from typing import List, Dict

from made.phase.entity.phase_states import PhaseStates


class ExamplePhaseStates(PhaseStates):
    state1: int = 0
    state2: str = ""
    state3: List[int] = field(default_factory=list)
    state4: Dict[str, str] = field(default_factory=dict)
