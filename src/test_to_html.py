import unittest

from to_html import markdown_to_html_node


class TestToHTML(unittest.TestCase):
    def test_to_html_unordered_list(self):
        markdown = """
# Blog Post 1: The advent of Recurring Dinosaurs

## Table of Contents

- Why want dinosaur recurrence
- How to combat infernal recursion?
- You cannot stop us

"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>Blog Post 1: The advent of Recurring Dinosaurs</h1><h2>Table of Contents</h2><ul><li>Why want dinosaur recurrence</li><li>How to combat infernal recursion?</li><li>You cannot stop us</li></ul></div>",
        )

    def test_to_html_ordered_list(self):
        markdown = """
# Blog Post 1: The advent of Recurring Dinosaurs

## Table of Contents

1. Why want dinosaur recurrence
2. How to combat infernal recursion?
3. You cannot stop us

"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>Blog Post 1: The advent of Recurring Dinosaurs</h1><h2>Table of Contents</h2><ol><li>Why want dinosaur recurrence</li><li>How to combat infernal recursion?</li><li>You cannot stop us</li></ol></div>",
        )

    def test_to_html_quote(self):
        markdown = """
## Disclaimer

The following quote is **not** to be taken for granted:

> Dinosaurs are really bad back-scratchers
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h2>Disclaimer</h2><p>The following quote is <b>not</b> to be taken for granted:</p><blockquote>Dinosaurs are really bad back-scratchers</blockquote></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
