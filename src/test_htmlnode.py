import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_multiple(self):
        node = HTMLNode(
            ...,
            ...,
            ...,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        node2 = HTMLNode(
            ...,
            ...,
            ...,
            {"href": "https://www.brave.com"},
        )
        print(node.props_to_html())
        print(node2.props_to_html())
        print(node)


if __name__ == "__main__":
    unittest.main()
