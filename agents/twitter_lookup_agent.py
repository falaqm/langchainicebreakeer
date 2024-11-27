from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from tools.tools import get_profile_url_tavily



def twitter_lookup_agent(name: str) -> str:
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    template = """Given the full name {name_of_person}, I want you to get me a link to
                their Twitter  or X profile page, and from it extract their username.In your final answer only the persons username"""

    # prompt_template = PromptTemplate.from_template(template=template)
    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])
    tools_for_agent = [
        Tool(
            name="Crawl Google for Twitter  or X profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get Twitter or X Page URL"
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)})
    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    twitter_url = twitter_lookup_agent(name="Elon Musk")
    print(twitter_url)