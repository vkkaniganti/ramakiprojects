Web Automation Tool - User Guide
================================

This tool automates web data entry and actions for you. You only need to provide your data and configuration files. No Python or technical setup is required.

How to Use
----------
1. Double-click the `main.exe` file on your desktop to start the automation.
2. Make sure the following folders are present in the same folder as `main.exe`:
   - `config` (contains `.conf` files for locators and steps)
   - `data` (contains your Excel or CSV files)
3. Edit the files in `config` and `data` as needed for your use case. Do NOT change any other files.

What You Can Edit
-----------------
- `config/locators.conf`: Update element locators if the website changes.
- `config/steps.conf`: Change the sequence of automation steps.
- `data/input_data.xlsx` or `data/input_data.csv`: Add or update your input data.

What You Should NOT Edit
------------------------
- Do not modify or delete `main.exe` or any files except those in `config` and `data`.
- Do not move `main.exe` out of its folder unless you also move the `config` and `data` folders with it.

Troubleshooting
---------------
- If you see a browser window asking for a value (like captcha or OTP), enter it and click OK.
- If you encounter errors, check the `automation.log` file for details.
- If you need to reset the tool, close all browser windows and double-click `main.exe` again.

Support
-------
For any issues or questions, please contact your automation provider.
