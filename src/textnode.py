from ast import Call
from enum import Enum
import re

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode():

    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode('b', text_node.text, None)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text, None)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {
                "src": text_node.url,
                "alt": text_node.text
            })
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delim_found = False
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(old_nodes)
        elif delimiter in node.text:
            delim_found = True
            nodes = node.text.split(delimiter)
            if len(nodes) % 2 == 0:
                raise Exception("Invalid markdown, formatted section is not closed")
            split_nodes = []
            for i in range(len(nodes)):
                if nodes[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(nodes[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(nodes[i], text_type))

            new_nodes.extend(split_nodes)
    if not delim_found:
        raise Exception("No delimiter existed within the TextNodes")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        found_links = extract_markdown_links(node.text)
        if not found_links:
            new_nodes.append(node)
        node_text = node.text
        sections = None
        for link in found_links:
            (link_alt, link) = link
            sections = node_text.split(f"[{link_alt}]({link})")
            if len(sections) == 2:
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                node_text = sections[1]
            new_nodes.append(TextNode(link_alt, TextType.LINK, link))

        if sections and len(sections) > 1 and sections[1] != "":
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        found_images = extract_markdown_images(node.text)
        if not found_images:
            new_nodes.append(node)
        node_text = node.text
        sections = None
        for pic in found_images:
            (pic_alt, pic_link) = pic
            sections = node_text.split(f"![{pic_alt}]({pic_link})")
            if len(sections) == 2:
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                node_text = sections[1]
            new_nodes.append(TextNode(pic_alt, TextType.IMAGE, pic_link))

        if sections and len(sections) > 1 and sections[1] != "":
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes

def split_nodes_on():
    pass