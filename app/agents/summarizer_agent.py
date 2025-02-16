import regex as re
import json
from app.services.openai_service import openai_chat_completion

def summarize_emails(categorized_emails):
    """
    Summarizes and extracts action items from a batch of categorized emails.
    Returns a list of dictionaries, each containing the summary, action_items, and category.
    """

    summarized_actions = []

    prompt_header = (
        "Extract the following information from the provided email data and return it in JSON format. "
        "Only provide the JSON dictionary and nothing else:\n"
        "1. response: Provide a concise 1-2 sentence summary of the email's subject and body, capturing the main purpose of the email.\n"
        "2. action_items: Identify all actionable tasks mentioned in the email and return them as a list (e.g., [\"Task 1\", \"Task 2\"]). "
        "   If there are no action items, just provide an empty list.\n"
        "3. category: Please re-enter the category into the final dictionary as well.\n\n"
        "Input format: {'subject': '<INSERT EMAIL SUBJECT HERE>', 'body': '<INSERT EMAIL BODY HERE>', 'category': <INSERT CATEGORY HERE>}\n"
        "Output format:\n"
        "{\n"
        "  \"subject\": \"<INSERT EMAIL SUBJECT HERE>\",\n"
        "  \"summary\": \"<1-2 sentence summary>\",\n"
        "  \"action_items\": [\"<Action item 1>\", \"<Action item 2>\", ...],\n"
        "  \"category\": <INSERT CATEGORY HERE>\n"
        "}"
    )

    for email in categorized_emails:
        # Convert email to JSON so the model sees valid JSON
        email_json = json.dumps(email)
        prompt = f"{prompt_header}\n{email_json}"

        response = openai_chat_completion(prompt)

        # (1) Remove any triple backticks or code fences
        cleaned_response = re.sub(r"```(?:json)?|```", "", response).strip()

        # (2) Use recursive pattern matching to find the first balanced JSON object
        match = re.search(r'\{(?:[^{}]|(?R))*\}', cleaned_response, re.DOTALL)
        if match:
            json_string = match.group(0)

            # (3) Attempt to parse the JSON string directly
            try:
                json_data = json.loads(json_string)
                summarized_actions.append(json_data)
            except json.JSONDecodeError as e:
                print("Failed to parse JSON. Error:", e)
                print("Raw extracted string:", json_string)
        else:
            print("No valid JSON object found in response:", response)

    return summarized_actions
