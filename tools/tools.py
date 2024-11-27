from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()

def get_profile_url_tavily(name:str):
    """Searches for LinkedIn or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res

if __name__=="__main__":
    print(get_profile_url_tavily("Eden Marco"))