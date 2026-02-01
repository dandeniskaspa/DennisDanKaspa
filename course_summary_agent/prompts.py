"""Prompt templates for different summary types."""

from .models import Course, SummaryType, Language

SYSTEM_PROMPT_HE = """אתה עוזר אקדמי מומחה ביצירת סיכומים לקורסים אקדמיים.
תפקידך לייצר סיכומים ברורים, מובנים ומקיפים שיעזרו לסטודנטים להבין את חומר הקורס.

כללים:
- כתוב בעברית ברורה ומקצועית
- השתמש במבנה היררכי עם כותרות וכותרות משנה
- הדגש מושגי מפתח
- הוסף דוגמאות כשרלוונטי
- התאם את רמת הפירוט לסוג הסיכום המבוקש
"""

SYSTEM_PROMPT_EN = """You are an expert academic assistant specialized in creating course summaries.
Your role is to produce clear, structured, and comprehensive summaries that help students understand course material.

Rules:
- Write in clear, professional language
- Use hierarchical structure with headings and subheadings
- Highlight key concepts
- Add examples when relevant
- Adjust detail level to match the requested summary type
"""


def get_system_prompt(language: Language) -> str:
    if language == Language.HEBREW:
        return SYSTEM_PROMPT_HE
    return SYSTEM_PROMPT_EN


def _format_course_context(course: Course) -> str:
    """Build a textual representation of the course for the prompt."""
    lines = [f"# {course.name}"]
    if course.description:
        lines.append(f"\n{course.description}")
    if course.instructor:
        lines.append(f"\nInstructor: {course.instructor}")
    if course.target_audience:
        lines.append(f"Target audience: {course.target_audience}")
    if course.prerequisites:
        lines.append(f"Prerequisites: {', '.join(course.prerequisites)}")

    if course.topics:
        lines.append("\n## Topics")
        for i, topic in enumerate(course.topics, 1):
            lines.append(f"\n### {i}. {topic.name}")
            if topic.description:
                lines.append(topic.description)
            if topic.subtopics:
                for sub in topic.subtopics:
                    lines.append(f"  - {sub}")
            if topic.key_concepts:
                lines.append(f"  Key concepts: {', '.join(topic.key_concepts)}")
            if topic.learning_objectives:
                lines.append("  Learning objectives:")
                for obj in topic.learning_objectives:
                    lines.append(f"    - {obj}")

    return "\n".join(lines)


def build_prompt(course: Course, summary_type: SummaryType, topic_name: str | None = None) -> str:
    """Build the user prompt based on summary type."""
    context = _format_course_context(course)
    is_hebrew = course.language == Language.HEBREW

    if summary_type == SummaryType.FULL:
        if is_hebrew:
            instruction = (
                "צור סיכום מלא ומקיף של הקורס הבא. "
                "הסיכום צריך לכלול:\n"
                "1. סקירה כללית של הקורס\n"
                "2. סיכום של כל נושא עם הנקודות העיקריות\n"
                "3. קשרים בין הנושאים\n"
                "4. מושגי מפתח מרכזיים\n"
                "5. סיכום מסכם"
            )
        else:
            instruction = (
                "Create a full and comprehensive summary of the following course. "
                "The summary should include:\n"
                "1. General course overview\n"
                "2. Summary of each topic with main points\n"
                "3. Connections between topics\n"
                "4. Central key concepts\n"
                "5. Concluding summary"
            )

    elif summary_type == SummaryType.TOPIC:
        if topic_name:
            if is_hebrew:
                instruction = (
                    f'צור סיכום מפורט של הנושא "{topic_name}" מתוך הקורס הבא. '
                    "הסיכום צריך לכלול:\n"
                    "1. הסבר מפורט של הנושא\n"
                    "2. מושגי מפתח והגדרות\n"
                    "3. דוגמאות להמחשה\n"
                    "4. קשר לנושאים אחרים בקורס"
                )
            else:
                instruction = (
                    f'Create a detailed summary of the topic "{topic_name}" from the following course. '
                    "The summary should include:\n"
                    "1. Detailed explanation of the topic\n"
                    "2. Key concepts and definitions\n"
                    "3. Illustrative examples\n"
                    "4. Connection to other course topics"
                )
        else:
            if is_hebrew:
                instruction = (
                    "צור סיכום נפרד לכל נושא בקורס הבא. "
                    "לכל נושא כלול:\n"
                    "1. הסבר מפורט\n"
                    "2. מושגי מפתח\n"
                    "3. דוגמאות\n"
                    "4. נקודות חשובות"
                )
            else:
                instruction = (
                    "Create a separate summary for each topic in the following course. "
                    "For each topic include:\n"
                    "1. Detailed explanation\n"
                    "2. Key concepts\n"
                    "3. Examples\n"
                    "4. Important points"
                )

    elif summary_type == SummaryType.KEY_CONCEPTS:
        if is_hebrew:
            instruction = (
                "צור רשימה מובנית של כל מושגי המפתח בקורס הבא. "
                "לכל מושג כלול:\n"
                "1. שם המושג\n"
                "2. הגדרה ברורה ותמציתית\n"
                "3. דוגמה או הקשר שימוש\n"
                "4. קשר למושגים אחרים בקורס"
            )
        else:
            instruction = (
                "Create a structured list of all key concepts in the following course. "
                "For each concept include:\n"
                "1. Concept name\n"
                "2. Clear and concise definition\n"
                "3. Example or usage context\n"
                "4. Connection to other concepts in the course"
            )

    elif summary_type == SummaryType.EXAM_PREP:
        if is_hebrew:
            instruction = (
                "צור סיכום להכנה למבחן עבור הקורס הבא. "
                "הסיכום צריך לכלול:\n"
                "1. נקודות עיקריות שחשוב לזכור\n"
                "2. מושגי מפתח עם הגדרות קצרות\n"
                "3. שאלות לחזרה עצמית (עם תשובות)\n"
                "4. טיפים ללמידה ושינון\n"
                "5. נושאים שכדאי להתמקד בהם"
            )
        else:
            instruction = (
                "Create an exam preparation summary for the following course. "
                "The summary should include:\n"
                "1. Main points to remember\n"
                "2. Key concepts with short definitions\n"
                "3. Self-review questions (with answers)\n"
                "4. Study and memorization tips\n"
                "5. Topics to focus on"
            )

    return f"{instruction}\n\n---\n\n{context}"
