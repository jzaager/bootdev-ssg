import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):

    print("\nTESTING HTMLNode...")
    print("=================\n")

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "boot.dev"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="boot.dev"',
        )

    def test_values(self):
        node = HTMLNode("div", "4 score and 7 years...")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "4 score and 7 years...")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode(
            "p",
            "Use the force",
            None,
            {"class": "primary"}
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, Use the force, children: None, {'class': 'primary'})"
        )

class TestLeafNode(unittest.TestCase):

    print("\nTESTING LeafNode...")
    print("=================\n")

    def test_values(self):
        node = LeafNode(
            "div",
            "This is my div, song",
            {'class': 'secondary'}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "This is my div, song")
        self.assertEqual(node.props_to_html(), ' class="secondary"')
        self.assertEqual(node.children, None)

    def test_to_html(self):
        node_no_value = LeafNode(
            "a",
            None,
            {'href': 'boot.dev'}
        )
        self.assertRaises(ValueError, node_no_value.to_html)

        node_no_tag = LeafNode(
            None,
            "Value without a tag",
            None
        )
        self.assertEqual(node_no_tag.to_html(), node_no_tag.value)

        node = LeafNode(
            "p",
            "A full HTML leaf node!",
            {'class': 'fw_bold'}
        )
        self.assertEqual(
            node.to_html(),
            f'<p class="fw_bold">A full HTML leaf node!</p>'
        )

class TestParentNode(unittest.TestCase):

    print("\nTESTING ParentNode...")
    print("=================\n")

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        node_no_tag = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertRaises(ValueError, node_no_tag.to_html)

        node_no_children = ParentNode("div", None)
        self.assertRaises(ValueError, node_no_children.to_html)

        node_nested_parents = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [LeafNode("b", "Bold text")],
                    {"class": "nested-parent-node"}
                ),
                LeafNode("i", "italic text", {"class": "nested-leaf"}),
                LeafNode(None, "Normal text")
            ],
            {"class": "parent-node"}
        )
        self.assertEqual(
            node_nested_parents.to_html(),
            f'<div class="parent-node"><p class="nested-parent-node"><b>Bold text</b></p><i class="nested-leaf">italic text</i>Normal text</div>'
        )

    def test_repr(self):
        node = ParentNode(
            "input",
            [
                LeafNode("b", "Bold text"),
            ],
            {"class": "parent-input"}
        )
        self.assertEqual(
            node.__repr__(),
            "ParentNode(input, children: [LeafNode(b, Bold text, None)], {'class': 'parent-input'})"
        )

class TestTextToHtmlNode(unittest.TestCase):

    print("\nTESTING TextToHtmlNode...")
    print("=================\n")

    def test_TEXT(self):
        text_node = TextNode("TEXT node", TextType.TEXT, None)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "TEXT node")
        self.assertEqual(html_node.props, None)

    def test_BOLD(self):
        text_node = TextNode("BOLD node", TextType.BOLD, None)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "BOLD node")
        self.assertEqual(html_node.props, None)

    def test_ITALIC(self):
        text_node = TextNode("ITALIC node", TextType.ITALIC, None)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "ITALIC node")
        self.assertEqual(html_node.props, None)

    def test_LINK(self):
        text_node = TextNode("LINK node", TextType.LINK, "http://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "LINK node")
        self.assertEqual(html_node.props, {'href': 'http://boot.dev'})

    def test_IMAGE(self):
        text_node = TextNode("IMAGE node", TextType.IMAGE, "unsplash.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {'src': 'unsplash.com', 'alt': 'IMAGE node'}
        )




if __name__ == "__main__":
    unittest.main()
