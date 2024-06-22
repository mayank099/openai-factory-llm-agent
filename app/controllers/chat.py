from app.tools import tools
#from app.prompts.prompttemplate import main_qa_prompt :: TODO : Use as system prompt
from app.models.db_helpers import insert_chat_history, get_chat_history
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored  
import logging.config
import json

load_dotenv()  # Load environment variables from .env file
logger = logging.getLogger(__name__)  # get a logger instance

retail_tool = tools ## Todo :: Fix this later, import them one by one

GPT_MODEL = "gpt-4o"
client = OpenAI()


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
            
            
def handle_function_calling(tool_calls, messages):
    try:
        
        tool_call_id = tool_calls[0].id
        tool_function_name = tool_calls[0].function.name
        tool_query_string = eval(tool_calls[0].function.arguments)['location']
        # Step 3: Call the function and retrieve results. Append the results to the messages list.      
        if tool_function_name == 'get_current_weather':
            results = {"india" : "32 Celsius"}
            json_data = json.dumps(results)
            messages.append({
                "role":"tool", 
                "tool_call_id":tool_call_id, 
                "name": tool_function_name, 
                "content":json_data
            })
            
            # Step 4: Invoke the chat completions API with the function response appended to the messages list
            # Note that messages with role 'tool' must be a response to a preceding message with 'tool_calls'
            model_response_with_function_call = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )  # get a new response from the model where it can see the function response

            assistant_message = model_response_with_function_call.choices[0].message
            tool_calls = assistant_message.tool_calls
            messages.append(assistant_message)

            if tool_calls:
                print("nhi agya fir se call kro")
                return assistant_message, True
            else:
                return assistant_message, False
        else: 
            print(f"Error: function {tool_function_name} does not exist")
        ## Check for tool
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None, False                
            
            
        
def chat_agent(params):
    resp = None
    prompt = params["input"]
    user_id = params["user_id"]
    user_phone = params["user_phone"]

    chat_history = get_chat_history(user_id)
    messages = []    
    
    # Append chat_history to chat.history if is not empty
    if len(chat_history) > 0:
        messages.extend(chat_history)
    chat_history_len = len(messages)
    
    messages.append({"role": "user", "content":prompt })
    print("==================History======================================")
    print(messages)
    print("=====================History===================================")

    chat_response = chat_completion_request(
        messages, tools=tools
    )

    assistant_message = chat_response.choices[0].message

    tool_calls = assistant_message.tool_calls
    if tool_calls:
        while True:
            messages.append(assistant_message)
            api_response, is_function_call = handle_function_calling(tool_calls, messages)
            if api_response:
                tool_calls = api_response.tool_calls
            if not is_function_call:
                resp = api_response.content
                break
    else:
        messages.append({"role" : assistant_message.role , "content" : assistant_message.content})        
        resp = assistant_message.content
    
    recent_chat_history = messages[chat_history_len:]
    insert_chat_history(user_id, user_phone, recent_chat_history)
    return {
        "response": resp,
        "chat_history": extract_chat_history(messages),
    }
    
    
def extract_chat_history(chat_history):
    history = []
    for content in chat_history:
        if isinstance(content, dict):
            if content['role'] == "user" or content['role'] == "assistant":
                history.append({
                    "role" : content['role'],
                    "content" : content['content']
                })
        else:
            role = content.role
            main_content = content.content
            tool_calls = content.tool_calls
    
            if tool_calls is not None:
                # Access tool_calls if it exists
                print(f"Tool Calls: {tool_calls}")
            elif role == "user" or role == "assistant":
                history.append({
                    "role" :role,
                    "content" : main_content,
                })
                print("No tool calls found But history added")    
    return history
     
    