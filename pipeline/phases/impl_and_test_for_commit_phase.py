from made.chat_env.repository.chat_env_repository_impl import ChatEnvRepositoryImpl
from made.engine import ModelConfig
from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.tools.docker.repository.docker_tool_repository_impl import DockerToolRepositoryImpl
from pipeline.states.impl_and_test_for_commit_phase_states import ImplAndTestForCommitPhaseStates

@PhaseRegistry.register()
class ImplAndTestForCommitPhase(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config: ModelConfig,
        phase_prompt: str = 
"""
[아래 주어진 자료를 참고하여, 조건과 상황에 맞는 답변을 반환 형식에 따라 작성하세요.]

[자료]

현재까지 작성된 스켈레톤 코드: (#으로 level이 구분되어 있습니다.)

{skeleton_code}
전체 구현 단계:
{impl_step}
[조건]
1. 우리는 전체 진행 단계에 대해 한 단계씩, 작성한 코드의 테스트가 통과할 때 까지 코드를 작성 또는 수정하고 다음단계로 진행되는 작업을 진행 중입니다.
2. 현재 진행 중인 단계에 해당하는 작업을 진행하세요. 스켈레톤 코드에서 내용을 추가 또는 수정하면 됩니다.
    **답변 시 추가/수정 사항을 전체 코드와 함께 반환해야합니다.**
3. 현재단계 메서드 구현과 해당 메서드 테스트 코드도 함께 작성해야 합니다. 테스트 코드는 test폴더 내에 작성 해야합니다. 
    테스트 코드는 테스트 케이스를 고려하여 작성하세요. 또한 해당 테스트만을 진행하기 위한 메인가드 블록을 사용해야 합니다.
4. 코드의 작성은 반환 형식에 따라 #으로 level을 구분하여 최상위 부터 프로젝트 구조와 함께 작성되어야 합니다.
5. 다음 단계 진행 상 의존성 문제가 생기지 않는 선에서, 필요하다고 생각되는 경우 메서드 추가가 가능합니다.
    추가사항도 형식에 따라 프로젝트 구조와 일관되도록 작성 해야합니다.
6. 코드 작성을 마쳤다면 답변 마지막 줄에 테스트할 메서드가 포함된 파일을 형식에 따라 적으세요.
7. 협업자 모두가 follow할 수 있도록 **반환 형식을 반드시 지켜야 합니다**.

[상황]
1. 우리는 지금 고객의 요구에 만족하는 **프로젝트 코드와 테스트 코드 구현 성공을 목표**로 하고 있습니다.
2. 현재 우리는 "{current_step}단계"의 {code_error_resolve_attempts}번 째 코드 작성 시도 입니다.
3. 코드와 그 테스트 실행이 실패한 경우에만 작성 시도로 간주되며, 반환 형식 위반으로 인한 재작성은 시도 횟수에 포함하지 않습니다.
4. 시스템 메시지에 따라서
    a. 구현 단계에 해당하는 코드와 테스트 코드 작성.
    b. 테스트를 통과하도록 코드수정 또는 예외처리 추가
    c. 반환 형식을 준수하여 답변

"{current_step}단계 시스템 메시지:
"{error_code}"


반환 형식:
PATH/FILENAME
```python
'''
DOCSTRING
'''
CODE
```

{current_step}단계 테스트 파일 반환형식:
<Test this>PATH/FILENAME<Test this/>
""",
        assistant_role_name: str = "Programmer",
        assistant_role_prompt: str = """
[당신은 SI-Follow의 AI 조직원입니다. SI-Follow는 고객의 요구에 맞춘 신뢰성 있는 맞춤형 소프트웨어 솔루션을 제공하는 AI IT파트너입니다.
조직원 모두 명확한 역할을 맡아 협력하고 있으며, 프로젝트의 성공을 목표로 합니다. 이번 고객의 요청한 요구 사항은 \"{task}\"입니다.
당신은 숙련된 프로그래머로서, Python을 비롯한 다양한 프로그래밍 언어와 플랫폼에 대한 깊은 지식을 보유하고 있습니다.
프로젝트 구조를 이해하고 이를 바탕으로 최적의 코드를 설계하고 구현하는 데 탁월한 능력을 발휘합니다.
지침을 따르고 목표를 성공적으로 완수할 수 있는 뛰어난 문제 해결 능력을 갖추고 있습니다.]
""",
        user_role_name: str = "CTO",
        user_role_prompt: str = """
[당신은 SI-Follow의 AI 조직원입니다. SI-Follow는 고객의 요구에 맞춘 신뢰성 있는 맞춤형 소프트웨어 솔루션을 제공하는 AI IT파트너입니다.
조직원 모두 명확한 역할을 맡아 협력하고 있으며, 프로젝트의 성공을 목표로 합니다. 이번 고객의 요청한 요구 사항은 \"{task}\"입니다.
당신은 Chief Technology Officer입니다. 복잡한 문제 해결에 뛰어난 능력이 있으며, IT 기술에 대한 깊은 이해와 전문 지식을 바탕으로 프로젝트의 기술적 방향을 빠르고 효율적으로 조율할 수 있습니다.
특히, Dependency Injection(DI)와 Inversion of Control(IoC) 개념을 통해 모듈 간 결합도를 최소화하고, 유연하고 확장 가능한 아키텍처를 설계하는 데 능숙합니다.
당신은 이러한 원칙을 기반으로 최적의 기술적 결정을 내립니다. 책임감 있게 기술적 결정을 내리고, 팀이 직면한 상황을 해결하는 데 중대한 역할을 합니다.]
""",
        chat_turn_limit: int = 1,
        temperature=0.5,
        top_p=0.5,
        states = ImplAndTestForCommitPhaseStates(),
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

    def update_phase_states(self, env: ChatEnvRepositoryImpl):
        self.states.__dict__ = env.states.__dict__
        env.states.skeleton_code = load_codes_from_hardware(env.config.directory)


    def update_env_states(self, env: ChatEnvRepositoryImpl) -> ChatEnvRepositoryImpl:
        env.states.skeleton_code = load_codes_from_hardware(env.config.directory)
        return env
    
    def execute(
        self,
        env: ChatEnvRepositoryImpl,
    ) -> ChatEnvRepositoryImpl:
        
        container = DockerToolRepositoryImpl.get_container("si_foIIow_test", volume=env.config.directory)
        self.update_phase_states(env)
        print(f"{self.states.impl_step}\n==> 입력된 impl_step입니다.")
        self.states.total_step_num = count_steps(self.states.impl_step)
        print(f"{self.states.total_step_num}\n==> 계산된 step 수 입니다")
        is_error_in_conclusion = False
        for step in range(1, self.states.total_step_num+1):
            print(f"[ {step} ] 단계 작업입니다.")
            code_error_resolve_attempts = 1
            while True:
                self.update_phase_states(env)
                
                if is_error_in_conclusion :
                    env.states.error_code = f"이전 응답에서 반환 형식을 위반하여 코드 실행 전에 재응답을 요청하였습니다.:\n{error_message_in_validate}"
                env.states.code_error_resolve_attempts = code_error_resolve_attempts
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
                if not (result := validate_response_format(seminar_conclusion))[1]:
                    error_message_in_validate = result[0]
                    print(f"반환형식위반: {error_message_in_validate}")
                    env.config.error_code = f"이전 응답에서 반환 형식을 위반하여 코드 실행 전에 재응답을 요청하였습니다.: {error_message_in_validate}"
                    is_error_in_conclusion = True
                    continue
                clean_modified_codes=parse_text(seminar_conclusion)
                rewrite_codes(clean_modified_codes, base_path=env.config.directory) # 하드웨어에 직접 덮어씀
                file_path, file_name = extract_test_file(seminar_conclusion)
                error_code, is_step_complete = verify_functionality(file_path, file_name, container, env)
                print(f"error code: {error_code},\nis_step_complete: {is_step_complete}")
                remove_pycache_dirs(env)
                if is_step_complete != 0:
                    code_error_resolve_attempts += 1
                    if code_error_resolve_attempts == 4:
                        print(f"{step}단계 오류수정 시도 {code_error_resolve_attempts-1}회로 제한 횟수 초과하여 다음 구현 단계로 넘어갑니다.")
                        self.update_env_states(env)
                        self.states.current_step += 1
                        self.states.error_code = ""
                        is_error_in_conclusion = False
                        break 
                    self.update_env_states(env)## step 사용해서 현재 phase전달가능해야댐
                    env.states.error_code = error_code
                    print(f"**[{step}]Step 실패.**\n**[ERROR CODE]**: {error_code}")
                    is_error_in_conclusion = False
                    continue

                if is_step_complete == 0:
                    self.update_env_states(env)
                    self.states.error_code = ""
                    self.states.current_step += 1
                    is_error_in_conclusion = False
                    code_error_resolve_attempts = 1
                    #TODO: git commit
                    break
            print(f"{step}step completed")
        print("all staeps completed.")

        return env
    

### 추가된 메서드


import os

def load_codes_from_hardware(base_path):
    structure_lines = []
    project_path = os.path.join(base_path, 'project')

    # 'project' 폴더가 존재하는지 확인
    if not os.path.isdir(project_path):
        print(f"'project' 폴더가 {base_path} 내에 존재하지 않습니다.")
        return ""
    
    # 'project' 폴더 내부의 하위 폴더 리스트 가져오기
    subdirs = [d for d in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, d))]
    
    if not subdirs:
        print(f"'project' 폴더 내에 하위 폴더가 존재하지 않습니다.")
        return ""
    
    # 'project' 폴더 내부의 모든 하위 폴더를 순회
    for subdir in subdirs:
        subdir_path = os.path.join(project_path, subdir)
        for root, dirs, files in os.walk(subdir_path):
            rel_path = os.path.relpath(root, project_path)
            if rel_path == subdir:
                level = 3  # 최상위 하위 폴더는 ###로 시작
                heading = '### ' + os.path.basename(root) + '/'
            else:
                depth = rel_path.count(os.sep)
                level = min(depth + 3, 6)  # 최대 헤딩 레벨을 6으로 제한
                heading = '#' * level + ' ' + os.path.basename(root) + '/'

            structure_lines.append(heading)

            for filename in files:
                if filename.endswith('.py'):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code_content = f.read()
                    except Exception as e:
                        code_content = f"파일을 읽는 중 오류 발생: {e}"

                    file_heading = '#' * (level + 1) + ' ' + filename
                    structure_lines.append('')
                    structure_lines.append(file_heading)
                    structure_lines.append('```python')
                    structure_lines.append(code_content)
                    structure_lines.append('```')
                    structure_lines.append('')
                else:
                    # .py 파일이 아닌 경우 처리하지 않음 (필요에 따라 수정 가능)
                    pass
    result = '\n'.join(structure_lines)
    return result


## 추가된 메서드


import os
import re


from typing import List, Dict

def parse_text(input_str: str) -> List[Dict[str, str]]:
    """
    주어진 문자열에서 프로젝트 파일 경로와 코드 블록을 추출하여
    {'path': full_path, 'code': code_block} 형태의 딕셔너리 리스트로 반환합니다.

    Args:
        input_str (str): 파싱할 프로젝트 구조를 나타내는 문자열.

    Returns:
        List[Dict[str, str]]: 각 파일의 경로와 코드 블록을 포함하는 딕셔너리 리스트.
    """
    path_stack = []  # 현재 경로를 추적하기 위한 스택
    result = []      # 최종 결과를 저장할 리스트
    in_code_block = False  # 코드 블록 내부에 있는지 여부
    code_block_lang = ''   # 코드 블록의 언어 (예: python)
    code_lines = []        # 현재 코드 블록의 라인들을 저장
    current_file = None    # 현재 파일명을 저장

    # 정규식을 사용하여 헤더와 코드 블록을 식별
    header_pattern = re.compile(r'^(#{1,6})\s+(.*)')
    code_block_start_pattern = re.compile(r'^```(\w+)?')
    code_block_end_pattern = re.compile(r'^```$')

    lines = input_str.splitlines()

    for line in lines:
        # 코드 블록 시작
        if not in_code_block and code_block_start_pattern.match(line):
            in_code_block = True
            code_block_lang = code_block_start_pattern.match(line).group(1) or ''
            code_lines = []
            continue

        # 코드 블록 끝
        if in_code_block and code_block_end_pattern.match(line):
            in_code_block = False
            # 전체 경로 생성
            if current_file:
                full_path = '/'.join(path_stack + [current_file])
            else:
                full_path = '/'.join(path_stack)
            # 코드 블록의 내용을 하나의 문자열로 결합
            code = '\n'.join(code_lines).strip()
            # 결과 리스트에 추가
            result.append({
                'path': full_path,
                'code': code
            })
            continue

        # 코드 블록 내부인 경우 코드 라인 저장
        if in_code_block:
            code_lines.append(line)
            continue

        # 헤더 라인 처리
        header_match = header_pattern.match(line)
        if header_match:
            hashes, heading_text = header_match.groups()
            level = len(hashes)

            base_level = 3  # 프로젝트 루트를 3단계 헤더로 가정

            # 현재 스택의 길이를 조정하여 새로운 레벨에 맞춤
            while len(path_stack) >= (level - base_level + 1):
                path_stack.pop()

            if heading_text.endswith('/'):
                # 디렉토리인 경우
                directory = heading_text.rstrip('/')
                path_stack.append(directory)
                current_file = None  # 디렉토리를 변경하면 현재 파일명 초기화
            else:
                # 파일인 경우
                current_file = heading_text  # 파일명을 현재 파일로 설정
            continue  # 다음 라인으로 이동

    return result

import difflib

def rewrite_codes(files, base_path='.', diff_output_dir=None, proj_dir="project"):
    project_path = os.path.join(base_path, proj_dir)

    # 'project' 폴더가 존재하지 않으면 생성
    if not os.path.isdir(project_path):
        try:
            os.makedirs(project_path, exist_ok=True)
            print(f"{proj_dir} 폴더를 생성했습니다: {project_path}")
        except (IOError, OSError) as e:
            print(f"{proj_dir} 폴더를 생성할 수 없습니다. 오류: {e}")
            return

    base_path = project_path
    print(f"files:\n\n{files}\n\n")
    for file in files:
        normalized_path = os.path.normpath(file['path'])
        base_name = os.path.basename(normalized_path)
        dir_name = os.path.dirname(normalized_path)

        # 파일 경로 생성
        file_path = os.path.join(base_path, dir_name, base_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print(f"{base_name}")
        print(f"file_path: {file_path}")
        print(f"dir_name: {dir_name}")

        new_code_lines = file['code'].splitlines(keepends=True)

        if os.path.exists(file_path):
            # 기존 파일 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_code_lines = f.readlines()

            # Diff 생성
            diff = difflib.unified_diff(
                existing_code_lines, new_code_lines,
                fromfile=f'original/{file["path"]}',
                tofile=f'updated/{file["path"]}',
                lineterm=''
            )
            diff_text = '\n'.join(diff)

            if diff_text:
                # 변경 사항이 있으면 파일 업데이트 및 Diff 출력
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_code_lines)
                print(f"Updated code in {file_path}")

                # Diff 출력
                print(f"Changes in {file_path}:\n{diff_text}\n")

                # Diff를 파일로 저장 (선택 사항)
                if diff_output_dir:
                    diff_file_path = os.path.join(diff_output_dir, f'{file["path"]}.diff')
                    diff_dir = os.path.dirname(diff_file_path)
                    os.makedirs(diff_dir, exist_ok=True)
                    with open(diff_file_path, 'w', encoding='utf-8') as diff_file:
                        diff_file.write(diff_text)
                    print(f"Saved diff to {diff_file_path}")
            else:
                print(f"No changes detected in {file_path}")
        else:
            # 파일 생성
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_code_lines)
            print(f"Created new file {file_path}")

# 메서드 추가

import os
import re

def install_missing_modules(error_message, container):
    # 오류 메시지에서 누락된 모듈 이름 추출

    match = re.search(r"No module named '([^']+)'", error_message)
    if match:
        module_name = match.group(1)
        print(f"Installing missing module: {module_name}")
        
        # 모듈 이름 검증
        if not re.match(r'^[a-zA-Z0-9_\-]+$', module_name):
            print(f"Invalid module name detected: {module_name}")
            return False
        
        # 모듈 설치
        try:
            #subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            output, error_code = DockerToolRepositoryImpl.exec_command(container, f"python -m pip install {module_name}")
            print(f"Successfully installed module: {module_name}")
            if error_code == 0:

                return output
        except error_code as e:
            print(f"Failed to install module {module_name}: {e}")
            return False
    else:
        print("Could not extract module name from error message.")
        return False

def verify_functionality (file_path, file_name, container, env, retries=0, max_retries=3, base_path="project"):
    if retries > max_retries:
        print("Maximum retry limit reached.")
        return "Maximum retry limit reached.", False
    
    potential_path = os.path.join(env.config.directory, base_path, file_path, file_name)
    norm_path= os.path.normpath(potential_path) if os.path.exists(potential_path) else next((os.path.normpath(os.path.join(root, file_name)) for root, _, files in os.walk(os.path.join(env.config.directory, base_path)) if file_name in files), "")
    print(f"\n\nnorm_path:{norm_path}\n\n")
    test_file = os.path.splitext(norm_path.replace("\\", "/"))[0].replace("/", ".")
    print(f"\n\ntest_file: {test_file}\n\n")
    normalized_env_config_directory = re.sub(r"[\\/]", ".", env.config.directory)
    normalized_base_path = re.sub(r"[\\/]", ".", base_path)
    modelservedfile = os.path.splitext(re.sub(r"[\\/]", ".", os.path.join(file_path, file_name)))[0]
    print(f"modelservedfile: {modelservedfile}")
    remaining_path = test_file.replace(normalized_env_config_directory + ".", "", 1)
    remaining_path = remaining_path.replace(normalized_base_path + ".", "", 1)
    remaining_path = remaining_path.replace("." + modelservedfile, "", 1)
    print(f"\n\nremaining_path: {remaining_path}\n\n")
    veiled_path = remaining_path.replace(".", "/")
    print(f"\n\nveiled_path: {veiled_path}\n\n")
    print(f"\n\nTEST FILE PATH!!!!!\n\ncd: {env.config.directory}/{base_path}/{veiled_path}\n\npython-m {modelservedfile}\n\nTEST FILE PATH!!!!!\n\n")# export:export PYTHONPATH=/Warehouse/example/project/계산기_프로젝트 실행: warehouse부터
    try:
        # error_code,is_step_complete = DockerToolRepositoryImpl.exec_command(container, f"/bin/bash -c export PYTHONPATH=/{export_path2}")
        error_code,is_step_complete = DockerToolRepositoryImpl.exec_command(container, f"/bin/bash -c 'cd \"/{env.config.directory}/{base_path}/{veiled_path}\" && python -m {modelservedfile}'")
        # error_code,is_step_complete = DockerToolRepositoryImpl.exec_command(container, f"/bin/bash -c 'cd /{env.config.directory}/{base_path}/{cd_path} && python -m {remaining_path}.{modelservedfile}'")
        # error_code,is_step_complete = DockerToolRepositoryImpl.exec_command(container, f"python -m {test_file}")
        

    except error_code as e:
        is_step_complete = False
        
        # ModuleNotFoundError 처리
        if 'ModuleNotFoundError' in e:
            success = install_missing_modules(e, container)
            if success:
                # 모듈 설치 후 재시도
                return verify_functionality(file_path, file_name, retries=retries+1, max_retries=max_retries)
            else:
                return error_code, is_step_complete
        else:
            # 다른 오류 처리
            return error_code, is_step_complete
    return error_code, is_step_complete

def extract_test_file(seminar_conclusion: str) -> tuple:
    test_file_pattern = re.compile(r"<Test this>([^<]+)<Test this/>")
    lines = seminar_conclusion.strip().splitlines()
    for line in reversed(lines):
        match = test_file_pattern.search(line)
        if match:
            full_path = match.group(1).strip()
            path_parts = full_path.rsplit('/', 1)
            if len(path_parts) == 2:
                return tuple(path_parts)  # (PATH, FILENAME)
            else:
                return (path_parts[0], '')  # FILENAME이 없는 경우 PATH만 반환
    
    # 형식이 맞지 않을 경우 None 반환
    return None

def count_steps(impl_step: str) -> int:
    numbers = re.findall(r'^\s*(\d+)\.', impl_step, re.MULTILINE)
    return len(numbers)


# 메서드 추가 ㅋ
import shutil
def remove_pycache_dirs(env):
    base_path:str = env.config.directory
    if not os.path.isdir(base_path):
        print(f"디렉토리가 존재하지 않습니다: {base_path}")
        return

    for root, dirs, files in os.walk(base_path, topdown=False):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"삭제됨: {dir_path}")
                except Exception as e:
                    print(f"삭제 실패: {dir_path}. 오류: {e}")

from typing import Tuple, List

def validate_response_format(response_text: str) -> Tuple[str, bool]:
    lines = response_text.strip().split('\n')
    if lines and lines[0].strip() and not lines[0].strip().startswith('#'): 
        return ("미사여구 없이 반환 형식에 따라 작성해주세요. ``` ``` 블록은 자료의 스켈레톤 코드처럼, 파일 코드와 docstring을 적은 내용에 사용해야 합니다..", False)
    header_pattern = re.compile(r'^(#+)\s+(.+)/\s*$')
    file_pattern = re.compile(r'^(#+)\s+([\w/]+\.py)\s*$')
    test_tag_pattern = re.compile(r'<Test this>([\w/]+\.py)<Test this/>')
    
    headers = []
    project_files = []
    current_path = []
    
    for line in lines:
        header_match = header_pattern.match(line)
        file_match = file_pattern.match(line)
        
        if header_match:
            num_hashes = len(header_match.group(1))
            dir_name = header_match.group(2).rstrip('/')
            headers.append((num_hashes, dir_name))
    
    if not headers:
        return ("#으로 레벨을 구분하여 표현된 프로젝트 디렉토리가 없습니다.", False)
    
    min_hash = min(header[0] for header in headers)
    top_level_dirs = [header for header in headers if header[0] == min_hash]
    
    if len(top_level_dirs) != 1:
        return ("코드 작성은 최상단 디렉토리 내에 해야 합니다.", False)
    
    top_level_dir_name = top_level_dirs[0][1]
    
    # 헤더 정보를 이용하여 디렉토리 구조 생성
    current_path = []
    dir_stack = []
    header_index = 0  # 헤더 인덱스 초기화
    
    for line in lines:
        header_match = header_pattern.match(line)
        file_match = file_pattern.match(line)
        
        if header_match:
            num_hashes = len(header_match.group(1))
            dir_name = header_match.group(2).rstrip('/')
            expected_depth = num_hashes - min_hash
            while len(dir_stack) > expected_depth:
                dir_stack.pop()
            dir_stack.append(dir_name)
            current_path = dir_stack.copy()
        elif file_match:
            num_hashes = len(file_match.group(1))
            file_name = file_match.group(2)
            expected_depth = num_hashes - min_hash
            file_dir = dir_stack[:expected_depth]
            file_path = '/'.join(file_dir) + '/' + file_name
            project_files.append(file_path)
    
    # 최상위 디렉토리를 제거하여 상대 경로로 변환
    project_files = [fp[len(top_level_dir_name)+1:] if fp.startswith(top_level_dir_name + '/') else fp for fp in project_files]
    print(f"project_files: {project_files}")
    # 테스트 파일 추출
    test_files = test_tag_pattern.findall(response_text)
    print(f"test_files: {test_files}")
    if not test_files:
        return ("에러: '<Test this>PATH/FILENAME<Test this/>' 형식의 태그가 작성되지 않았습니다.", False)
    
    # 테스트 파일이 프로젝트 내에 존재하는지 확인
    missing_files = [file for file in test_files if file not in project_files]
    
    if missing_files:
        missing_str = ', '.join(missing_files)
        return (f"테스트 파일은 프로젝트 구조 내에 존재 해야 합니다.\
이전에 작성된 내용이 표현하는 level 구조가 전달된 프로젝트 구조와 일치하지 않을 수 있습니다. ", False)
    
    return ("형식이 올바릅니다.", True)