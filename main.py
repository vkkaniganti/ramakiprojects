
import asyncio
from playwright.async_api import async_playwright
from utils.excel_reader import read_csv, read_excel
from automation import AutomationSteps
import os
import sys
import subprocess

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

EXCEL_PATH = resource_path("data/input_data.xlsx")
CSV_PATH= resource_path("data/Dummy_Data.csv")
LOCATORS_CONF = resource_path("config/locators.conf")
STEPS_CONF = resource_path("config/steps.conf")

async def run_automation():
    # input_rows = read_excel(EXCEL_PATH)
    input_rows = read_csv(CSV_PATH)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://tgtransport.net/TGCFSTONLINE/Registration/DealerLogin.aspx")

        for user_data in input_rows:
            automator = AutomationSteps(page, LOCATORS_CONF, STEPS_CONF, user_data)
            await automator.run()

        await browser.close()
def ensure_playwright_browsers_installed():
    try:
        from playwright.sync_api import sync_playwright
        # Try launching a browser to check if installed
        with sync_playwright() as p:
            p.chromium.launch(headless=False).close()
    except Exception:
        # If fails, run playwright install
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)

       

if __name__ == "__main__":
    # ensure_playwright_browsers_installed() 
    asyncio.run(run_automation())
