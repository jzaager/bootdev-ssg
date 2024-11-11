from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        split_nodes = []
        sections = node.text.split(delimiter)

        # ensure closing delimiter is provided
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown syntax: no closing delimiter provided")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
                
            # odd sections are text while even are what
            # was split between the delimiters
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)
    return new_nodes
