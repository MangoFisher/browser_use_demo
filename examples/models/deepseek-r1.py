import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig

# dotenv
load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key:
	raise ValueError('DEEPSEEK_API_KEY is not set')


async def run_search():
	# 创建浏览器配置
	browser_config = BrowserConfig(
		cdp_url="http://localhost:9222",  # 使用 CDP URL 连接到已运行的 Chrome
		disable_security=True  # 添加这个选项可能有助于解决一些连接问题
	)
	browser = Browser(browser_config)

	agent = Agent(
		#task=('go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result'),
		task=('打开https://www.ctrip.com/, 打开成功后，关闭这个标签页'),
		llm=ChatOpenAI(
			base_url='https://api.deepseek.com/v1',
			model='deepseek-reasoner',
			api_key=SecretStr(api_key),
		),
		use_vision=False,
		max_failures=2,
		max_actions_per_step=1,
		browser=browser,
	)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(run_search())
