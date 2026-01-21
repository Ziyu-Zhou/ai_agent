import os 
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function

# setups
def setup():
    load_dotenv()
    global api_key 
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("bad api key")
    
def parsing_input():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    return args
# Now we can access `args.user_prompt`

# user_input = arg.user_prompt

def llm_process(args):
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # calling the LLM model
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction=system_prompt,
            temperature=0
            ),
    )

    #checking response meta data

    if response.usage_metadata != None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("no usage_metadata")
    

    # program output 
    if response.function_calls != None:
        function_result = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts:
                raise Exception("No parts in function_call_result")
            first_part = function_call_result.parts[0]

            if not first_part.function_response:
                raise Exception("No function_response in function_call_result")

            if not first_part.function_response.response:
                raise Exception("No function_response.response in function_call_result")

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            
        # for function_call in response.function_calls:
        #     print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)



def main():

    setup()

    args = parsing_input()

    llm_process(args)

    # print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
