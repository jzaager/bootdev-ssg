import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    print("\nTESTING...")
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
        node = HTMLNode(
            "div",
            "4 score and 7 years..."
        )
        self.assertEqual(
            node.tag,
            "div"
        )
        self.assertEqual(
            node.value,
            "4 score and 7 years..."
        )
        self.assertEqual(
            node.children,
            None
        )
        self.assertEqual(
            node.props,
            None
        )

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

    if __name__ == "__main__":
        unittest.main()
