import asyncio
import requests
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from app.core.config import settings
from app.core.exceptions import CaptchaSolveError
from app.core.humanizer import Humanizer

class StealthBrowser:
    def __init__(self):
        self.humanizer = Humanizer()
        self.proxy_list = []

    async def run_task(self, proxy_url: str, user_agent: str, task_url: str, actions: list):
        """Run stealth task with proxy rotation and CAPTCHA solving."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
            proxy = proxy_url or self._get_proxy()
            context = await browser.new_context(
                user_agent=user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                proxy={"server": proxy} if proxy else None,
                viewport={"width": 1920, "height": 1080}
            )
            await stealth_async(context)
            page = await context.new_page()
            await page.goto(task_url)
            await self.humanizer.async_random_delay(1, 3)
            for action in actions:
                if action['type'] == 'click':
                    await page.click(action['selector'])
                    await self.humanizer.async_random_delay(0.5, 2)
                elif action['type'] == 'type':
                    await page.fill(action['selector'], action['text'])
                    await self.humanizer.async_random_delay(0.5, 2)
                elif action['type'] == 'captcha':
                    await self.solve_captcha(page, action.get('site_key'))
            await browser.close()

    def _get_proxy(self) -> str:
        """Rotate proxy from BrightData."""
        if not self.proxy_list:
            try:
                response = requests.get(settings.BRIGHTDATA_PROXY_URL, timeout=10)
                self.proxy_list = response.json().get('proxies', []) if response.status_code == 200 else []
            except:
                pass
        return self.proxy_list.pop(0) if self.proxy_list else ""

    async def solve_captcha(self, page, site_key: str = None):
        """Solve CAPTCHA using CapSolver API with fallback."""
        if not site_key:
            site_key = await page.evaluate("document.querySelector('.g-recaptcha, .h-captcha').getAttribute('data-sitekey')")
        if not site_key:
            return  # No CAPTCHA
        payload = {
            "clientKey": settings.CAPSOLVER_API_KEY,
            "task": {
                "type": "HCaptchaTaskProxyless" if "h-captcha" in await page.content() else "ReCaptchaV2TaskProxyless",
                "websiteURL": page.url,
                "websiteKey": site_key
            }
        }
        response = requests.post("https://api.capsolver.com/createTask", json=payload, timeout=30)
        if response.status_code != 200:
            raise CaptchaSolveError("CapSolver API error")
        task_id = response.json().get("taskId")
        for _ in range(60):  # Poll up to 60s
            result = requests.post("https://api.capsolver.com/getTaskResult", json={"clientKey": settings.CAPSOLVER_API_KEY, "taskId": task_id}, timeout=10)
            if result.json().get("status") == "ready":
                token = result.json()["solution"]["gRecaptchaResponse"]
                await page.evaluate(f"document.querySelector('.g-recaptcha-response, #h-captcha-response').innerHTML = '{token}';")
                return
            await asyncio.sleep(1)
        raise CaptchaSolveError("CapSolver timeout")
