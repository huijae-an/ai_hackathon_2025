from flask import request, jsonify
from app.services.email_service import get_emails
from app.agents.categorization_agent import categorize_emails
from app.agents.summarizer_agent import summarize_emails
from app.agents.final_summarizer_agent import finalize_summaries

def handle_get_summary():
    # 1. Get all emails from the email service
    emails = get_emails()

    # Split emails into batches of 5-10
    batch_size = 10
    email_batches = [emails[i:i + batch_size] for i in range(0, len(emails), batch_size)]



    all_batch_summaries_actions = []
    final_batch_list = []

    for batch in email_batches:
        # 2. Categorize and filter emails in the batch
        categorized_filtered = categorize_emails(batch)

        # 3. Summarize & Extract action items from this batch
        all_batch_summaries_actions = summarize_emails(categorized_filtered)
        final_batch_list.append(all_batch_summaries_actions)

    
    # dictionary mapping response to condensed summary
    final_summary = finalize_summaries(final_batch_list)



    return {
        "final_comp_summary": final_summary['response'],
        "complete_email_list": final_batch_list
    }
