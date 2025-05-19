import unittest

from block_markdown import BlockType, block_to_blocktype, extract_title, markdown_to_blocks, list_to_html_node, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
             blocks,
             [
                 "This is **bolded** paragraph",
                 "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                 "- This is a list\n- with items",
             ],
        )

    def test_markdown_to_blocks_v2(self):
        md = """
This is **bolded** paragraph


    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
             blocks,
             [
                 "This is **bolded** paragraph",
                 "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                 "- This is a list\n- with items",
             ],
        )

    def test_markdown_to_blocks_tab(self):
        md = """
This is **bolded** paragraph


    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertNotEqual(
             blocks,
             [
                 "This is **bolded** paragraph",
                 "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                 "- This is a list\n- with items",
             ],
        )

    def test_block_to_blocktype_heading(self):
        block = "# Hello"
        self.assertEqual(
            block_to_blocktype(block),
            BlockType.HEADING
        )

    def test_block_to_blocktype_code(self):
        block = "``` Some Code ```"
        self.assertEqual(
            block_to_blocktype(block),
            BlockType.CODE
        )


    def test_block_to_blocktype_quote(self):
        block = "> hello\n>They"
        self.assertEqual(
            block_to_blocktype(block),
            BlockType.QUOTE
        )


    def test_block_to_blocktype_unordered_list(self):
        block = '''
- This
- That
- More of that
                '''.strip()
        self.assertEqual(
            block_to_blocktype(block),
            BlockType.UNORDERED_LIST,
            block
        )

    def test_block_to_blocktype_ordered_list(self):
        block = '''
1. This
2. That
3. More of that
                '''.strip()
        self.assertEqual(
            block_to_blocktype(block),
            BlockType.ORDERED_LIST,
            block
        )

    def test_block_to_blocktype_ordered_list_failure(self):
        block = '''
1. This
4. That
3. More of that
                '''.strip()
        self.assertEqual(
            block_to_blocktype(block),
            BlockType.PARAGRAPH,
            block
        )

    def test_unordered_list_to_html_node(self):
        block = '''
- This is
- That
- Another
        '''.strip()
        result = list_to_html_node('ul', block)
        self.assertEqual(
            result.to_html(),
          "<ul><li>This is</li><li>That</li><li>Another</li></ul>",
            result
        )

    def test_unordered_list_to_html_node_bold(self):
        block = '''
- This **is**
- That
- Another
        '''.strip()
        result = list_to_html_node("ul",block)
        self.assertEqual(
            result.to_html(),
          "<ul><li>This <b>is</b></li><li>That</li><li>Another</li></ul>",
            result
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
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(
            html,
            expected
        )

    def test_all_blocks(self):
        md = """
## New heading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

Ordered list

1. Item one
2. Item two added

Unordered List

- items
- item Another

Quote blocks

> Hello
> This is a quote

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>New heading</h2><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><p>Ordered list</p><ol><li>Item one</li><li>Item two added</li></ol><p>Unordered List</p><ul><li>items</li><li>item Another</li></ul><p>Quote blocks</p><blockquote>Hello\nThis is a quote</blockquote></div>"
        )

    def test_extract_title(self):

        md = """
# New heading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
           """
        result = extract_title(md)
        self.assertEqual(
            result,
            'New heading'
        )

    def test_extract_title_no_title(self):

        md = """
## New heading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
           """
        result = extract_title(md)
        self.assertEqual(
            result,
            None
        )
