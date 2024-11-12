import unittest

from textnode import TextNode, TextType
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):

    print("\nTESTING SplitNodes...")
    print("=================\n")

    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_invalid_markdown(self):
        node = TextNode(
            "This is text with *improper markdown",
            TextType.TEXT
        )
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            str(context.exception),
            "Invalid markdown syntax: no closing delimiter provided"
        )

class TestRegexExtractions(unittest.TestCase):

    print("\nTESTING RegexExtractions...")
    print("=================\n")

    # START image extraction tests
    def test_single_image_extraction(self):
        text = "This is text with a single ![image](https://google.com)"
        self.assertEqual(
            extract_markdown_images(text),
            [("image", "https://google.com")]
        )

    def test_double_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_image_with_link_extraction(self):
        text = "This is text with a [link](http://boot.dev) and an ![image](https://google.com)"
        self.assertEqual(
            extract_markdown_images(text),
            [("image", "https://google.com")]
        )

    def test_image_between_links_extraction(self):
        text = "This is text with a [link](http://boot.dev) and an ![image](https://google.com) and another [link](https://yahoo.com) and another ![image2](https://aol.com)"
        self.assertEqual(
            extract_markdown_images(text),
            [("image", "https://google.com"), ("image2", "https://aol.com")]
        )

    def test_no_image_to_extract(self):
        text = "Here is text without any image! [sneaky link](boot.dev)"
        self.assertEqual(
            extract_markdown_images(text),
            []
        )

    # START link extraction tests
    def test_link_extraction(self):
        text = "This is text with a single [link](https://google.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://google.com")]
        )

    def test_double_link_extraction(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_links(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_link_with_image_extraction(self):
        text = "This is text with an ![image](http://boot.dev) and a [link](https://google.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://google.com")]
        )

    def test_link_between_images_extraction(self):
        text = "This is text with an ![image](http://boot.dev) and a [link](https://google.com) and another ![image](https://yahoo.com) and another [link2](https://aol.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://google.com"), ("link2", "https://aol.com")]
        )

    def test_no_link_to_extract(self):
        text = "Here is text without any link! ![sneaky image](boot.dev)"
        self.assertEqual(
            extract_markdown_links(text),
            []
        )

if __name__ == "__main__":
    unittest.main()
