import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_simple_task(description):

    if not client.api_key:
        return ["Error: OpenAI API key is not set."]

    try:

        prompt = f""""Break down the following task into a list of 3 to 5 subtasks simple and actionable.

Task: {description}

Response format:
- Subtask 1
- Subtask 2
- Subtask 3
- etc.

Response only with the list of subtasks, one per line, starting each line with a -"""

        params = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that breaks down tasks into simple subtasks."},
                {"role": "user", "content": prompt}
            ],
        }

        response = client.chat.completions.create(**params)
        content = response.choices[0].message.content.strip()

        subtasks = []

        for line in content.split("\n"):
            line = line.strip()
            if line and line.startswith("-"):
                subtask = line[1:].strip()
                if subtask:
                    subtasks.append(subtask)

        return subtasks if subtasks else ["Error: No subtasks generated."]

    except Exception as e:
        print(f"Error while connecting to OpenAI API: {e}")
        return [f"Error: Can't connect to OpenAI API."]