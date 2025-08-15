import os
from googlesearch import search
from eigenlib.utils.parallel_utils import ParallelUtilsClass
from openai import AzureOpenAI
import asyncio
import sys
from crawl4ai import AsyncWebCrawler

class IntelligentWebSearch:
    def __init__(self):
        self.client = AzureOpenAI(azure_endpoint=os.environ["OAI_SUBS_1"], api_key=os.environ["OAI_API_KEY_1"], api_version=os.environ["OAI_API_VERSION_1"],)

    def run(self, query, num_results=10, summarize=True):
        self.summarize = summarize
        self.model = "gpt-5-nano"
        urls = list(search(query, num_results=num_results))
        result = ParallelUtilsClass().run_in_parallel(self._url_to_summary, {'query':query}, {'url': urls}, n_threads=num_results, use_processes=False)
        result = '\n'.join(result)
        if self.summarize:
            history = [{'role': 'system', 'content': f'Extract the relevant information to the following query using the source: "{query}". \nFocus on the relevant information and include the sources (url and citation.).'}, {'role': 'user', 'content': 'Source of information: ' + result}]
            answer = self.client.chat.completions.create(model=self.model, messages=history, temperature=1).choices[0].message.content
        else:
            answer = result
        return answer

    def _url_to_summary(self, url, query):
        try:
            content = self._fast_browser_engine(url)#self._browser_engine(url)
        except Exception as e:
            return url + '->' + str(e)
        if self.summarize:
            history = [{'role': 'system', 'content': f'Given the following query: "{query}". Extract from the source a very synthetic and compact extract of the relevant information to answer the query. Be very concise.'}, {'role': 'user', 'content': 'Source of information: ' + str(content)}]
            answer = self.client.chat.completions.create(model=self.model, messages=history, temperature=1).choices[0].message.content
        else:
            answer = content
        return 'Information from source ' + url + ' ->' + str(answer)

    def _browser_engine(self, url):
        if sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        async def _crawl():
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url)
                return result.markdown
        return asyncio.run(_crawl())

    def _fast_browser_engine(self, url):
        from playwright.sync_api import sync_playwright
        if sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            content = page.evaluate("document.documentElement.innerText")
            browser.close()
            return content

