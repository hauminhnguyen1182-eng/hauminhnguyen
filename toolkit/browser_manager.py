from playwright.async_api import async_playwright
from browser_use import Agent
import asyncio

class BrowserManager:
    def __init__(self):
        self.browser = None
        self.page = None

    async def start(self, headless=True):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()
        print("✅ Browser started")

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("✅ Browser stopped")

    async def goto(self, url):
        await self.page.goto(url, wait_until="domcontentloaded")
        title = await self.page.title()
        print(f"📄 Loaded: {title}")
        return title

    async def get_text(self):
        return await self.page.inner_text("body")

    async def search_google(self, query):
        await self.page.goto(f"https://www.google.com/search?q={query}", wait_until="networkidle")
        await self.page.wait_for_timeout(2000)

        data = []
        # Try multiple selectors
        for selector in ["div.g", "div[data-sokoban-container]", "div.tF2Cxc"]:
            results = await self.page.query_selector_all(selector)
            if results:
                break

        for r in results[:10]:
            try:
                title_el = await r.query_selector("h3")
                link_el = await r.query_selector("a")
                if title_el and link_el:
                    title = await title_el.inner_text()
                    url = await link_el.get_attribute("href")
                    if url and url.startswith("http"):
                        data.append({"title": title, "url": url})
            except:
                continue
        return data

    async def screenshot(self, path="screenshot.png"):
        await self.page.screenshot(path=path)
        print(f"📸 Screenshot saved: {path}")

    async def browser_use_task(self, task, api_key=None):
        agent = Agent(
            task=task,
            llm=None,
            browser=self.browser
        )
        result = await agent.run()
        return result