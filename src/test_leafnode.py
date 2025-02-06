import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_multiple(self):
        print(LeafNode(tag=None, value="This is a test."))
        print(LeafNode(tag=None, value="This is a test.").to_html())
        with self.assertRaises(ValueError):
            print(LeafNode(tag="p", value=None).to_html())
        print(
            LeafNode(
                tag="b",
                value="This is also a test.",
                props={"href": "https://www.google.com"},
            )
        )
        print(
            LeafNode(
                tag="b",
                value="This is also a test.",
                props={"href": "https://www.google.com"},
            ).to_html()
        )


if __name__ == "__main__":
    unittest.main()
