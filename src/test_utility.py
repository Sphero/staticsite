import unittest

from textnode import *
from utility import *


class TestMain(unittest.TestCase):

    def test_textohtml(self):
        textnode = TextNode(text="This is a text", text_type=TextType.TEXT)
        boldnode = TextNode(text="This is a bold text", text_type=TextType.BOLD)
        italicnode = TextNode(text="This is a italic text", text_type=TextType.ITALIC)
        codenode = TextNode(text="This is a code text", text_type=TextType.CODE)
        linknode = TextNode(
            text="This is a link", text_type=TextType.LINK, url="http://www.google.de"
        )
        imagenode = TextNode(
            text="This is an image", text_type=TextType.IMAGE, url="./image.jpg"
        )

        node1 = text_node_to_html_node(textnode)
        node2 = text_node_to_html_node(boldnode)
        node3 = text_node_to_html_node(italicnode)
        node4 = text_node_to_html_node(codenode)
        node5 = text_node_to_html_node(linknode)
        node6 = text_node_to_html_node(imagenode)

        print(node1)
        print(node2)
        print(node3)
        print(node4)
        print(node5)
        print(node6)

    def test_textnodeconvert(self):
        node = TextNode("This is text with a *italic block* word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold block** word", TextType.TEXT)
        node3 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        new_nodes3 = split_nodes_delimiter([node3], "`", TextType.CODE)

        print(new_nodes)
        print(new_nodes2)
        print(new_nodes3)

    def test_image_link_extraction(self):
        print("\n")
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        print(extract_markdown_images(text))
        print(extract_markdown_links(text2))

    def test_image_link_convert(self):
        print("\n")
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text without a link",
            TextType.TEXT,
        )
        node3 = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes2 = split_nodes_link([node2])
        new_nodes3 = split_nodes_image([node3])
        print(new_nodes)
        print(new_nodes2)
        print(new_nodes3)

    def test_text_to_textnodes(self):
        text = f"This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        print("\n")
        print(new_nodes)

    def test_markdown_to_blocks(self):
        markdown = "# This is a heading\n\n\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        blocks = markdown_to_blocks(markdown)
        print("\n")
        print(blocks)

    def test_block_to_blocktype(self):
        markdown = "# This is a heading\n\n\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        blocks = markdown_to_blocks(markdown)
        for block in blocks:
            print(block_to_block_type(block))

        test_blockstrings = [
            "# Heading 1",
            "This is a single-line paragraph.",
            "1. Ordered list item\n2. Second item\n3. Third item",
            "1. Ordered list item\n3. Invalid ordered item",
            "* Unordered list item\n* Second item\n* Third item",
        ]

        for test in test_blockstrings:
            print(block_to_block_type(test))

    def test_markdown_to_html_node(self):
        markdown = '# Heading 1\n\nThis is a paragraph with some **bold text** and *italic text*. Here is some `inline code`.\n\n> This is a blockquote.\n\n- This is an unordered list item 1\n- This is an unordered list item 2\n\n1. This is an ordered list item 1\n2. This is an ordered list item 2\n\n```\ndef example_code():\n    print("This is a code block")\n```'
        html = markdown_to_html_node(markdown)
        print("\n")
        print(html)


if __name__ == "__main__":
    unittest.main()
