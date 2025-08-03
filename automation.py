
import configparser
import logging

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
        section, key_name = section_key.split('.')
        selector = self.locators[section][key_name]
        logging.info(f"Mouse over element {section}.{key_name}")
        await self.page.hover(selector)

    async def fill_field_action(self, section_key, value=None):
        if '=' in section_key:
            section_key, value = section_key.split('=')
        if value is None:
            value = self.user_data.get(section_key.split('.')[-1])
        section, key_name = section_key.split('.')
        selector = self.locators[section][key_name]
        logging.info(f"Filling field {section}.{key_name} with value: {value}")
        await self.page.fill(selector, value)

    async def click_action(self, section_key):
        section, key_name = section_key.split('.')
        selector = self.locators[section][key_name]
        logging.info(f"Clicking element {section}.{key_name}")
        await self.page.click(selector)

    async def pause_action(self, section_key):
        section, key_name = section_key.split('.')
        logging.info(f"Pausing for {section}.{key_name}")
        # Use Python input for OTP or navigation-prone steps
        if any(x in key_name.lower() for x in ["otp", "password", "pin", "code"]):
            user_value = input(f"Please enter the value for {key_name.replace('_', ' ')} (as seen in the browser): ")
        else:
            js_code = f'''
                new Promise((resolve) => {{
                    let existing = document.getElementById('automation-prompt-modal');
                    if (existing) existing.remove();
                    let modal = document.createElement('div');
                    modal.id = 'automation-prompt-modal';
                    modal.style.position = 'fixed';
                    modal.style.top = '0';
                    modal.style.left = '0';
                    modal.style.width = '100vw';
                    modal.style.height = '100vh';
                    modal.style.background = 'rgba(0,0,0,0.5)';
                    modal.style.display = 'flex';
                    modal.style.alignItems = 'center';
                    modal.style.justifyContent = 'center';
                    modal.style.zIndex = '9999';
                    let box = document.createElement('div');
                    box.style.background = '#fff';
                    box.style.padding = '2em';
                    box.style.borderRadius = '8px';
                    box.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
                    box.style.position = 'absolute';
                    box.style.left = '50%';
                    box.style.top = '50%';
                    box.style.transform = 'translate(-50%, -50%)';
                    let label = document.createElement('label');
                    label.innerText = 'Please enter the value for {key_name.replace('_', ' ')}:';
                    label.style.display = 'block';
                    label.style.marginBottom = '1em';
                    label.style.cursor = 'move';
                    let input = document.createElement('input');
                    input.type = 'text';
                    input.style.width = '100%';
                    input.style.fontSize = '1.2em';
                    input.style.marginBottom = '1em';
                    let btn = document.createElement('button');
                    btn.innerText = 'OK';
                    btn.style.fontSize = '1em';
                    btn.onclick = () => {{
                        let val = input.value;
                        modal.remove();
                        resolve(val);
                    }};
                    box.appendChild(label);
                    box.appendChild(input);
                    box.appendChild(btn);
                    modal.appendChild(box);
                    document.body.appendChild(modal);
                    input.focus();

                    // Make the box draggable by the label
                    let isDragging = false, startX, startY, startLeft, startTop;
                    label.addEventListener('mousedown', function(e) {{
                        isDragging = true;
                        startX = e.clientX;
                        startY = e.clientY;
                        startLeft = box.offsetLeft;
                        startTop = box.offsetTop;
                        document.body.style.userSelect = 'none';
                    }});
                    document.addEventListener('mousemove', function(e) {{
                        if (!isDragging) return;
                        let dx = e.clientX - startX;
                        let dy = e.clientY - startY;
                        box.style.left = (startLeft + dx) + 'px';
                        box.style.top = (startTop + dy) + 'px';
                        box.style.transform = '';
                    }});
                    document.addEventListener('mouseup', function(e) {{
                        isDragging = false;
                        document.body.style.userSelect = '';
                    }});
                }});
            '''
            user_value = await self.page.evaluate(js_code)
        if not user_value:
            logging.warning(f"User cancelled or left blank the prompt for {section}.{key_name}")
            return
        if section in self.locators and key_name in self.locators[section]:
            selector = self.locators[section][key_name]
            logging.info(f"Filling paused value into {section}.{key_name} using selector: {selector}")
            await self.page.fill(selector, user_value)
        else:
            logging.warning(f"No locator found for pause: {section}.{key_name}")

    async def select_action(self, section_key, value=None):
        # Support select:section.key=value or select:section.key (value from user_data)
        if '=' in section_key:
            section_key, value = section_key.split('=')
        if value is None:
            value = self.user_data.get(section_key.split('.')[-1])
        section, key_name = section_key.split('.')
        selector = self.locators[section][key_name]
        logging.info(f"Selecting value '{value}' in dropdown {section}.{key_name} using selector: {selector}")
        await self.page.select_option(selector, label=value)

    async def radio_action(self, section_key, value=None):
        # Placeholder for radio buttons
        logging.info(f"Radio action not implemented for {section_key}")

    async def checkbox_action(self, section_key, value=None):
        # Placeholder for checkboxes
        logging.info(f"Checkbox action not implemented for {section_key}")

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
