# Course Summary Agent

סוכן AI ליצירת סיכומים לקורסים אקדמיים, מבוסס Claude API.

## תכונות

- **סיכום מלא** - סיכום מקיף של כל הקורס
- **סיכום לפי נושא** - סיכום מפורט של נושא ספציפי או כל הנושאים
- **מושגי מפתח** - רשימה מובנית של כל המושגים עם הגדרות
- **הכנה למבחן** - סיכום ממוקד עם שאלות לחזרה עצמית
- **מצב אינטראקטיבי** - צ'אט חי לשאלות על חומר הקורס
- **תמיכה בעברית ואנגלית**

## התקנה

```bash
pip install -r requirements.txt
```

הגדר את מפתח ה-API:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## שימוש

### הגדרת קורס

צור קובץ YAML עם מבנה הקורס (ראה דוגמאות בתיקיית `courses/`):

```yaml
name: "שם הקורס"
description: "תיאור הקורס"
instructor: "שם המרצה"
language: "he"  # he / en
target_audience: "קהל היעד"
prerequisites:
  - "דרישות קדם"

topics:
  - name: "שם הנושא"
    description: "תיאור הנושא"
    subtopics:
      - "תת-נושא 1"
      - "תת-נושא 2"
    key_concepts:
      - "מושג 1"
      - "מושג 2"
    learning_objectives:
      - "יעד למידה 1"
```

### יצירת סיכומים

```bash
# סיכום מלא
python -m course_summary_agent.cli generate courses/example_intro_to_cs.yaml

# סיכום לפי נושאים
python -m course_summary_agent.cli generate courses/example_intro_to_cs.yaml -t topic

# סיכום נושא ספציפי
python -m course_summary_agent.cli generate courses/example_intro_to_cs.yaml -t topic -n "יסודות פייתון"

# מושגי מפתח
python -m course_summary_agent.cli generate courses/example_intro_to_cs.yaml -t key_concepts

# הכנה למבחן
python -m course_summary_agent.cli generate courses/example_intro_to_cs.yaml -t exam_prep

# שמירה לתיקייה מותאמת
python -m course_summary_agent.cli generate courses/example_intro_to_cs.yaml -o my_summaries/
```

### מצב אינטראקטיבי

```bash
python -m course_summary_agent.cli chat courses/example_intro_to_cs.yaml
```

### הצגת מידע על קורס

```bash
python -m course_summary_agent.cli info courses/example_intro_to_cs.yaml
```

## מבנה הפרויקט

```
├── course_summary_agent/
│   ├── __init__.py       # Package init
│   ├── agent.py          # Core agent logic
│   ├── cli.py            # CLI interface
│   ├── models.py         # Data models
│   └── prompts.py        # Prompt templates
├── courses/              # Course YAML files
│   ├── example_intro_to_cs.yaml
│   └── example_data_science.yaml
├── output/               # Generated summaries
├── requirements.txt
└── README.md
```
