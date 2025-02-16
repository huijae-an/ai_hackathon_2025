from app.services.openai_service import openai_chat_completion
import re
import json

def categorize_emails(emails):
    """
    Uses GPT to categorize emails into:
        1. Jobs/Internships/LinkedIn + UC Berkeley news/opportunities
        2. Grades/assignments + ED emails
        3. Conversations
    Returns a list of dicts with structure:
        [
            {
                "subject": ...,
                "body": ...,
                "category": "jobs" / "grades" / "conversations" / "other"
            },
            ...
        ]
    """
    filtered_categorized = []
    # Construct a single prompt with all email subjects/bodies
    # Or do multiple calls (one per email). We'll do one call for demonstration:
    prompt = (
    "You are a helpful assistant that categorizes emails into "
    "one of the following categories:\n"
    "1) Jobs/Internships/LinkedIn/UC Berkeley news/opportunities\n"
    "2) Grades/assignments + ED emails\n"
    "3) Conversations\n"
    "4) Other (includes marketing or spam)\n\n"
    "Return ONLY the email as a dictionary with the following keys:\n"
    "- 'subject': The subject of the email\n"
    "- 'body': The body of the email\n"
    "- 'category': The category (numerical only) based on the classification above\n\n"
    "Remember, only return the json data (dictionary) and nothing else. YOU MUST ENSURE THAT IT IS IN PROPER JSON FORMAT. MY CODE WILL CRASH OTHERWISE. PLEASE DOUBLE CHECK THE JSON DATA OUTPUT PLEASE. Please don't give any other explanations—literally only the dictionary and nothing else. Within the body of the email, please format the email in full sentences and structure it properly.\n")


    for email in emails:
        partial_prompt = f"Subject: {email['subject']}\nBody: {email['body']}\n"

        # We'll get a single category from GPT for each email
        response = openai_chat_completion(prompt + partial_prompt)
        match = re.search(r'{.*}', response, re.DOTALL)
        if match:
            json_string = match.group(0)
            print(json_string)
            json_data = json.loads(json_string)
            print(json_data)

        if json_data['category'] != 4 :
            filtered_categorized.append(json_data)
        
        print(json_data)

    return filtered_categorized
