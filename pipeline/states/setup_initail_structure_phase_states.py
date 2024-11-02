from dataclasses import field
from typing import List, Dict

from made.phase.entity.phase_states import PhaseStates


class SetupInitialSturcturetPhaseStates(PhaseStates):
    task: str = ""
    demand_analysis_result: str = ""
    return_type_violation_in_inital_structure: str = ""

