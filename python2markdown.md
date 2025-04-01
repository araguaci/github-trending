## Install the Library

```
pip install markdownify
```

## Python script that takes an HTML string and converts it to Markdown:

```
from markdownify import markdownify

# Example HTML content
html = """
<h1>Hello, World!</h1>
<p>This is a <strong>bold</strong> statement with a <a href="https://example.com">link</a>.</p>
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
</ul>
"""

# Convert HTML to Markdown
markdown = markdownify(html)

# Print the result
print(markdown)
```
