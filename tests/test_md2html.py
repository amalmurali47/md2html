from io import StringIO
from unittest.mock import patch

import pytest

from md2html import (
    convert_markdown_to_html,
    get_default_output_path,
    main,
    read_input,
    write_output,
)


class TestMarkdownConversion:
    """Test markdown to HTML conversion functionality."""

    def test_convert_basic_markdown(self):
        """Test basic markdown conversion"""
        markdown_text = "# Header\n\nThis is a paragraph."
        html = convert_markdown_to_html(markdown_text)
        assert '<h1 id="header">Header</h1>' in html
        assert "<p>This is a paragraph.</p>" in html

    def test_convert_headers(self):
        """Test header conversion"""
        markdown_text = "# H1\n## H2\n### H3"
        html = convert_markdown_to_html(markdown_text)
        assert '<h1 id="h1">H1</h1>' in html
        assert '<h2 id="h2">H2</h2>' in html
        assert '<h3 id="h3">H3</h3>' in html

    def test_convert_links(self):
        """Test link conversion"""
        markdown_text = "[Link text](https://example.com)"
        html = convert_markdown_to_html(markdown_text)
        assert '<a href="https://example.com">Link text</a>' in html

    def test_convert_emphasis(self):
        """Test emphasis conversion"""
        markdown_text = "*italic* and **bold**"
        html = convert_markdown_to_html(markdown_text)
        assert "<em>italic</em>" in html
        assert "<strong>bold</strong>" in html

    def test_convert_lists(self):
        """Test list conversion"""
        markdown_text = "- Item 1\n- Item 2\n- Item 3"
        html = convert_markdown_to_html(markdown_text)
        assert "<ul>" in html
        assert "<li>Item 1</li>" in html
        assert "<li>Item 2</li>" in html
        assert "<li>Item 3</li>" in html

    def test_convert_code(self):
        """Test code conversion"""
        markdown_text = "`inline code`\n\n```\ncode block\n```"
        html = convert_markdown_to_html(markdown_text)
        assert "<code>inline code</code>" in html
        assert "<pre><code>code block" in html

    def test_convert_tables(self):
        """Test table conversion"""
        markdown_text = (
            "| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |"
        )
        html = convert_markdown_to_html(markdown_text)
        assert "<table>" in html
        assert "<th>Header 1</th>" in html
        assert "<td>Cell 1</td>" in html

    def test_empty_input(self):
        """Test empty input"""
        html = convert_markdown_to_html("")
        assert html == ""


class TestUtilityFunctions:
    """Test utility functions."""

    def test_get_default_output_path_with_input(self):
        """Test default output path generation from input file"""
        assert get_default_output_path("test.md") == "test.html"
        assert get_default_output_path("path/to/file.md") == "path/to/file.html"
        assert get_default_output_path("file.txt") == "file.html"

    def test_get_default_output_path_stdin(self):
        """Test default output path for stdin"""
        assert get_default_output_path(None) == "out.html"
        assert get_default_output_path("-") == "out.html"

    def test_read_input_stdin(self):
        """Test reading from stdin"""
        test_input = "# Test\n\nContent"
        with patch("sys.stdin", StringIO(test_input)):
            result = read_input(None)
            assert result == test_input

        with patch("sys.stdin", StringIO(test_input)):
            result = read_input("-")
            assert result == test_input

    def test_read_input_file(self, tmp_path):
        """Test reading from file"""
        test_file = tmp_path / "test.md"
        test_content = "# Test File\n\nContent"
        test_file.write_text(test_content)

        result = read_input(str(test_file))
        assert result == test_content

    def test_read_input_file_not_found(self):
        """Test reading non-existent file"""
        with pytest.raises(FileNotFoundError):
            read_input("nonexistent.md")

    def test_write_output_stdout(self, capsys):
        """Test writing to stdout"""
        test_html = "<h1>Test</h1>"
        write_output(test_html, "-")
        captured = capsys.readouterr()
        assert captured.out.strip() == test_html

    def test_write_output_file(self, tmp_path):
        """Test writing to file"""
        test_html = "<h1>Test</h1>"
        output_file = tmp_path / "output.html"

        write_output(test_html, str(output_file))

        assert output_file.exists()
        assert output_file.read_text() == test_html


class TestMainFunction:
    """Test main CLI function."""

    def test_main_with_file_input(self, tmp_path):
        """Test main function with file input"""
        input_file = tmp_path / "input.md"
        output_file = tmp_path / "output.html"

        input_file.write_text("# Test Header\n\nTest paragraph.")

        with patch("sys.argv", ["md2html", str(input_file), str(output_file)]):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called_with(f"Converted to {output_file}")

        assert output_file.exists()
        html_content = output_file.read_text()
        assert '<h1 id="test-header">Test Header</h1>' in html_content
        assert "<p>Test paragraph.</p>" in html_content

    def test_main_with_stdin(self, tmp_path, monkeypatch):
        """Test main function with stdin input"""
        markdown_input = "# Stdin Test\n\nFrom stdin."

        monkeypatch.chdir(tmp_path)

        with patch("sys.argv", ["md2html"]):
            with patch("sys.stdin", StringIO(markdown_input)):
                with patch("builtins.print") as mock_print:
                    main()
                    mock_print.assert_called_with("Converted to out.html")

        output_file = tmp_path / "out.html"
        assert output_file.exists()
        html_content = output_file.read_text()
        assert '<h1 id="stdin-test">Stdin Test</h1>' in html_content
        assert "<p>From stdin.</p>" in html_content

    def test_main_stdout_output(self, capsys):
        """Test main function with stdout output"""
        markdown_input = "# Test\n\nContent"

        with patch("sys.argv", ["md2html", "-", "-"]):
            with patch("sys.stdin", StringIO(markdown_input)):
                main()

        captured = capsys.readouterr()
        assert '<h1 id="test">Test</h1>' in captured.out
        assert "<p>Content</p>" in captured.out

    def test_main_file_not_found(self, capsys):
        """Test main function with non-existent file"""
        with patch("sys.argv", ["md2html", "nonexistent.md"]):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        assert "Error: File 'nonexistent.md' not found" in captured.err

    def test_main_help(self):
        """Test help message"""
        with patch("sys.argv", ["md2html", "--help"]):
            with pytest.raises(SystemExit):
                main()

    def test_main_default_output_path(self, tmp_path):
        """Test main function with default output path"""
        input_file = tmp_path / "test.md"
        expected_output = tmp_path / "test.html"

        input_file.write_text("# Test\n\nContent")

        with patch("sys.argv", ["md2html", str(input_file)]):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called_with(f"Converted to {expected_output}")

        assert expected_output.exists()
        html_content = expected_output.read_text()
        assert '<h1 id="test">Test</h1>' in html_content
