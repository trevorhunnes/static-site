from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    text = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("- "):
        is_list = True
        for i in text:
            if not i.startswith("- "):
                is_list = False
                break
        if is_list:
            return BlockType.ULIST
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        is_quote = True
        for i in text:
            if not i.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
    if block.startswith("1. "):
        is_ordered_list = True
        for i in range(len(text)):
            if not text[i].startswith(f"{i+1}. "):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.OLIST
    return BlockType.PARAGRAPH
