from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from app.core.config import settings

class StealthBrowser:
    async def run_task(self, proxy_url: str, user_agent: str, task_url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
            context = await browser.new_context(
                user_agent=user_agent,
                proxy={"server": proxy_url or settings.BRIGHTDATA_PROXY_URL},
                viewport={"width": 1920, "height": 1080}
            )
            await stealth_async(context)
            page = await context.new_page()
            await page.goto(task_url)
            # Perform actions, e.g., fill forms, solve CAPTCHA via CapSolver API
            # Example CAPTCHA integration:
            # response = requests.post("https://api.capsolver.com/createTask", json={...})
            # Then page.solve_captcha(response)
            await browser.close()