"""CLI interface for the course summary agent."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .agent import CourseSummaryAgent
from .models import SummaryType

console = Console()

SUMMARY_TYPE_LABELS = {
    "full": ("סיכום מלא", "Full summary"),
    "topic": ("סיכום לפי נושא", "Per-topic summary"),
    "key_concepts": ("מושגי מפתח", "Key concepts"),
    "exam_prep": ("הכנה למבחן", "Exam preparation"),
}


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Course Summary Agent - AI-powered course summary generator."""
    pass


@cli.command()
@click.argument("course_file", type=click.Path(exists=True))
@click.option(
    "--type", "-t",
    "summary_type",
    type=click.Choice(["full", "topic", "key_concepts", "exam_prep"]),
    default="full",
    help="Type of summary to generate",
)
@click.option("--topic", "-n", "topic_name", help="Specific topic name (for topic summary type)")
@click.option("--output", "-o", "output_dir", default="output", help="Output directory")
@click.option("--api-key", "-k", envvar="ANTHROPIC_API_KEY", help="Anthropic API key")
@click.option("--model", "-m", default="claude-sonnet-4-20250514", help="Model to use")
def generate(course_file, summary_type, topic_name, output_dir, api_key, model):
    """Generate a course summary from a YAML course file."""
    try:
        agent = CourseSummaryAgent(api_key=api_key, model=model)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)

    course = agent.load_course(course_file)

    st = SummaryType(summary_type)
    label_he, label_en = SUMMARY_TYPE_LABELS[summary_type]

    console.print(Panel(
        f"[bold]{course.name}[/bold]\n{label_he} / {label_en}",
        title="Course Summary Agent",
    ))

    if st == SummaryType.TOPIC and topic_name is None:
        if course.topics:
            _show_topics_table(course)
            topic_name = click.prompt("Enter topic name")
        else:
            console.print("[yellow]No topics defined and no topic name provided. Generating per-topic summary.[/yellow]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Generating summary...", total=None)
        output_path = agent.generate_and_save(course, st, output_dir, topic_name)

    console.print(f"\n[green]Summary saved to: {output_path}[/green]")


@cli.command()
@click.argument("course_file", type=click.Path(exists=True))
@click.option("--api-key", "-k", envvar="ANTHROPIC_API_KEY", help="Anthropic API key")
@click.option("--model", "-m", default="claude-sonnet-4-20250514", help="Model to use")
def chat(course_file, api_key, model):
    """Start an interactive chat session about a course."""
    try:
        agent = CourseSummaryAgent(api_key=api_key, model=model)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)

    course = agent.load_course(course_file)

    console.print(Panel(
        f"[bold]{course.name}[/bold]\nInteractive Mode",
        title="Course Summary Agent",
    ))

    agent.interactive_session(course)


@cli.command()
@click.argument("course_file", type=click.Path(exists=True))
def info(course_file):
    """Display information about a course file."""
    agent = CourseSummaryAgent.__new__(CourseSummaryAgent)
    course = agent.load_course(course_file)

    console.print(Panel(f"[bold]{course.name}[/bold]", title="Course Info"))

    if course.description:
        console.print(f"\n{course.description}\n")
    if course.instructor:
        console.print(f"Instructor: {course.instructor}")
    if course.target_audience:
        console.print(f"Target audience: {course.target_audience}")
    if course.prerequisites:
        console.print(f"Prerequisites: {', '.join(course.prerequisites)}")

    if course.topics:
        console.print()
        _show_topics_table(course)


def _show_topics_table(course):
    table = Table(title="Topics")
    table.add_column("#", style="cyan", width=4)
    table.add_column("Name", style="bold")
    table.add_column("Subtopics", style="dim")
    table.add_column("Key Concepts", style="dim")

    for i, topic in enumerate(course.topics, 1):
        table.add_row(
            str(i),
            topic.name,
            str(len(topic.subtopics)),
            str(len(topic.key_concepts)),
        )

    console.print(table)


def main():
    cli()


if __name__ == "__main__":
    main()
