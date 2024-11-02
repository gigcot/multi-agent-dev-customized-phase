from dataclasses import field
from typing import List, Dict

from made.phase.entity.phase_states import PhaseStates


class DemandAnalysisPhaseStates(PhaseStates):
    task:str = ""

