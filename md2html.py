"""Simple markdown to HTML converter using the Python markdown library."""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    import markdown
except ImportError:
    print(
        "Error: markdown library not found. Install with: pip install markdown",
        file=sys.stderr,
    )
    sys.exit(1)


def convert_markdown_to_html(markdown_text: str) -> str:
    """Convert markdown text to HTML using the markdown library.

    Args:
        markdown_text: The markdown content to convert

    Returns:
        HTML string
    """
    md = markdown.Markdown(
        extensions=["attr_list", "fenced_code", "tables", "toc", "smarty"]
    )
    result = md.convert(markdown_text)
    # The markdown library returns str, but mypy can't infer this
    return str(result)


def get_default_output_path(input_path: Optional[str]) -> str:
    """Get default output path based on input path.

    Args:
        input_path: Path to input file, or None for stdin

    Returns:
        Default output file path
    """
    if input_path and input_path != "-":
        return str(Path(input_path).with_suffix(".html"))
    return "out.html"


def read_input(input_path: Optional[str]) -> str:
    """Read markdown content from file or stdin.

    Args:
        input_path: Path to input file, or None for stdin

    Returns:
        Markdown content as string

    Raises:
        FileNotFoundError: If input file doesn't exist
        IOError: If file can't be read
    """
    if not input_path or input_path == "-":
        return sys.stdin.read()

    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"File '{input_path}' not found")

    return path.read_text(encoding="utf-8")


def write_output(html: str, output_path: str) -> None:
    """Write HTML content to file or stdout.

    Args:
        html: HTML content to write
        output_path: Path to output file, or '-' for stdout

    Raises:
        IOError: If file can't be written
    """
    if output_path == "-":
        print(html)
    else:
        Path(output_path).write_text(html, encoding="utf-8")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert markdown to HTML",
        epilog='Use "-" for stdin/stdout. Examples:\n'
        "  md2html file.md\n"
        "  md2html file.md output.html\n"
        "  cat file.md | md2html - -",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input",
        nargs="?",
        help='Input markdown file (default: stdin, use "-" explicitly)',
    )
    parser.add_argument(
        "output",
        nargs="?",
        help='Output HTML file (default: derived from input, use "-" for stdout)',
    )

    args = parser.parse_args()

    # Determine output path
    if args.output is None:
        output_path = get_default_output_path(args.input)
    else:
        output_path = args.output

    try:
        # Read input
        markdown_text = read_input(args.input)

        # Convert to HTML
        html = convert_markdown_to_html(markdown_text)

        # Write output
        write_output(html, output_path)

        if output_path != "-":
            print(f"Converted to {output_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
