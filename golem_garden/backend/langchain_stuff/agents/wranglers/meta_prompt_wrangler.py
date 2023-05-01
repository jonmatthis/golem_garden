import asyncio
from copy import deepcopy

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.memory import ConversationBufferWindowMemory

from golem_garden.backend.langchain_stuff.agents.get_available_agents import get_available_agents, get_agent_config
from golem_garden.backend.langchain_stuff.agents.llm_chain_builder import LLMChainBuilder


def initialize_meta_chain():
    meta_template = """
    Assistant has just had the below interactions with a User. Assistant followed their "Instructions" closely. Your job is to critique the Assistant's performance and then revise the Instructions so that Assistant would quickly and correctly respond in the future.

    ####

    {chat_history}

    ####

    Please reflect on these interactions.

    You should first critique Assistant's performance. What could Assistant have done better? What should the Assistant remember about this user? Are there things this user always wants? Indicate this with "Critique: ...".

    You should next revise the Instructions so that Assistant would quickly and correctly respond in the future. Assistant's goal is to satisfy the user in as few interactions as possible. Assistant will only see the new Instructions, not the interaction history, so anything important must be summarized in the Instructions. Don't forget any important details in the current Instructions! Indicate the new Instructions by "Instructions: ...".
    """

    meta_prompt = PromptTemplate(
        input_variables=["chat_history"],
        template=meta_template
    )

    meta_chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=meta_prompt,
        verbose=True,
    )
    return meta_chain





def get_new_instructions(meta_output):
    delimiter = 'Instructions: '
    new_instructions = meta_output[meta_output.find(delimiter) + len(delimiter):]
    return new_instructions
async def meta_prompt_main(task:str, max_inner_loops=3, max_meta_iterations=5):

    meta_prompt_config = get_agent_config(agent_name = "meta_prompt")
    instruction_follower_config = get_agent_config(agent_name="instruction_follower")

    failed_phrase = 'fail'
    success_phrase = 'succeed'
    key_phrases = [success_phrase, failed_phrase]

    instructions = 'None'
    for iteration_number in range(max_meta_iterations):
        print(f'[Episode {iteration_number + 1}/{max_meta_iterations}]')
        instruction_follower = LLMChainBuilder(config=instruction_follower_config)
        instruction_follower_output = instruction_follower.intake_message(instructions=task)
        for j in range(max_inner_loops):
            print(f'(Inner loop {j + 1}/{max_inner_loops})\n---\n')
            print(f'Assistant: {instruction_follower_output}')
            print(f'Human ("success" or "fail" to indicate bot performance): ')
            human_input = input()
            if any(phrase in human_input.lower() for phrase in key_phrases):
                break
            instruction_follower_output = instruction_follower.intake_message(human_input=human_input)

        if success_phrase in human_input.lower():
            print(f'You succeeded! Thanks for playing!')
            return

        meta_prompt_llm_chain = LLMChainBuilder(config=meta_prompt_config)
        meta_output = meta_prompt_llm_chain.intake_message(chat_history=instruction_follower.get_chat_history())
        print(f'Feedback from `meta_prompt_chain`: {meta_output}')
        instructions = get_new_instructions(meta_output)
        print(f'New Instructions: {instructions}')
        print('\n' + '#' * 80 + '\n')
    print(f'You failed! Thanks for playing!')


if __name__ == "__main__":
    asyncio.run(meta_prompt_main(task="help me plan an online course"))
