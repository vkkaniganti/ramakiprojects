
import asyncio
from playwright.async_api import async_playwright
from utils.excel_reader import read_excel
from automation import AutomationSteps
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

EXCEL_PATH = resource_path("data/input_data.xlsx")
LOCATORS_CONF = resource_path("config/locators.conf")
STEPS_CONF = resource_path("config/steps.conf")

async def run_automation():
    input_rows = read_excel(EXCEL_PATH)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://example.com/login")

        for user_data in input_rows:
            automator = AutomationSteps(page, LOCATORS_CONF, STEPS_CONF, user_data)
            await automator.run()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_automation())
