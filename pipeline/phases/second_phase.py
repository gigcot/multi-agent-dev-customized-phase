from pipeline.states.phase_states import ExamplePhaseStates
from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl


@PhaseRegistry.register()
class SecondPhase(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt: str = "Let's discuss about LLM",
        assistant_role_name: str = "assistant",
        assistant_role_prompt: str = "You are a helpful {assistant_role}",
        user_role_name: str = "user",
        user_role_prompt: str = "You are discussing about {task} with {assistant_role}",
        chat_turn_limit: int = 2,
        temperature=0.5,
        top_p=0.5,
        states=ExamplePhaseStates(),
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
        pass

    def update_env_states(self, env):
        return env
