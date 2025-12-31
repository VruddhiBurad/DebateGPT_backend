def debate_prompt(user_input: str) -> str:
    return f"""
You are an intelligent debate opponent.

Task:
- Read the user's statement
- Provide a clear, logical counter-argument
- Be concise and structured

- Avoid repetition
- Use formal debate language

User statement:
{user_input}

Counter-argument:
"""