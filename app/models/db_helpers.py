from datetime import datetime
from app.models.models import conversation_collection, message_collection
from app.helpers.helpers import extract_chat_history

def insert_or_get_conversation(user_id, user_ph_number):
    existing_conversation = conversation_collection.find_one({'user_id': user_id})
    
    if existing_conversation:
        return str(existing_conversation['_id'])
    else:
        conversation = {
            'user_id': user_id,
            'time': datetime.now(),
            'user_ph_number': user_ph_number
        }
        try:
            result = conversation_collection.insert_one(conversation)
            return str(result.inserted_id)
        except Exception as e:
            return str(e)


def insert_chat_history(user_id, user_ph_number, chat_history):
    conv_id = insert_or_get_conversation(user_id, user_ph_number)
    extracted_history = extract_chat_history(chat_history, conv_id, user_id)        
    try:
        message_collection.insert_many(extracted_history)
    except Exception as e:
        print(f"Error inserting message: {str(e)}")
            

def get_chat_history(user_id):
    chat_history = []
    messages = message_collection.find({'user_id': user_id}).sort('timestamp', 1)
    for message in messages:
        chat_history.append({"content" : message["content"], "role": message["role"]})
    return chat_history
