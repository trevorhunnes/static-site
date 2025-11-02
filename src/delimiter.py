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
