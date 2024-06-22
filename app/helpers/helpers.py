# app/helpers.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)  # get a logger instance

def handle_response(data, status_code=200):
    """Handle standard responses for the application."""
    return {
        "data": data,
        "status": status_code
    }

def extract_chat_history(chat_history, conv_id, user_id):
    logger.info("Extracting chat history")
    history = []
    for content in chat_history:
        if isinstance(content, dict):
            if content['role'] == "user" or content['role'] == "assistant":
                history.append({
                    "role" : content['role'],
                    "content" : content['content'],
                    "user_id": user_id,
                    "convo_id": conv_id,
                    "timestamp": datetime.now()
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
                    "user_id": user_id,
                    "convo_id": conv_id,
                    "timestamp": datetime.now()
                })
                print("No tool calls found But history appened")    
    return history