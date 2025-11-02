from textnode import TextType
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode
from delimiter import split_nodes_delimiter


def main():
    node = TextNode("**", TextType.TEXT)
    print(split_nodes_delimiter([node], "`", TextType.CODE))


main()
