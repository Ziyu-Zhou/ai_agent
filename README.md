## Overview

This project is a small AI coding agent that can inspect and modify a
calculator project using Gemini function calling.

### How it works

### main.py

This file wires everything together and runs the agent.

- `setup()`
  - Loads environment variables with `dotenv`.
  - Reads `GEMINI_API_KEY` and raises an error if it’s missing.

- `parsing_input()`
  - Uses `argparse` to parse the CLI:
    - `user_prompt`: the initial question / task for the agent.
    - `--verbose`: if set, prints extra debug info and tool output.

- `llm_process(args)`
  - Creates the Gemini client.
  - Initializes the conversation `messages` with the user’s prompt.
  - **Agent loop** (`for _ in range(20)`):
    - Calls `client.models.generate_content(...)` with:
      - the current `messages`
      - the tools (`available_functions`)
      - the system prompt.
    - Appends the model’s `candidates` to `messages` so the model “remembers” what it said.
    - If there are **no** `function_calls`:
      - Prints `response.text` as the final answer and returns.
    - If there **are** `function_calls`:
      - For each tool call:
        - Uses `call_function` to run the corresponding Python function.
        - Extracts the `function_response` part.
        - Collects these into `function_result`.
      - Appends a new `types.Content(role="user", parts=function_result)` to `messages`
        so the next model call can see the tool results.

- `main()`
  - Calls `setup()` to load the API key.
  - Calls `parsing_input()` to get CLI arguments.
  - Calls `llm_process(args)` to run the agent.

### Tool function

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
