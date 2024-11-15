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

# convert MD text nodes to text+image nodes 
def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        # format == [(alt_text, link), (alt2, link2)...]
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        original_text = node.text
        for alt_text, link in images:
            # split the original_text on the markdown ![image](link) syntax, max once
            sections = original_text.split(f"![{alt_text}]({link})", maxsplit=1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if sections[0] == "":
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=link))
            else:
                new_nodes.extend([
                    TextNode(sections[0], TextType.TEXT),
                    TextNode(alt_text, TextType.IMAGE, url=link)
                ])
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

# convert MD text nodes to text+link nodes 
def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        # format == [(text, link), (text2, link2)...]
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            continue

        original_text = node.text
        for text, link in links:
            # split the original_text on the markdown [text](link) syntax, max once
            sections = original_text.split(f"[{text}]({link})", maxsplit=1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if sections[0] == "":
                new_nodes.append(TextNode(text, TextType.LINK, url=link))
            else:
                new_nodes.extend([
                    TextNode(sections[0], TextType.TEXT),
                    TextNode(text, TextType.LINK, url=link)
                ])
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


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


def text_to_text_nodes(text):
    final_nodes = [TextNode(text, TextType.TEXT)]

    final_nodes = split_nodes_delimiter(final_nodes, "**", TextType.BOLD)
    final_nodes = split_nodes_delimiter(final_nodes, "*", TextType.ITALIC)
    final_nodes = split_nodes_delimiter(final_nodes, "`", TextType.CODE)
    final_nodes = split_nodes_image(final_nodes)
    final_nodes = split_nodes_link(final_nodes)

    return final_nodes


