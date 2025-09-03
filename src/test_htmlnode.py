import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "Link", None, {"href": "www.example.com", "target": "_blank"})
        node2 = HTMLNode("a", "Link", None, {"href": "www.example.com", "target": "_blank"})
        self.assertNotEqual(node, node2)

    # TODO: more tests


if __name__ == "__main__":
    unittest.main()