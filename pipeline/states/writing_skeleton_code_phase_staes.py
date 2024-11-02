
from dataclasses import field
from typing import List, Dict

from made.phase.entity.phase_states import PhaseStates


class WritingSkeletonCodePhaseStates(PhaseStates):
    task: str = ""
    demand_analysis_result: str = ""
    initial_structure:str = ""
    skeleton_code:str = ""
    return_type_violation_in_writing_skeleton_code:str = ""
