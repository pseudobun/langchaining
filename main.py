from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search import TavilySearchResults
from web3_tools import get_ERC20_balance, get_ETH_balance
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from utils_tools import send_to_discord, get_todays_date

load_dotenv()


def main():
    memory = MemorySaver()
    search = TavilySearchResults(max_results=5)
    tools = [send_to_discord, search,
             get_ERC20_balance, get_ETH_balance, get_todays_date]
    llm = init_chat_model("gpt-4.1", model_provider="openai")
    llm_with_tools = llm.bind_tools(tools)
    prompt = """
    Find or use (if you already know them) the contract addresses for USDC, EURC, and
    Ethena sUSDe (0x9d39a5de30e57443bff2a8307a4256c8797a3497) -
    perform each search separately
    on Ethereum network and get balances for those tokens and
    ETH for eth:0x1Db51d6F3349Db0846496db5C8A588b44fF3f09C.

    Send those balances (ignore zero or small ones) to Discord then as a daily
    summary along with total value
    in USD and EUR.

    Along with the balances, please also add a short summary of the market for today
    and what caused the price changes if any bigger events happened.

    Make sure to nicely construct the message, use the emojis, make the formatting readable
    and nice to be sent to Discord.

    Use the same format as yesterday, same sections, same style and same emoji usage.
    """

    langchainer = create_react_agent(
        llm_with_tools, tools, checkpointer=memory)
    config = {"configurable": {"thread_id": "langchainer-0"}}
    for step in langchainer.stream(
        {"messages": [HumanMessage(content=prompt)]},
        stream_mode="values",
        config=config,
    ):
        step["messages"][-1].pretty_print()


if __name__ == "__main__":
    main()
