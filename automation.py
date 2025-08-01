
import configparser

class AutomationSteps:
    def __init__(self, page, locators_conf_path, steps_conf_path, user_data):
        self.page = page
        self.user_data = user_data

        self.locators = configparser.ConfigParser()
        self.locators.read(locators_conf_path)

        self.steps = configparser.ConfigParser()
        self.steps.read(steps_conf_path)

    async def run(self):
        for key in self.steps['steps']:
            action = self.steps['steps'][key]
            if action.startswith("fill_field:"):
                section_key = action.split("fill_field:")[1]
                section, key_name = section_key.split('.')
                selector = self.locators[section][key_name]
                value = self.user_data.get(key_name)
                await self.page.fill(selector, value)
            elif action.startswith("click:"):
                section_key = action.split("click:")[1]
                section, key_name = section_key.split('.')
                selector = self.locators[section][key_name]
                await self.page.click(selector)
            elif action == "pause_for_otp":
                input("Please enter the OTP manually in the browser and press Enter here to continue...")
