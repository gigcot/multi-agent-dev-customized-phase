from pipeline.phases import *
from pipeline.states.env_states import ExampleEnvStates
from made.chat_chain.service.chat_chain_service_impl import ChatChainServiceImpl
from made.phase import import_all_modules
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("api_key")
import_all_modules("pipeline.phases")


if __name__ == "__main__":
    chain = ChatChainServiceImpl(
        task_prompt="python 언어로 gui 되는 계산기 만들어줘.",
        directory="Warehouse/example",
        base_url=None,
        model="",
        phases=["DemandAnalysis","SetupInitialSturcture","WritingSkeletonCode","ImplementationSequencing","ImplAndTestForCommit"],
        env_states=ExampleEnvStates(),
        api_key=api_key,
        max_tokens=20000,
    )
    chain.run()


