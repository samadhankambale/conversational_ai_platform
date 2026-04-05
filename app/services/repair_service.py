def repair_conversation(message: str):
    if not message or len(message.strip()) == 0:
        return "Can you clarify your request?"
    return message