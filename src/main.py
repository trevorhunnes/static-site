from textnode import TextType
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode


def main():
    html_node = HTMLNode(
        props={
            "href": "https://www.google.com",
            "target": "_blank",
        }
    )
    print(html_node)


main()
