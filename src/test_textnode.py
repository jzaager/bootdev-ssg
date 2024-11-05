import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "http.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_method(self):
        node = TextNode("This is a text node", TextType.BOLD, "http.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "http.boot.dev")
        self.assertTrue(node.__eq__(node2))

    def test_url_is_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "http.boot.dev")
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.CODE, "http.boot.dev")
        self.assertEqual(
            node.__repr__(),
            "TextNode(This is a text node, code, http.boot.dev)"
        )

    if __name__ == "__main__":
        unittest.main()
