from enum import Enum
import re

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
    for i,line in enumerate(block.split('\n')):
        if not line.startswith(f"{i+1}. "):
            return False
    return True
