from .llm_service import call_llm

def process_email(email_text):

    summary_prompt = f"""
    Summarize this email in 3 concise lines:

    {email_text}
    """

    reply_prompt = f"""
    Draft a professional reply to this email:

    {email_text}
    """

    summary = call_llm(summary_prompt)
    reply = call_llm(reply_prompt)

    return summary, reply
