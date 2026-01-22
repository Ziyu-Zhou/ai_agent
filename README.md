## Overview

This project is a small AI coding agent that can inspect and modify a
calculator project using Gemini function calling.

### How it works

- `main.py`
  - Parses CLI args and starts the agent loop.
  - Maintains a `messages` list: the conversation history with the model.
  - Repeatedly calls `generate_content()` until the model produces a final answer
    (i.e., no more `function_calls`) or we hit `MAX_ITERS`.

- `generate_content()`
  - Sends `messages` to Gemini.
  - Appends the model's candidates to `messages`.
  - If the model requests tools:
    - Calls local Python functions via `call_function`.
    - Collects tool results and appends them to `messages` as a `"user"` message.
  - If there are no tool calls:
    - Returns the final natural-language answer.

- `call_function.py`
  - Maps Gemini function names (e.g. `"get_files_info"`) to Python functions.
  - Injects `working_directory="./calculator"` into each call.
  - Wraps the Python return value into a Gemini `function_response`.

- `functions/`
  - `get_files_info.py`: list files under the calculator project.
  - `get_file_content.py`: read source files.
  - `run_python_file.py`: execute `calculator/main.py`.
  - `write_file.py`: modify files when the agent wants to apply fixes.

### Calculator project

- Lives under `calculator/`
  - `calculator/main.py`: CLI entrypoint.
  - `calculator/pkg/calculator.py`: core calculator logic.
  - `calculator/pkg/render.py`: `format_json_output` to render results.
