#
# Description: Source code for the AI Agent that powers Site Sense AI
# Author: Alexander Powell
# Version: v1.0
# Dependencies: langchain, dotenv, typing, os, whois_lookup, sitesense_ai_memory
#

from dotenv import load_dotenv, find_dotenv
from typing import Any, Dict
from .sitesense_ai_memory import SiteSenseAIMemory
from .whois_lookup import domain_search

from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache

import os


class SiteSenseAI:
    load_dotenv(find_dotenv(), override=True)
    set_llm_cache(SQLiteCache(database_path=os.environ["DB_PATH"]))

    def __init__(self, *, model="", temp=0.5):
        self.agent_emily: ChatOpenAI = ChatOpenAI(model=model, temperature=temp)  # NOQA
        self.chat_memory: SiteSenseAIMemory = SiteSenseAIMemory()
        self.agent_executor: AgentExecutor

    def _get_prompt_template(self) -> PromptTemplate:  # NOQA
        """
        Gets the ReAct prompt template from a file and creates
        a prompt template for the AI Agent.

        :return prompt:
        """

        with open(os.environ["TEMPLATE_PATH"]) as template_file:
            template = template_file.read()
            template_file.close()

        prompt = PromptTemplate(
            input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools', 'memory_context'],
            template=template
        )

        return prompt

    def _get_whois_tool(self, domain_name: str) -> Any:  # NOQA
        """
        Gets the results of a WHOIS lookup from an external function.

        :param domain_name:
        :return whois_lookup:
        """
        return domain_search(domain_name)

    def _get_memory(self):
        """
        Gets the chat memory.

        :return:
        """
        return self.chat_memory

    def _update_memory(self, context: str):
        """
        Updates the chat memory.

        :param context:
        :return:
        """
        self.chat_memory.append(context)

    def _create_agent(self):
        """
        Creates the ReAct agent and implements all the
        tools the agent can use.

        :return:
        """

        prompt = self._get_prompt_template()

        domain_tool = Tool(
            name="WHOIS",
            func=self._get_whois_tool,
            description="Find the availability of a domain name"
        )

        tools = [domain_tool]

        agent = create_react_agent(self.agent_emily, tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )


    def engage(self, user_input: str) -> Dict[str, Any]:
        """
        Entry point to engage with the AI Agent and ask it questions.

        :param user_input:
        :return ai_response:
        """

        self._create_agent()
        memory_context = self.chat_memory.get_chat_history()

        # Get the response from the ReAct Agent
        ai_response = self.agent_executor.invoke({
            "input": user_input,
            "memory_context": memory_context,
        })

        # Create the context for the memory and update the chat memory
        context: str = f"Human: {user_input}\nAI: {ai_response}"
        self.chat_memory.append(context)

        return ai_response
