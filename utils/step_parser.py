def get_pause_dialog_js(key_name):
    # Returns the JS code for the browser modal dialog for pause_action
    label_text = f"Please enter the value for {key_name.replace('_', ' ')}:"
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
            label.innerText = `{label_text}`;
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
    return js_code

def parse_section_key(section_key, user_data, locators, value=None):
    """
    Parses a section_key string and returns (section, key_name, selector, value).
    Handles =value, user_data fallback, and locator lookup.
    """
    if '=' in section_key:
        section_key, value = section_key.split('=')
    if value is None and user_data is not None:
        value = user_data.get(section_key.split('.')[-1])
    section, key_name = section_key.split('.')
    selector = locators[section][key_name]
    return section, key_name, selector, value
