#!/usr/bin/env python3
"""
סוכן תודעה - מבוסס תורת בשאר
Consciousness Agent - Based on Bashar Teachings
"""

import os
import sys
from anthropic import Anthropic
from system_prompt import SYSTEM_PROMPT


def create_client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("שגיאה: משתנה הסביבה ANTHROPIC_API_KEY לא מוגדר.")
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def run_bot() -> None:
    client = create_client()
    conversation_history = []

    print("\n" + "=" * 60)
    print("  סוכן התודעה  |  Consciousness Agent")
    print("  מבוסס תורת בשאר  |  Based on Bashar Teachings")
    print("=" * 60)
    print("\nכדי לצאת, הקלד: יציאה / exit / quit\n")

    while True:
        try:
            user_input = input("אתה: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nהאור שבך תמיד יאיר. להתראות.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("יציאה", "exit", "quit", "q"):
            print("\nהאור שבך תמיד יאיר. להתראות.")
            break

        conversation_history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=conversation_history,
        )

        assistant_message = response.content[0].text
        conversation_history.append(
            {"role": "assistant", "content": assistant_message}
        )

        print(f"\nסוכן: {assistant_message}\n")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    run_bot()
