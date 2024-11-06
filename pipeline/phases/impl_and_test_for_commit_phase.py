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
현재 작업과 상황을 참고하여 반환 형식에 맞게 답변을 작성하세요.

[자료]

현재까지 작성된 스켈레톤 코드: (#으로 트리 구조가 구분되어 있습니다.)

{skeleton_code}
전체 구현 단계:
{impl_step}
[상황]
현재 우리는 전체 진행 구현 단계에 대해 한 단계씩 구현하면서, 테스트가 통과할 때까지 코드를 작성 또는 수정하고, 하나의 단계가 완료되면 다음 단계로 진행하면서 전체 구현단계가 완료되도록 작업을 진행중입니다.

[지시]
1. 현재 진행 중인 단계에 해당하는 작업을 진행하세요. 작성된 스켈레톤 코드에서 내용을 추가 또는 수정하면 됩니다.
   **추가/수정 사항을 전체 코드와 함께 반환해야 합니다.**
2. 현재 단계의 파일 내 기능 구현과 동시에 테스트 코드 구현도 함께 진행하세요.
3. 테스트 코드는 test 폴더 내에 작성하고, 주요 테스트 시나리오와 메인가드 블록을 포함해야 합니다.
4. 기능 구현과 테스트 코드 작성 시 완전하게 구현해야 합니다.(**placeholder나 pass는 제한됩니다.**)
5. 각 주요 로직 구문에 대해 주석을 추가하여 해당 코드의 목적을 설명하세요.
6. 코드 작성은 반환 형식에 따라 #을 사용하여 트리 구조가 구분 되도록 하고, 최상단 디렉토리부터 작성해야 합니다.
7. 답변 마지막 줄에 테스트할 메서드가 포함된 파일을 형식에 따라 적으세요.
8. 협업자 모두가 따를 수 있도록 **반환 형식을 반드시 준수**하세요.


[작업 현황]
• 현재 "{current_step}단계"의 {code_error_resolve_attempts}번째 코드 작성 시도 중입니다.
    구현 단계에 해당하는 프로젝트 코드와 테스트 코드 작성을 진행하세요.
[조건]
• 시스템 메시지에 테스트 실패(FAILED)가 있는경우
    - 테스트가 통과하도록 프로젝트 코드의 import문, 변수, 구문, 예외 처리, 로직, 타입 또는 반환값 또는 테스트 코드의 기대값 등을 수정하세요.
• 시스템 메시지에 반환형식 위반이 있는경우
    - 반환 형식을 준수하여 답변하세요.

"{current_step}단계 시스템 메시지:
"{error_code}"


반환 형식:
PATH/FILENAME
```
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
        
        abs_path = os.path.abspath("pipeline/utils")
        if build_docker_image(path=abs_path, tag="using_xvfb:v1"):
            print("이미지 빌드 성공. 다음 작업을 진행합니다.")
        else:
            print("이미지 빌드에 실패했습니다.")

        container = DockerToolRepositoryImpl.get_container(
                                                            "si_foIIow_test",
                                                            volume=env.config.directory,
                                                            image_name="using_xvfb:v1",
                                                            )
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
                    env.states.error_code = f"이전 응답에서 반환 형식을 위반하여 테스트 실행 전에 재응답을 요청하였습니다.:\n{error_message_in_validate}"
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
                if is_step_complete != True:
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

                if is_step_complete == True:
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
    Parses the input string representing the project structure and extracts
    the file paths and code blocks.

    Args:
        input_str (str): The project structure string to parse.

    Returns:
        List[Dict[str, str]]: A list of dictionaries with 'path', 'code', and 'type' keys.
    """
    path_stack = []  # Stack to keep track of current path
    result = []      # List to store the final result
    in_code_block = False
    code_block_lang = ''
    code_lines = []
    current_file = None

    # Regular expressions to match headers and code blocks
    header_pattern = re.compile(r'^(#{1,6})\s+(.*)')
    code_block_start_pattern = re.compile(r'^```(\w+)?')
    code_block_end_pattern = re.compile(r'^```$')

    lines = input_str.splitlines()

    # Find the minimum header level to determine the base level
    header_levels = []
    for line in lines:
        header_match = header_pattern.match(line)
        if header_match:
            hashes, _ = header_match.groups()
            level = len(hashes)
            header_levels.append(level)

    if not header_levels:
        base_level = 1  # Default base level if no headers are found
    else:
        base_level = min(header_levels)

    for line in lines:
        line = line.rstrip()
        # Code block start
        if not in_code_block and code_block_start_pattern.match(line):
            in_code_block = True
            code_block_lang = code_block_start_pattern.match(line).group(1) or ''
            code_lines = []
            continue

        # Code block end
        if in_code_block and code_block_end_pattern.match(line):
            in_code_block = False
            code = '\n'.join(code_lines).strip()
            if current_file:
                full_path = '/'.join(path_stack + [current_file])
                result.append({
                    'path': full_path,
                    'code': code,
                    'type': 'file'
                })
                current_file = None
            else:
                # If there's code but no current file, associate it with the current directory
                full_path = '/'.join(path_stack)
                result.append({
                    'path': full_path,
                    'code': code,
                    'type': 'directory'
                })
            continue

        # Inside code block
        if in_code_block:
            code_lines.append(line)
            continue

        # Header line
        header_match = header_pattern.match(line)
        if header_match:
            hashes, heading_text = header_match.groups()
            level = len(hashes)
            depth = level - base_level

            # Adjust the path stack to match the current depth
            if depth < 0:
                path_stack = []
            else:
                while len(path_stack) > depth:
                    path_stack.pop()

            # Split the heading text from any description after a colon
            heading_parts = heading_text.split(':', 1)
            heading_name = heading_parts[0].strip()

            if heading_name.endswith('/'):
                # It's a directory
                directory = heading_name.rstrip('/')
                path_stack.append(directory)
                result.append({
                    'path': '/'.join(path_stack),
                    'code': '',
                    'type': 'directory'
                })
                current_file = None
            else:
                # It's a file
                current_file = heading_name
            continue

    return result

import difflib

def rewrite_codes(files, base_path='.', diff_output_dir=None, proj_dir="project"):
    project_path = os.path.join(base_path, proj_dir)

    # Ensure the 'project' folder exists
    if not os.path.isdir(project_path):
        try:
            os.makedirs(project_path, exist_ok=True)
            print(f"{proj_dir} folder created at: {project_path}")
        except (IOError, OSError) as e:
            print(f"Cannot create {proj_dir} folder. Error: {e}")
            return

    base_path = project_path
    print(f"files:\n\n{files}\n\n")
    for file in files:
        normalized_path = os.path.normpath(file['path'])
        file_path = os.path.join(base_path, normalized_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print(f"Processing: {normalized_path}")
        print(f"file_path: {file_path}")

        if file['type'] == 'directory':
            # Create the directory if it doesn't exist
            os.makedirs(file_path, exist_ok=True)
            print(f"Created directory {file_path}")
            continue

        new_code_lines = file['code'].splitlines(keepends=True)

        if os.path.exists(file_path):
            # Read the existing file
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_code_lines = f.readlines()

            # Create a diff
            diff = difflib.unified_diff(
                existing_code_lines, new_code_lines,
                fromfile=f'original/{file["path"]}',
                tofile=f'updated/{file["path"]}',
                lineterm=''
            )
            diff_text = '\n'.join(diff)

            if diff_text:
                # Update the file if there are changes
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_code_lines)
                print(f"Updated code in {file_path}")

                # Output the diff
                print(f"Changes in {file_path}:\n{diff_text}\n")

                # Optionally save the diff to a file
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
            # Create a new file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_code_lines)
            print(f"Created new file {file_path}")

# 메서드 추가

def install_missing_modules(error_message, container):
    import re
    import docker

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
            # Docker SDK를 사용하여 컨테이너 내에서 pip install 실행
            install_command = f"python -m pip install {module_name}"
            exec_install = container.exec_run(install_command)
            install_output = exec_install.output.decode('utf-8', errors='ignore')
            install_exit_code = exec_install.exit_code

            if install_exit_code == 0:
                print(f"Successfully installed module: {module_name}")
                return install_output, True
            else:
                print(f"Failed to install module {module_name}. Output:\n{install_output}")
                return install_output, False

        except Exception as e:
            print(f"Exception occurred while installing module {module_name}: {e}")
            return e, False
    else:
        print("Could not extract module name from error message.")
        return "Could not extract module name from error message.", False

import os
import re
import time
import threading
import docker

def verify_functionality(file_path, file_name, container, env, retries=0, max_retries=3, base_path="project"):
    if retries > max_retries:
        print("Maximum retry limit reached.")
        return "Maximum retry limit reached.", False

    # 기존 경로 설정 로직
    potential_path = os.path.join(env.config.directory, base_path, file_path, file_name)
    norm_path = os.path.normpath(potential_path) if os.path.exists(potential_path) else next(
        (os.path.normpath(os.path.join(root, file_name)) for root, _, files in os.walk(os.path.join(env.config.directory, base_path)) if file_name in files), "")
    test_file = os.path.splitext(norm_path.replace("\\", "/"))[0].replace("/", ".")
    normalized_env_config_directory = re.sub(r"[\\/]", ".", env.config.directory)
    normalized_base_path = re.sub(r"[\\/]", ".", base_path)
    modelservedfile = os.path.splitext(re.sub(r"[\\/]", ".", os.path.join(file_path, file_name)))[0]
    remaining_path = test_file.replace(normalized_env_config_directory + ".", "", 1)
    remaining_path = remaining_path.replace(normalized_base_path + ".", "", 1)
    remaining_path = remaining_path.replace("." + modelservedfile, "", 1)
    veiled_path = remaining_path.replace(".", "/")
    print(f"test_file:{test_file}")
    print(f"\n\nremaining_path: {remaining_path}\n\n")
    print(f"modelservedfile:{modelservedfile}")
    print(f"veild_path:{veiled_path}")
    print(f"cd:{env.config.directory}/{base_path}/{veiled_path}")
    print(f"python -m {modelservedfile}")

    # command = f"/bin/bash -c 'cd \"{env.config.directory}/{base_path}/{veiled_path}\" && python -m {modelservedfile}'"
    timeout_duration = 10 # TODO: 추후 상위에서 설정할 수 있으면 좋을듯    
    command = f"timeout {timeout_duration}s bash -c 'cd .. && cd \"{env.config.directory}/{base_path}/{veiled_path}\" && xvfb-run -a -s \"-screen 0 1024x768x24\" python -m {modelservedfile}'"


    # Docker SDK를 사용하여 컨테이너에 연결
    client = docker.from_env()

    # 컨테이너 객체 확인
    if isinstance(container, str):
        container = client.containers.get(container)

    try:
        # 명령을 비동기적으로 실행하고 출력 스트림을 캡처
        exec_instance = client.api.exec_create(container.id, command, tty=False)
        exec_id = exec_instance['Id']
        output_generator = client.api.exec_start(exec_id, detach=False, tty=False, stream=True)
        print(f"Command started with exec_id: {exec_id}")

        # 타임아웃 설정
        timeout = 10  # 원하는 타임아웃 시간(초)
        start_time = time.time()

        output_lines = []

        def read_output():
            nonlocal output_generator, output_lines
            try:
                for chunk in output_generator:
                    decoded_chunk = chunk.decode('utf-8', errors='ignore')
                    output_lines.append(decoded_chunk)
                    print(decoded_chunk, end='')
            except Exception as e:
                print(f"Output reading error: {e}")

        # 출력 읽기 스레드 시작
        output_thread = threading.Thread(target=read_output)
        output_thread.start()

        # 실행 상태를 모니터링하는 함수
        def monitor_exec():
            nonlocal exec_id, container
            while True:
                exec_info = client.api.exec_inspect(exec_id)
                if not exec_info['Running']:
                    print("Command completed.")
                    break
                if time.time() - start_time > timeout:
                    print("Timeout reached. Sending SIGINT to the process.")
                    # 프로세스에 SIGINT 신호 보내기
                    pid = exec_info.get('Pid')
                    if pid:
                        container.exec_run(f"kill -2 {pid}", detach=True, privileged=True)
                    else:
                        print("Unable to get PID of the process.")
                    break
                time.sleep(1)

        # 모니터링 스레드 시작
        monitor_thread = threading.Thread(target=monitor_exec)
        monitor_thread.start()

        # 스레드들이 종료되길 기다림
        output_thread.join(timeout + 5)
        monitor_thread.join(timeout + 5)

        # 실행 결과 확인
        exec_info = client.api.exec_inspect(exec_id)
        exit_code = exec_info['ExitCode']
        is_step_complete = (exit_code == 0)

        # 출력 내용을 결합
        output = ''.join(output_lines)
        
        if exit_code == 124:
            error_code = f"Timeout occurred after {timeout_duration} seconds."
            is_step_complete = False
            return error_code, is_step_complete

        
        if not is_step_complete:
            error_code = f"Exit code: {exit_code}\nOutput:\n{output}"

            # ModuleNotFoundError 처리
            if 'ModuleNotFoundError' in output and retries < max_retries:
                install_output, success = install_missing_modules(output, container)
                if success:
                    # 모듈 설치 후 재시도
                    return verify_functionality(file_path, file_name, container, env, retries=retries, max_retries=max_retries)
                else:
                    print("Module installation failed or import error.")
                    return install_output, False
            else:
                # 기타 오류 처리
                return error_code, False
        else:
            error_code = f"Exit code: {exit_code}\nOutput:\n{output}"

    except Exception as e:
        is_step_complete = False
        error_code = str(e)
        # 예외 발생 시 처리
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
        return ("반환 형식에 따라 작성해주세요.```plaintext ```로 전체를 감싸면 반환 형식 위반입니다. ``` ``` 블록은 자료의 스켈레톤 코드처럼, 파일명 아래 파일 코드와 docstring을 적은 내용에만 사용해야 합니다.", False)
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
        return ("#으로 프로젝트 트리구조를 구분하여 작성되지 않았습니다.", False)
    
    min_hash = min(header[0] for header in headers)
    top_level_dirs = [header for header in headers if header[0] == min_hash]
    
    if len(top_level_dirs) != 1:
        return ("최상단 디렉토리 부터 #으로 트리 구조가 구분되도록 표현해야 합니다.", False)
    
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
        return ("'<Test this>PATH/FILENAME<Test this/>' 형식의 태그가 작성되지 않았습니다.", False)
    
    # 테스트 파일이 프로젝트 내에 존재하는지 확인
    missing_files = [file for file in test_files if file not in project_files]
    
    if missing_files:
        missing_str = ', '.join(missing_files)
        return (f"테스트 파일은 프로젝트 구조 내에 존재 해야 합니다.\
이전에 작성 되어 있던 내용과 구조가 당신이 제출한 프로젝트 구조와 일치하지 않을 수 있습니다.", False)
    
    return ("형식이 올바릅니다.", True)

import docker

def build_docker_image(path: str, tag: str) -> bool:
    """
    지정된 경로의 Dockerfile을 기반으로 Docker 이미지를 빌드합니다.
    
    Parameters:
        path (str): Dockerfile이 위치한 디렉토리 경로.
        tag (str): 빌드된 이미지에 할당할 태그.
    
    Returns:
        bool: 빌드 성공 여부 (성공하면 True, 실패하면 False).
    """
    client = docker.from_env()
    try:
        client.images.build(path=path, tag=tag, rm=True)
        print(f"Docker 이미지 '{tag}'가 성공적으로 빌드되었습니다.")
        return True
    except docker.errors.BuildError as e:
        print(f"이미지 빌드 실패: {e}")
        return False
    except docker.errors.APIError as e:
        print(f"Docker API 오류: {e}")
        return False
