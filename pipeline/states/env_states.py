from dataclasses import field,dataclass
from typing import Dict, List

from made.chat_env.entity.env_states import EnvStates

@dataclass
class ExampleEnvStates:
    # example: state1: int = 0 state2: str = "" state3: List[int] = field(default_factory=list) state4: Dict[str, str] = field(default_factory=dict)
    error_code: str = ""
    current_step: int = 1
    total_step_num: int = 0
    total_step_num: int = 0
    skeleton_code: str = ""
    impl_step: str =""
    error_code: str = ""
    current_step: int = 1
    total_step_num: int =0
    code_error_resolve_attempts: int = 1
    demand_analysis_result:str = ""
    initial_structure:str = ""
    return_type_violation_in_inital_structure:str = ""
    return_type_violation_in_writing_skeleton_code:str = ""