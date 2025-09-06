import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextType(unittest.TestCase):
    def test_enum_members_exist(self):
        self.assertEqual(TextType.TEXT.value, "text")
        self.assertEqual(TextType.BOLD.value, "bold")
        self.assertEqual(TextType.ITALIC.value, "italic")
        self.assertEqual(TextType.CODE.value, "code")
        self.assertEqual(TextType.LINK.value, "link")
        self.assertEqual(TextType.IMAGE.value, "image")

    def test_enum_values_are_unique(self):
        values = [t.value for t in TextType]
        self.assertEqual(len(values), len(set(values)))


class TestTextNode(unittest.TestCase):
    def test_basic_initialization(self):
        node = TextNode("hello", TextType.TEXT)
        self.assertEqual(node.text, "hello")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_initialization_with_url(self):
        node = TextNode("example", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "example")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")
    
    def test_url_defaults_to_none(self):
        node = TextNode("test", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("hi", TextType.TEXT)
        node2 = TextNode("hi", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("hi", TextType.LINK, "a")
        node2 = TextNode("hi", TextType.LINK, "b")
        self.assertNotEqual(node, node2)

    def test_comparison_with_non_textnode(self):
        node = TextNode("hi", TextType.TEXT)
        self.assertFalse(node == "hi")

    def test_repr(self):
        node = TextNode("hi", TextType.LINK, "https://example.com")
        self.assertEqual(
            "TextNode(hi, link, https://example.com)", repr(node)
        )

    def test_repr_no_url(self):
        node = TextNode("hi", TextType.BOLD)
        self.assertEqual(
            "TextNode(hi, bold, None)", repr(node)
        )


# --- text_node_to_html_node ---
def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()