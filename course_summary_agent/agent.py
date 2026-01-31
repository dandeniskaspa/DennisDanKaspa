"""Core agent logic for generating course summaries."""

import os
from pathlib import Path

import yaml
from anthropic import Anthropic

from .models import Course, Language, SummaryType
from .prompts import build_prompt, get_system_prompt


class CourseSummaryAgent:
    """Agent that generates course summaries using Claude."""

    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is required. "
                "Set it as an environment variable or pass it directly."
            )
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def load_course(self, path: str) -> Course:
        """Load a course definition from a YAML file."""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Course file not found: {path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return Course.from_dict(data)

    def generate_summary(
        self,
        course: Course,
        summary_type: SummaryType,
        topic_name: str | None = None,
    ) -> str:
        """Generate a summary for the given course."""
        system_prompt = get_system_prompt(course.language)
        user_prompt = build_prompt(course, summary_type, topic_name)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        return response.content[0].text

    def generate_and_save(
        self,
        course: Course,
        summary_type: SummaryType,
        output_dir: str = "output",
        topic_name: str | None = None,
    ) -> Path:
        """Generate a summary and save it to a markdown file."""
        summary = self.generate_summary(course, summary_type, topic_name)

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        safe_name = course.name.replace(" ", "_").replace("/", "_")
        if topic_name:
            safe_topic = topic_name.replace(" ", "_").replace("/", "_")
            filename = f"{safe_name}_{summary_type.value}_{safe_topic}.md"
        else:
            filename = f"{safe_name}_{summary_type.value}.md"

        file_path = out_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(summary)

        return file_path

    def interactive_session(self, course: Course) -> None:
        """Run an interactive chat session about the course."""
        system_prompt = get_system_prompt(course.language)
        context = build_prompt(course, SummaryType.FULL)

        is_hebrew = course.language == Language.HEBREW
        if is_hebrew:
            welcome = (
                f'\nשלום! אני הסוכן לסיכום קורסים. אני מוכן לעזור לך עם הקורס "{course.name}".\n'
                "אתה יכול לשאול אותי שאלות, לבקש סיכומים, או לדון בחומר הקורס.\n"
                'כתוב "יציאה" כדי לסיים.\n'
            )
        else:
            welcome = (
                f'\nHello! I\'m the course summary agent. I\'m ready to help you with the course "{course.name}".\n'
                "You can ask me questions, request summaries, or discuss the course material.\n"
                'Type "exit" to quit.\n'
            )

        print(welcome)

        messages = [
            {
                "role": "user",
                "content": f"Here is the course information for context:\n\n{context}",
            },
            {
                "role": "assistant",
                "content": "I've reviewed the course material. I'm ready to help. What would you like to know?",
            },
        ]

        exit_words = {"exit", "quit", "יציאה", "צא"}

        while True:
            try:
                user_input = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nלהתראות!" if is_hebrew else "\nGoodbye!")
                break

            if user_input.lower() in exit_words or not user_input:
                print("להתראות!" if is_hebrew else "Goodbye!")
                break

            messages.append({"role": "user", "content": user_input})

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=messages,
            )

            assistant_message = response.content[0].text
            messages.append({"role": "assistant", "content": assistant_message})
            print(f"\n{assistant_message}")
