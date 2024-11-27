from dotenv import load_dotenv
from typing import Tuple
# from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama


from third_party.linkedin_conn import scrape_linkedin_profile
from agents.linkedin_lookup_agent import linkedin_lookup_agent
from third_party.twitter_conn import scrape_user_tweets
from output_parsers import summary_parser,Summary


# information = """
# Dame Agatha Mary Clarissa Christie, Lady Mallowan, DBE (née Miller; 15 September 1890 – 12 January 1976) was an English writer known for her 66 detective novels and 14 short story collections, particularly those revolving around fictional detectives Hercule Poirot and Miss Marple. She also wrote the world's longest-running play, the murder mystery The Mousetrap, which has been performed in the West End of London since 1952. A writer during the "Golden Age of Detective Fiction", Christie has been called the "Queen of Crime"—a moniker which is now trademarked by her estate—or the "Queen of Mystery".[1][2] She also wrote six novels under the pseudonym Mary Westmacott. In 1971, she was made a Dame (DBE) by Queen Elizabeth II for her contributions to literature. Guinness World Records lists Christie as the best-selling fiction writer of all time, her novels having sold more than two billion copies.[2]
#
# Christie was born into a wealthy upper-middle-class family in Torquay, Devon, and was largely home-schooled. She was initially an unsuccessful writer with six consecutive rejections, but this changed in 1920 when The Mysterious Affair at Styles, featuring detective Hercule Poirot, was published. Her first husband was Archibald Christie; they married in 1914 and had one child before divorcing in 1928. Following the breakdown of her marriage and the death of her mother in 1926, she made international headlines by going missing for eleven days. During both World Wars, she served in hospital dispensaries, acquiring a thorough knowledge of the poisons that featured in many of her novels, short stories, and plays. Following her marriage to archaeologist Max Mallowan in 1930, she spent several months each year on digs in the Middle East and used her first-hand knowledge of this profession in her fiction.
#
# According to UNESCO's Index Translationum, she remains the most-translated individual author.[3] Her novel And Then There Were None is one of the top-selling books of all time, with approximately 100 million copies sold. Christie's stage play The Mousetrap holds the world record for the longest initial run. It opened at the Ambassadors Theatre in the West End on 25 November 1952, and by 2018 there had been more than 27,500 performances. The play was temporarily closed in 2020 because of COVID-19 lockdowns in London before it reopened in 2021.
#
# In 1955, Christie was the first recipient of the Mystery Writers of America's Grand Master Award. Later that year, Witness for the Prosecution received an Edgar Award for best play. In 2013, she was voted the best crime writer and The Murder of Roger Ackroyd the best crime novel ever by 600 professional novelists of the Crime Writers' Association. In 2015, And Then There Were None was named the "World's Favourite Christie" in a vote sponsored by the author's estate.[4] Many of Christie's books and short stories have been adapted for television, radio, video games, and graphic novels. More than 30 feature films are based on her work.
# """

# information = json.load(open("third_party/cleaned.json"))
# print(information)

def ice_break_with(name: str) -> Tuple[Summary,str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    # twitter_username = twitter_lookup_agent(name=name)
    twitter_data = scrape_user_tweets('', mock=True)

    summary_template = """
    given the information {information} about a person, {twitter_posts} I want you to create
    1. a short summary
    2. two interesting facts about them
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        partial_variables={"format_instructions": summary_parser.get_format_instructions()},
        template=summary_template
    )
    # summary_prompt_template = PromptTemplate.from_template(summary_template)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = summary_prompt_template | llm | summary_parser
    linkedin_data = scrape_linkedin_profile("", True)
    res:Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": twitter_data})
    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    print("Hello Langchain, Ice Breaker!!!")
    ice_break_with("Eden Marco")
    # llm = ChatOpenAI(temperature=0,model_name='gpt-4o-mini')
    # llm = ChatOllama(model="llama3.2", temperature=0)

# from openai import OpenAI
# client = OpenAI()
# completion = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "user", "content": "write a haiku about ai"}
#     ]
# )
