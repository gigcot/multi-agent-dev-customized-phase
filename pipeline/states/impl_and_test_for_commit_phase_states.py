from dataclasses import field,dataclass
from typing import List, Dict

from made.phase.entity.phase_states import PhaseStates
import re
@dataclass
class ImplAndTestForCommitPhaseStates:
    skeleton_code: str =""
    impl_step: str = ""
    project_structure: str = ""
    error_code: str = ""
    current_step: int = 1
    total_step_num: int =0