import unittest

from block_markdown import BlockType, block_to_blocktype, markdown_to_blocks, unordered_list_to_html_node
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
        result = unordered_list_to_html_node(block)
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
        result = unordered_list_to_html_node(block)
        self.assertEqual(
            result.to_html(),
          "<ul><li>This <b>is</b></li><li>That</li><li>Another</li></ul>",
            result
        )
