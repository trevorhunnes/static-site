from textnode import TextType
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode
from delimiter import split_nodes_delimiter, split_nodes_image, text_to_textnodes
from block_markdown import (
    block_to_block_type
)


def main():
    print(block_to_block_type("*** Heading"))


main()
