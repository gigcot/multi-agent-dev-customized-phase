# 기능 정의
from pipeline.states.demand_analysis_phase_states import DemandAnalysisPhaseStates
from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl



@PhaseRegistry.register()
class DemandAnalysisPhase(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt: str = """
[상황]
SI-Follow는 이러한 개발 절차를 사용합니다:
1. 고객 요구사항에 따른 필요한 기능 분석
2. 기능에 따른 디렉토리 구조 정의, 스켈레톤 코드 작성
3. 메서드별 기능 구현 단계 수립
4. 코드 구현 및 테스트
5. 각종 문서 작성

현재 단계는"1. 고객 요구사항에 따른 필요한 기능 분석"이며,
이번 프로젝트에서 제공해야 할 기능을 결정해야 합니다. 고객의 요구와 시스템이 사용자에게 제공할 가치를 고려해서, 구현할 기능들을 답변해야 합니다.
고객의 요청사항 : "{task}"

필요하다고 생각되는 기능과 설명을 답변하세요.
협업자 모두가 follow할 수 있도록 반환형식에 따라 답변해야합니다.


반환 형식:
<INFO>
Project Name:
1.*
2.*
3.*
...

""",
        assistant_role_name: str = "Chief Product Strategist",
        assistant_role_prompt: str = """
당신은 SI-Follow의 AI 조직원입니다. SI-Follow는 고객의 요구에 맞춘 신뢰성 있는 맞춤형 소프트웨어 솔루션을 제공하는 AI IT파트너입니다.
조직원 모두 명확한 역할을 맡아 협력하고 있으며, 프로젝트의 성공을 목표로 합니다. 이번 고객의 요청한 요구 사항은 \"{task}\"입니다.
당신은 최고 제품 전략 책임자입니다. 당신의 목표는 주어진 task의 요구 사항을 분석하고, 시스템이 제공해야 하는 기능을 파악하는 것입니다. 문제 해결에 있어서 거시적인 시각을 가지고 있으며 당신의 활동은 다음과 같습니다.
1) 고객이 제공한 요구 사항을 전체적으로 분석하고, 시스템이 무엇을 해야 하는지 큰 틀에서 파악. 2) 필요한 주요 기능들을 식별하고 정의. 3) 세부 기능을 도출하기 위해 더 깊이 들어가며 구상.
        """,
        user_role_name: str = "user",
        user_role_prompt: str = "task:{task}",
        chat_turn_limit: int = 1,
        temperature=0.5,
        top_p=0.5,
        states=DemandAnalysisPhaseStates(),
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
        self.states.task = env.config.task_prompt

    def update_env_states(self, env):
        env.states.demand_analysis_result = self.seminar_conclusion
        print(f"**Demand Analysis Phase.**\n\nseminar conclusion: {self.seminar_conclusion}")
        return env
