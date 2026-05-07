from langchain_aws import ChatBedrock
from dotenv import load_dotenv

load_dotenv()

# Claude Haiku — fast and cheap, great for development
llm = ChatBedrock(
    model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="us-east-2",
    model_kwargs={"max_tokens": 2048}
)