import re

from textnode import TextNode, TextType


# takes raw MD and returns a list of tuples based on image syntax: [(alt text, URL), (alt2, URL2)]
# "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# takes raw MD and returns a list of tuples based on link syntax: [(anchor text, URL), (anchor text2, URL2)]
# "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
# [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# converts MD TextNodes to bold, italic, or code types
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
