import re
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)
from delimiter import (
    text_to_textnodes,
)
from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)
from textnode import (
    TextType,
    text_node_to_html_node,
    TextNode,
)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            block = block[2:]
            block = " ".join(block.split())
            return block
    raise Exception("no title")


def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type is BlockType.PARAGRAPH:
            norm_block = " ".join(block.split())
            html_nodes.append(ParentNode("p", text_to_children(norm_block)))
        if block_type is BlockType.HEADING:
            tag = get_heading(block)
            block = block[tag+1:]
            html_nodes.append(ParentNode(f"h{tag}", text_to_children(block)))
        if block_type is BlockType.QUOTE:
            block = block.replace(">", "")
            block = " ".join(block.split())
            html_nodes.append(ParentNode(
                "blockquote", text_to_children(block)))
        if block_type is BlockType.CODE:
            lines = block.splitlines()
            lines = lines[1:-1]
            block = "\n".join(lines) + "\n"
            node = TextNode(block, TextType.TEXT)
            html_nodes.append(
                ParentNode("pre", [ParentNode(
                    "code", [text_node_to_html_node(node)])])
            )
        if block_type is BlockType.OLIST:
            html_nodes.append(ParentNode(
                "ol", list_to_children(block, block_type)))
        if block_type is BlockType.ULIST:
            html_nodes.append(ParentNode(
                "ul", list_to_children(block, block_type)))
    return ParentNode("div", html_nodes)


def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def get_heading(text):
    level = 0
    for char in text:
        if char == "#":
            level += 1
        else:
            break
    return level


def list_to_children(text, block_type):
    html_nodes = []
    items = text.split("\n")
    for item in items:
        if block_type is BlockType.ULIST:
            item = item[2:]
        if block_type is BlockType.OLIST:
            item = re.sub(r'^\d+\.\s*', "", item)
        item = item.strip()
        if item == "":
            continue
        item = " ".join(item.split())
        children_nodes = []
        text_node = text_to_textnodes(item)
        for node in text_node:
            children_nodes.append(text_node_to_html_node(node))
        html_nodes.append(ParentNode("li", children_nodes))
    return html_nodes
