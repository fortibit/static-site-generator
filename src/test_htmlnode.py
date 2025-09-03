import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    # __init__
    def test_default_initialization(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_initialization_with_values(self):
        node = HTMLNode(tag="p", value="hello", children=[], props={"id": "main"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"id": "main"})

    def test_children_as_list(self):
        child1 = HTMLNode(tag="span", value="child1")
        child2 = HTMLNode(tag="span", value="child2")
        node = HTMLNode(tag="div", children=[child1, child2])
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].value, "child1")
        self.assertEqual(node.children[1].value, "child2")

    # props_to_html
    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="hi")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(tag="p", value="hi", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_attribute(self):
        node = HTMLNode(tag="a", value="link", props={"href": "example.com"})
        self.assertEqual(node.props_to_html(), ' href="example.com"')

    def test_props_to_html_multiple_attributes(self):
        node = HTMLNode(tag="div", props={"class": "btn", "id": "main"})
        result = node.props_to_html()
        # attributes should appear in insertion order
        self.assertEqual(result, ' class="btn" id="main"')

    # to_html
    def test_to_html_raises_not_implemented(self):
        node = HTMLNode(tag="p", value="hi")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # __repr__
    def test_repr_with_all_fields(self):
        child = HTMLNode(tag="span", value="child")
        node = HTMLNode(tag="div", value="parent", children=[child], props={"class": "container"})
        expected = f"HTMLNode(div, parent, children: [{repr(child)}], {{'class': 'container'}})"
        self.assertEqual(repr(node), expected)

    def test_repr_with_defaults(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(None, None, children: None, None)")

if __name__ == "__main__":
    unittest.main()