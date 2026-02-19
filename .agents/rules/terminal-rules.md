---
trigger: always_on
---

# Execution Policy: WSL & Virtual Environment

When executing commands or running code in this workspace, you must strictly adhere to the following constraints:

1. **Terminal Environment:** All terminal commands must be executed within a `WSL` (Windows Subsystem for Linux) terminal. Do not use PowerShell or standard Windows Command Prompt. DO not use `wsl bash` instead use `wsl`
2. **Target Virtual Environment:** The Python virtual environment for this project is located one directory level up from the current working directory. 
3. **Python Execution Syntax:** Never use the global `python` or `python3` commands. Whenever you need to execute a Python script, you must explicitly call the Python binary from the parent directory's `bin` folder.
   - **Correct:** `../bin/python3 -m <script_name.py>`
   - **Incorrect:** `python <script_name.py>` or `python3 <script_name.py>`

Always verify you are using the `../bin/python3` path to avoid missing dependency errors.