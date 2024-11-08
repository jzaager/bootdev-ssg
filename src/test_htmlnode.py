import unittest

from htmlnode import HTMLNode, LeafNode


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

class TestLeafNode(unittest.TestCase):

    print("\nTESTING LeafNode...")
    print("=================\n")

    def test_values(self):
        node = LeafNode(
            "div",
            "This is my div, song",
            {'class': 'secondary'}
        )
        self.assertEqual(
            node.tag,
            "div"
        )
        self.assertEqual(
            node.value,
            "This is my div, song",
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="secondary"'
        )
        self.assertEqual(
            node.children,
            None
        )

    def test_to_html(self):
        node_no_value = LeafNode(
            "a",
            None,
            {'href': 'boot.dev'}
        )
        self.assertRaises(
            ValueError,
            node_no_value.to_html
        )

        node_no_tag = LeafNode(
            None,
            "Value without a tag",
            None
        )
        self.assertEqual(
            node_no_tag.to_html(),
            node_no_tag.value
        )

        node = LeafNode(
            "p",
            "A full HTML leaf node!",
            {'class': 'fw_bold'}
        )
        self.assertEqual(
            node.to_html(),
            f'<p class="fw_bold">A full HTML leaf node!</p>'
        )

if __name__ == "__main__":
    unittest.main()
