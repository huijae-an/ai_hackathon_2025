from app.services.openai_service import openai_chat_completion


def finalize_summaries(input):
   """
   :param input: A list of lists (batches).
                 Each batch is a list of dictionaries with keys 'summary' and 'action_items'.
                 Example:
                 [
                     [
                         {"summary": "Summary text 1", "action_items": "..."},
                         {"summary": "Summary text 2", "action_items": "..."}
                     ],
                     [
                         {"summary": "Summary text 3", "action_items": "..."},
                         {"summary": "Summary text 4", "action_items": "..."}
                     ]
                 ]
   :return: A dictionary with a single key 'response' whose value is the 5-6 sentence
            condensed summary generated by the OpenAI API.
   """
   # Gather all summary texts from all batches
   all_summaries = []
   for batch in input:
       for entry in batch:
           all_summaries.append(entry["summary"])
  
   # Construct the prompt by concatenating all summaries
   combined_summaries = "\n".join(all_summaries)
   prompt = (
       "Below are several summaries. Read them carefully and provide a condensed, "
       "insightful 5-6 sentence final summary:\n\n"
       f"{combined_summaries}"
   )

  
   # Call the OpenAI service
   final_summary = openai_chat_completion(prompt)
  
   # Return in the requested format
   return {"response": final_summary}