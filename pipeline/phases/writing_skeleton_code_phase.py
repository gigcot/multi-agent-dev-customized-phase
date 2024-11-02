from pipeline.states.writing_skeleton_code_phase_staes import WritingSkeletonCodePhaseStates
from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from pipeline.utils.utils import parse_text, rewrite_codes, validate_response_format, load_codes_from_hardware


@PhaseRegistry.register()
class WritingSkeletonCodePhase(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt: str = """

고객의 요청사항: {task}
결정 된 프로젝트 구조:
{initial_structure}

[상황]
우리는 이 구조에 따라 들어갈 클래스와 메서드의 틀을 잡아두고 pass로 비워둔 상태를 스켈레톤 코드를 작성해야 합니다.
[조건]
1. 결정된 프로젝트 구조와 파일명에 따라 **모든** 파일을 in one go 작성해야 합니다.
1-1. **test파일은 스켈레톤 코드가 필요없습니다.** 구현 단계에서 작성할 예정이므로 빈 디렉토리로 두어 반환 하세요.
2. 각 파일의 이름과 내용을 아래 마크다운 형식에 따라 작성해야 합니다. **파일의 레벨은 #으로 구분합니다.**
2-1. 작성한 내용을 협업자 모두 follow 할 수 있도록 마크다운 형식을 엄격히 준수해야 합니다.
{return_type_violation_in_writing_skeleton_code}
마크다운 형식:

FILENAME
```
''' 
DOCSTRING
''' 
CODE
```


""",
        assistant_role_name: str = "Skeleton Architect",
        assistant_role_prompt: str = """당신은 SI-Follow의 AI 조직원입니다. SI-Follow는 고객의 요구에 맞춘 신뢰성 있는 맞춤형 소프트웨어 솔루션을 제공하는 AI IT파트너입니다.
조직원 모두 명확한 역할을 맡아 협력하고 있으며, 프로젝트의 성공을 목표로 합니다. 이번 고객의 요청한 요구 사항은 \"{task}\"입니다.
당신은 Skeleton Architect입니다. 프로젝트의 전반적인 구조를 이해하고, 이를 스켈레톤 코드로 구조화하는 탁월한 능력을 갖춘 전문가입니다.
프로젝트의 기능적 요구사항과 결정된 구조를 기반으로, 각 파일에 필요한 클래스와 메서드를 직관적으로 설계하여 프로젝트의 안정성과 확장성을 고려한 기틀을 마련합니다.""",
        user_role_name: str = "user",
        user_role_prompt: str = "You are discussing about {task} with {assistant_role}",
        chat_turn_limit: int = 1,
        temperature=0.5,
        top_p=0.5,
        states=WritingSkeletonCodePhaseStates(),
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
        self.states.initial_structure = env.states.initial_structure
        self.states.return_type_violation_in_writing_skeleton_code = env.states.return_type_violation_in_writing_skeleton_code

    def update_env_states(self, env):
        env.states.skeleton_code = load_codes_from_hardware(env.config.directory)
        return env
    
    def execute(self, env: ChatEnvRepositoryImpl,) -> ChatEnvRepositoryImpl:
        self.update_phase_states(env)
        while True:
            seminar_conclusion = self.chatting(
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
            message, is_valid = validate_response_format(seminar_conclusion)
            if not is_valid:
                self.states.return_type_violation_in_writing_skeleton_code = message
                continue
            if is_valid:
                path_and_codes = parse_text(seminar_conclusion)
                rewrite_codes(path_and_codes, base_path=env.config.directory)
                break
        self.update_env_states(env)

        return env


# 메서드 추가
