# md2html

[![CI](https://github.com/amalmurali47/md2html/actions/workflows/ci.yml/badge.svg)](https://github.com/amalmurali47/md2html/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Simple, fast markdown to HTML converter with no dependencies beyond the Python standard library and the `markdown` package.

## Features

- Clean, minimal CLI interface
- Supports GitHub Flavored Markdown (tables, fenced code blocks, etc.)
- Smart output path defaults (`file.md` → `file.html`)
- Pipe-friendly (stdin/stdout support)
- Type-safe with comprehensive test coverage

## Installation

```bash
pip install .
```

Or for development:

```bash
pip install -e .[dev,test]
```

## Usage

```bash
# Convert file with automatic output naming
md2html input.md                    # Creates input.html

# Convert with custom output
md2html input.md output.html

# Convert from stdin to stdout
cat input.md | md2html - -

# Convert from stdin to file
cat input.md | md2html

# Use as Python module
python -m md2html input.md
```

## Examples

**Input** (`example.md`):

```markdown
# My Document

This is a **bold** statement with a [link](https://example.com).

## Code Example

```python
print("Hello, world!")
```

| Feature | Status |
|---------|--------|
| Tables  | ✅     |
| Code    | ✅     |


**Output** (`example.html`):

```html
<h1>My Document</h1>
<p>This is a <strong>bold</strong> statement with a <a href="https://example.com">link</a>.</p>
<h2>Code Example</h2>
<pre><code class="language-python">print("Hello, world!")
</code></pre>
<table>
<thead>
<tr>
<th>Feature</th>
<th>Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>Tables</td>
<td>✅</td>
</tr>
<tr>
<td>Code</td>
<td>✅</td>
</tr>
</tbody>
</table>
```

## Supported Markdown Extensions

- **Attribute Lists**: Add CSS classes and IDs
- **Fenced Code Blocks**: Syntax highlighting support
- **Tables**: GitHub-style tables
- **Table of Contents**: Auto-generated TOC
- **SmartyPants**: Smart quotes and dashes

## Development

```bash
# Run tests
pytest

# Run linting
ruff check .
ruff format .

# Type checking
mypy md2html.py
```

## License

MIT License - see [LICENSE](LICENSE) file for details.
