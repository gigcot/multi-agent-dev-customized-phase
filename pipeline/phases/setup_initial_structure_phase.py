from pipeline.states.setup_initail_structure_phase_states import SetupInitialSturcturetPhaseStates
from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl


@PhaseRegistry.register()
class SetupInitialSturcturePhase(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt: str = """
[상황]
고객의 요청: "{task}"
현재까지 진행된 단계: 고객 요청에 따라 추가할 기능 설정
현재 진행해야 하는 단계: 추가할 기능에 따른 클래스, 메서드 설정과 그것에 따른 디렉토리 구조 작성
결정된 기능:
{demand_analysis_result}

[지시] 기능을 구현하기 위한 디렉토리 구조를 고려하여 작성하세요.

[조건]
1. 필요한 파일과 클래스, 메서드를 시스템 안정성과 확장성을 고려하여 작성해야 함.
2. 결정된 기능이 전부 포함되어야 함.
3. 궁극적으로 프로젝트가 실행 될 엔트리 포인트인 "main.py"가 있어야 함.
    이후 단계에서 코드 구현 시 테스트 파일들이 추가될 "test/" 디렉토리가 __init__.py만 있어야 함.

답변 형식은 다음과 같은 계층 구조 예시를 따르세요.
작성되는 파일은 전부 최상위 디렉토리 내에 있어야 합니다.
"{return_type_violation_in_inital_structure}"

계층 구조 예시:
```
1. top_level_dir/
    1.1 */
        1.1.1 *.py: description
        ...
    1.2 */
        1.2.1 *.py: description
        ...
    1.3 */
        1.3.1 *.py: description
        ...
    ...
    1.n test/
        1.n.1 __init__.py
    1.n+1 main.py: project main entry point
```


""",
        assistant_role_name: str = "System Architect",
        assistant_role_prompt: str = """당신은 SI-Follow의 AI 조직원입니다. SI-Follow는 고객의 요구에 맞춘 신뢰성 있는 맞춤형 소프트웨어 솔루션을 제공하는 AI IT파트너입니다.
조직원 모두 명확한 역할을 맡아 협력하고 있으며, 프로젝트의 성공을 목표로 합니다. 이번 고객의 요청한 요구 사항은 \"{task}\"입니다.
당신은 고급 시스템 구조 설계 전문가로서, 결정된 기능을 깊이 이해하고 이를 디렉토리 구조와 파일 구성에 자연스럽게 녹여내어 최적의 형태로 설계합니다.
프로젝트의 안정성과 확장성을 자연스럽게 고려하며, 요구 사항에 맞춘 최적의 구조를 마련하는 데 뛰어난 감각을 발휘합니다.""",
        user_role_name: str = "user",
        user_role_prompt: str = "Hi",
        chat_turn_limit: int = 1,
        temperature=0.5,
        top_p=0.5,
        states=SetupInitialSturcturetPhaseStates(),
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
        self.states.return_type_violation_in_inital_structure = env.states.return_type_violation_in_inital_structure
        self.states.task = env.config.task_prompt
        self.states.demand_analysis_result = env.states.demand_analysis_result

    def update_env_states(self, env):
        env.states.initial_structure = self.states.initial_structure

        return env

    def execute(
        self,
        env: ChatEnvRepositoryImpl,
    ) -> ChatEnvRepositoryImpl:
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
            message, is_correct, structure = check_answer_in_init_structure(seminar_conclusion)
            print(f"message: {message}, is_correct: {is_correct}")
            if is_correct:
                self.states.initial_structure= structure
                self.update_env_states(env)
                print(f"structure:{structure}")
                break
            if is_correct is not True:
                self.states.return_type_violation_in_inital_structure = message
                continue
        self.update_env_states(env)

        return env
# 메서드 추가
from typing import Tuple

def check_answer_in_init_structure(answer_str: str) -> Tuple[str, bool, str]:
    import re

    error_messages = []
    pass_check = True
    code_block_content = ""

    # 코드 블록 추출을 위한 정규표현식 패턴
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, answer_str, re.DOTALL)

    if not matches:
        error_messages.append("답변은 ```로 시작하고 ```로 끝나야 하며, 그 안에 내용이 있어야 합니다.")
        pass_check = False
    else:
        code_block_content = matches[0].strip()
        if not code_block_content:
            error_messages.append("코드 블록 안에 내용이 없습니다.")
            pass_check = False
        else:
            lines = code_block_content.strip().splitlines()
            if len(lines) < 2:
                error_messages.append("코드 블록 안에 디렉토리 구조가 없습니다.")
                pass_check = False
            else:
                # 번호 체계를 기반으로 계층 구조 파싱
                hierarchy = {}
                parent_stack = []
                top_level_nodes = []
                for line in lines:
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue  # 빈 라인 건너뜀

                    # 번호와 내용 분리
                    match = re.match(r'(\d+(\.\d+)*)\s+(.*)', stripped_line)
                    if match:
                        num_str, _, content = match.groups()
                        num_parts = num_str.split('.')
                        level = len(num_parts)

                        # 파일명과 설명 분리
                        content_parts = content.split(':', 1)
                        content_name = content_parts[0].strip()
                        description = content_parts[1].strip() if len(content_parts) > 1 else ''

                        # 파일과 디렉토리 구분
                        if content_name.endswith('/'):
                            node_type = 'directory'
                            content_name = content_name.rstrip('/')
                        else:
                            node_type = 'file'

                        node = {
                            'number': num_str,
                            'content': content_name,
                            'type': node_type,
                            'children': []
                        }

                        # 현재 레벨에 맞게 부모 스택 조정
                        while len(parent_stack) >= level:
                            parent_stack.pop()

                        if parent_stack:
                            parent_stack[-1]['children'].append(node)
                        else:
                            hierarchy[num_str] = node
                            top_level_nodes.append(node)  # 최상위 노드로 추가

                        parent_stack.append(node)
                    else:
                        # 번호 체계가 없는 경우 무시하거나 오류 처리 가능
                        continue

                # 최상위 레벨 항목 수 검사
                if len(top_level_nodes) != 1:
                    error_messages.append("최상위 디렉토리와 같은 레벨에 다른 디렉토리나 파일이 있어서는 안 됩니다.")
                    pass_check = False

                # test 디렉토리 검사 함수 정의
                def check_test_dirs(node):
                    nonlocal pass_check
                    # 'test'로 시작하고 정확히 일치하는 디렉토리 찾기
                    if node['type'] == 'directory' and re.match(r'^test[s]?$', node['content']):
                        if not node['children']:
                            error_messages.append(f"'{node['content']}/' 디렉토리에는 '__init__.py' 파일이 포함되어 있어야 합니다.")
                            pass_check = False
                        elif len(node['children']) > 1:
                            error_messages.append(f"'{node['content']}/' 디렉토리에는 '__init__.py' 파일만 포함되어 있어야 합니다.")
                            pass_check = False
                        else:
                            child = node['children'][0]
                            if child['type'] != 'file' or child['content'] != '__init__.py':
                                error_messages.append(f"'{node['content']}/' 디렉토리에는 '__init__.py' 파일만 포함되어 있어야 합니다.")
                                pass_check = False
                    # 자식 노드에 대해 재귀적으로 검사
                    for child in node['children']:
                        check_test_dirs(child)

                # 최상위 노드에 대해 test 디렉토리 검사 실행
                for node in top_level_nodes:
                    check_test_dirs(node)

    error_message = '\n'.join(error_messages) if error_messages else "OK"
    return error_message, pass_check, code_block_content

