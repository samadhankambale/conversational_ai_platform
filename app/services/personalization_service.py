def personalize_prompt(user_id: str, message: str) -> str:
    """
    Minimal personalization using authenticated user context.
    Keeps system extensible without unnecessary DB complexity.
    """
    return f"User ID: {user_id}\nUser message: {message}"