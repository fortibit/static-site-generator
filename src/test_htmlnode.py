import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # --- __init__ ---
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

    # --- props_to_html ---
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

    # --- to_html ---
    def test_to_html_raises_not_implemented(self):
        node = HTMLNode(tag="p", value="hi")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # --- __repr__ ---
    def test_repr_with_all_fields(self):
        child = HTMLNode(tag="span", value="child")
        node = HTMLNode(
            tag="div", value="parent", children=[child], props={"class": "container"}
        )
        expected = f"HTMLNode(div, parent, children: [{repr(child)}], {{'class': 'container'}})"
        self.assertEqual(repr(node), expected)

    def test_repr_with_defaults(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(None, None, children: None, None)")


class TestLeafNode(unittest.TestCase):
    # --- __init__ ---
    def test_initialization_with_values(self):
        node = LeafNode("p", "hello", {"id": "main"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"id": "main"})

    # --- to_html ---
    def test_to_html_with_tag_and_value(self):
        node = LeafNode("p", "hi")
        self.assertEqual(node.to_html(), "<p>hi</p>")

    def test_to_html_with_props(self):
        node = LeafNode("b", "bold text", {"class": "container"})
        self.assertEqual(node.to_html(), '<b class="container">bold text</b>')

    def test_to_html_without_tag_returns_value(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_to_html_raises_value_error_if_no_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_empty_string_value_raises_value_error(self):
        node = LeafNode("a", "")
        with self.assertRaises(ValueError):
            node.to_html()

    # --- __repr__ (inherited) ---
    def test_repr_includes_all_fields(self):
        node = LeafNode("i", "italic", {"style": "color:red"})
        repr_str = repr(node)
        self.assertIn("i", repr_str)
        self.assertIn("italic", repr_str)
        self.assertIn(
            "{'style': 'color:red'}".replace("'", '"').replace('"', "'"), repr_str
        )


class TestParentNode(unittest.TestCase):
    # --- __init__ ---
    def test_initialization_sets_values(self):
        child1 = HTMLNode(tag="span", value="child1")
        child2 = HTMLNode(tag="span", value="child2")
        node = ParentNode("p", [child1, child2], {"style": "color:blue"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children, [child1, child2])
        self.assertEqual(node.value, None)
        self.assertEqual(node.props, {"style": "color:blue"})

    # --- to_html ---
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1_node = LeafNode("b", "bold")
        child2_node = LeafNode(None, "plain")
        parent_node = ParentNode("div", [child1_node, child2_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>bold</b>plain</div>",
        )

    def test_to_html_with_props(self):
        child1_node = LeafNode("span", "hi")
        parent_node = ParentNode("div", [child1_node], {"class": "wrapper"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="wrapper"><span>hi</span></div>',
        )

    def test_to_html_raises_if_no_tag(self):
        node = ParentNode(None, [LeafNode("span", "hi")])
        with self.assertRaises(ValueError) as ctx:
            node.to_html()
        self.assertEqual(str(ctx.exception), "Parent node must have a tag")

    def test_to_html_raises_if_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError) as ctx:
            node.to_html()
        self.assertEqual(str(ctx.exception), "Parent node must have children nodes")

    # --- __repr__ ---
    def test_repr_includes_tag_and_children(self):
        child = LeafNode("span", "hi")
        node = ParentNode("div", [child], {"style": "color:brown"})
        repr_str = repr(node)
        self.assertIn("ParentNode(", repr_str)
        self.assertIn("div", repr_str)
        self.assertIn(f"children: [{repr(child)}]", repr_str)
        self.assertIn("{'style': 'color:brown'}", repr_str)


if __name__ == "__main__":
    unittest.main()
