import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:

        if node.text_type == TextType.TEXT:
            temp = node.text.split(delimiter)

            if len(temp) % 2 == 0:
                raise Exception("invalid Markdown syntax")

            temp_nodes = []
            is_text = True

            for i in temp:

                if len(i) > 0 or is_text is False:

                    if is_text:
                        temp_nodes.append(TextNode(i, TextType.TEXT))

                    else:
                        temp_nodes.append(TextNode(i, text_type))

                is_text = not is_text

            new_nodes.extend(temp_nodes)

        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            text = node.text
            for image in images:
                sections = text.split(f"![{image[0]}]({image[1]})", 1)
                text = sections[1]
                if len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            text = node.text
            for link in links:
                sections = text.split(f"[{link[0]}]({link[1]})", 1)
                text = sections[1]
                if len(sections[0]) > 0:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes


def text_to_textnodes(text):
    new_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([new_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes
