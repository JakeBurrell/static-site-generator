from enum import Enum
import re

from htmlnode import LeafNode, ParentNode
from textnode import create_to_textnodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

def block_to_blocktype(block) -> BlockType:
    if is_heading(block):
        return BlockType.HEADING
    if is_code(block):
        return BlockType.CODE
    if is_quote(block):
        return BlockType.QUOTE
    if is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def heading_to_htmlnode(text):
    heading_number = text.count("#")
    heading_text = text.split(" ", 1)[1]
    heading_text_nodes = create_to_textnodes(heading_text)
    heading_html_nodes = [text_node_to_html_node(node) for node in heading_text_nodes]
    return ParentNode(f"h{heading_number}", heading_html_nodes )

def paragraph_to_html_node(text):
    para_text_nodes = create_to_textnodes(text)
    para_html_nodes = [text_node_to_html_node(node) for node in para_text_nodes]
    return ParentNode("p", para_html_nodes)

def code_to_html_node(text):
    code_text = '\n'.join(text.split('\n')[1:-1])
    return ParentNode("pre", [LeafNode("code", code_text)])

def quote_to_html_node(text):
    quote_text = "\n".join([quote[-1:] for quote in text.split("\n")])
    quote_text_nodes = create_to_textnodes(quote_text)
    quote_html_nodes = [text_node_to_html_node(node) for node in quote_text_nodes]
    return ParentNode("blockquote", quote_html_nodes)

def unordered_list_to_html_node(text):
    unordered_list = [list_item.split(" ", 1)[1] for list_item in text.split("\n")]
    unordered_list_nodes = [create_to_textnodes(list_item) for list_item in unordered_list]
    unordered_list_html_nodes = [[text_node_to_html_node(node) 
        for node in list_item_nodes] 
    for list_item_nodes in unordered_list_nodes]
    return ParentNode('ul', [ParentNode('li', list_item_nodes) 
        for list_item_nodes in unordered_list_html_nodes])

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        match (block_type):
            case BlockType.HEADING:
                block_nodes.append(heading_to_htmlnode(block))
            case BlockType.PARAGRAPH:
                block_nodes.append(paragraph_to_html_node(block))
            case BlockType.CODE:
                block_nodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                block_nodes.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                block_nodes.append()


def is_heading(block) -> bool:
    heading_pattern = re.compile(r"#{1,6} [\d\w ]+")
    if heading_pattern.fullmatch(block):
        return True
    return False


def is_code(block) -> bool:
    return block.startswith('```') and block.endswith('```')


def is_quote(block) -> bool:
    for line in block.split('\n'):
        if not line.startswith(">"):
            return False
    return True


def is_unordered_list(block) -> bool:
    for line in block.split('\n'):
        if not line.startswith("- "):
            return False
    return True


def is_ordered_list(block) -> bool:
    for i, line in enumerate(block.split('\n'), 1):
        if not line.startswith(f"{i}. "):
            return False
    return True
