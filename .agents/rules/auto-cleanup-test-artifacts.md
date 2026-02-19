---
trigger: always_on
---

Trigger: Upon the successful completion and verification of a task, script execution, or debugging session.
Context: To maintain a clean, production-ready directory structure, all temporary files generated for the sole purpose of testing or debugging must be ephemeral.
Instruction:

"You must aggressively maintain a clean workspace. Whenever you create temporary scripts, dummy data files, or debug logs (e.g., test_*.py, temp_output.json, debug.log) to verify logic or test an API, you must track these files.

Cleanup Execution:
Once the primary task is successfully completed, verified, and the final code is integrated, you must automatically delete all corresponding test and debug artifacts.

Command Pattern:
Use standard Linux removal commands (e.g., rm test_script.py or rm -rf temp_debug_dir/). Never delete user-provided source files or configuration files without explicit permission."