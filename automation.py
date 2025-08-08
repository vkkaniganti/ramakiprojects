

import configparser
import logging
from utils.step_parser import parse_section_key

logging.basicConfig(
    filename='automation.log',
    filemode='w',  # Overwrite log file on each run
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
)


class AutomationSteps:

    
    def __init__(self, page, locators_conf_path, steps_conf_path, user_data):
        self.page = page
        self.user_data = user_data

        self.locators = configparser.ConfigParser()
        self.locators.read(locators_conf_path)

        self.steps = configparser.ConfigParser()
        self.steps.read(steps_conf_path)

    async def mouseover_action(self, section_key):
        section, key_name, selector, _ = parse_section_key(section_key, self.user_data, self.locators)
        logging.info(f"Mouse over element {section}.{key_name}")
        await self.page.hover(selector)

    async def fill_field_action(self, section_key, value=None):
        from utils.step_parser import scroll_and_retry
        section, key_name, selector, value = parse_section_key(section_key, self.user_data, self.locators, value)
        logging.info(f"Filling field {section}.{key_name} with value: {value}")
        found = await scroll_and_retry(self.page, selector)
        if found:
            await self.page.fill(selector, value)
        else:
            logging.error(f"Could not find element for {section}.{key_name} after scrolling.")

    async def click_action(self, section_key):
        from utils.step_parser import scroll_and_retry
        section, key_name, selector, _ = parse_section_key(section_key, self.user_data, self.locators)
        logging.info(f"Clicking element {section}.{key_name}")
        found = await scroll_and_retry(self.page, selector)
        if found:
            await self.page.click(selector)
        else:
            logging.error(f"Could not find element for {section}.{key_name} after scrolling.")

    async def pause_action(self, section_key):
        from utils.step_parser import scroll_and_retry, get_pause_dialog_js
        section, key_name, selector, _ = parse_section_key(section_key, self.user_data, self.locators)
        logging.info(f"Pausing for {section}.{key_name}")
        # Use Python input for OTP or navigation-prone steps
        # if any(x in key_name.lower() for x in ["otp", "password", "pin", "code"]):
        #     user_value = input(f"Please enter the value for {key_name.replace('_', ' ')} (as seen in the browser): ")
        # else:
        js_code = get_pause_dialog_js(key_name)
        user_value = await self.page.evaluate(js_code)
        if not user_value:
            logging.warning(f"User cancelled or left blank the prompt for {section}.{key_name}")
            return
        found = await scroll_and_retry(self.page, selector)
        if found:
            logging.info(f"Filling paused value into {section}.{key_name} using selector: {selector}")
            await self.page.fill(selector, user_value)
        else:
            logging.warning(f"No locator found for pause: {section}.{key_name} after scrolling.")

    async def select_action(self, section_key, value=None):
        section, key_name, selector, value = parse_section_key(section_key, self.user_data, self.locators, value)
        logging.info(f"Selecting value '{value}' in dropdown {section}.{key_name} using selector: {selector}")
        await self.page.select_option(selector, label=value)


    async def radio_action(self, section_key, value=None):
        section, key_name, selector, value = parse_section_key(section_key, self.user_data, self.locators, value)
        logging.info(f"Selecting radio button {section}.{key_name} with value: {value} using selector: {selector}")
        # If value is provided, try to select the radio with the matching value attribute
        if value:
            radio_selector = f"{selector}[value='{value}']"
            await self.page.check(radio_selector)
        else:
            await self.page.check(selector)


    async def checkbox_action(self, section_key, value=None):
        section, key_name, selector, value = parse_section_key(section_key, self.user_data, self.locators, value)
        logging.info(f"Setting checkbox {section}.{key_name} to value: {value} using selector: {selector}")
        # If value is provided, check or uncheck accordingly (accepts 'true', 'false', 'yes', 'no', '1', '0')
        if value is not None:
            value_str = str(value).strip().lower()
            if value_str in ["true", "yes", "1"]:
                await self.page.check(selector)
            elif value_str in ["false", "no", "0"]:
                await self.page.uncheck(selector)
            else:
                logging.warning(f"Unknown checkbox value '{value}' for {section}.{key_name}, defaulting to check.")
                await self.page.check(selector)
        else:
            # Default: toggle the checkbox
            await self.page.click(selector)

    async def run(self):
        for key in self.steps['steps']:
            action = self.steps['steps'][key]
            try:
                logging.info(f"Starting step: {key} - {action}")
                if action.startswith("fill_field:"):
                    section_key = action.split("fill_field:")[1]
                    await self.fill_field_action(section_key)
                elif action.startswith("click:"):
                    section_key = action.split("click:")[1]
                    await self.click_action(section_key)
                elif action.startswith("pause:"):
                    section_key = action.split("pause:")[1]
                    await self.pause_action(section_key)
                elif action.startswith("select:"):
                    section_key = action.split("select:")[1]
                    await self.select_action(section_key)
                elif action.startswith("radio:"):
                    section_key = action.split("radio:")[1]
                    await self.radio_action(section_key)
                elif action.startswith("checkbox:"):
                    section_key = action.split("checkbox:")[1]
                    await self.checkbox_action(section_key)
                elif action.startswith("mouseover:"):
                    section_key = action.split("mouseover:")[1]
                    await self.mouseover_action(section_key)
                else:
                    logging.warning(f"Unknown action: {action}")
            except Exception as e:
                logging.error(f"Error in step {key} ({action}): {e}", exc_info=True)
                raise
