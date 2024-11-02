from pipeline.states.implementation_sequencing_phase_states import ImplementationSequencingPhaseStates
from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from pipeline.utils.utils import load_codes_from_hardware
@PhaseRegistry.register()
class ImplementationSequencingPhase(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt: str = """
[이번 고객의 요청 사항] {task}
[상황]
우리는 작성된 스켈레톤 코드와 프로젝트 구조를 확인하고,
**의존성**을 고려하여 메서드 구현 작업의 우선순위를 작성해야 합니다.
[조건]
1. 스켈레톤 코드에서 파일의 level은 #으로 구별되어 있습니다. 프로젝트 구조를 참고하세요.
2. 작성된 스켈레톤 코드에 포함된 메서드만 리스트에 포함할 수 있습니다.
3. **For all classes and methods** 작업 순서를 정하세요.
5. 작성한 내용을 협업자 모두 follow 할 수 있도록 **아래 format을 엄격히 준수**해야 합니다.

**format**:
<sequence>
1. PATH/FILENAME - class.method: impl what method
2. PATH/FILENAME - class.method: impl what method
3. ...
...
<sequence/>


스켈레톤코드:
{skeleton_code}
프로젝트 구조:
{initial_structure}

""",
        assistant_role_name: str = "Software Architect",
        assistant_role_prompt: str = """[당신은 SI-Follow의 AI 조직원입니다. SI-Follow는 고객의 요구에 맞춘 신뢰성 있는 맞춤형 소프트웨어 솔루션을 제공하는 AI IT파트너입니다.
조직원 모두 명확한 역할을 맡아 협력하고 있으며, 프로젝트의 성공을 목표로 합니다. 이번 고객의 요청한 요구 사항은 \"{task}\"입니다.
당신은 뛰어난 소프트웨어 아키텍트로서, 복잡한 시스템의 구조와 구성 요소 간의 의존성을 명확하게 이해하고 관리할 수 있습니다.
프로젝트의 전체적인 아키텍처를 설계하고, 각 기능의 구현 우선순위를 결정하여 효율적인 개발 프로세스를 이끌어냅니다.
고객의 요구사항을 파악하고, 팀원들과 효과적으로 협업하여 프로젝트의 성공을 이끌었던 경험이 많습니다.]
""",
        user_role_name: str = "user",
        user_role_prompt: str = "Hi.",
        chat_turn_limit: int = 1,
        temperature=0.5,
        top_p=0.5,
        states=ImplementationSequencingPhaseStates(),
        **kwargs,
    ):
        super().__init__(
            model_config=model_config,
            phase_prompt=phase_prompt,
            assistant_role_name=assistant_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_name=user_role_name,
            user_role_prompt=user_role_prompt,
            chat_turn_limit=chat_turn_limit,
            temperature=temperature,
            top_p=top_p,
            states=states,
            **kwargs,
        )

    def update_phase_states(self, env):
        self.states.skeleton_code = env.states.skeleton_code
        self.states.initial_structure = env.states.initial_structure


    def update_env_states(self, env):
        env.states.impl_step = self.states.impl_step
        return env
    
    def execute(
        self,
        env: ChatEnvRepositoryImpl,
    ) -> ChatEnvRepositoryImpl:
        self.update_phase_states(env)
        self.seminar_conclusion = self.chatting(
            env=env,
            task_prompt=env.config.task_prompt,
            phase_prompt=self.phase_prompt,
            assistant_role_name=self.assistant_role_name,
            assistant_role_prompt=self.assistant_role_prompt,
            user_role_name=self.user_role_name,
            user_role_prompt=self.user_role_prompt,
            placeholders=self.states,
            chat_turn_limit=self.chat_turn_limit,
        )
        self.states.impl_step = self.seminar_conclusion
        self.update_env_states(env)
        return env
