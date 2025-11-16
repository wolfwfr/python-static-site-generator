import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_node_props_to_html(self):
        field_1, field_2 = "field_1", "field_2"
        value_1, value_2 = "value_1", "value_2"

        nd = HTMLNode(props={field_1: value_1, field_2: value_2})

        res = nd.props_to_html()
        self.assertEqual(res, f'{field_1}="{value_1}" {field_2}="{value_2}"')

    def test_node_inputs(self):
        nd = HTMLNode()
        self.assertIsNone(nd.tag)
        self.assertIsNone(nd.value)
        self.assertIsNone(nd.children)
        self.assertIsNone(nd.props)

        child = HTMLNode()
        nd = HTMLNode("tag", "value", [child], {"field_1": "value_1"})
        self.assertEqual(nd.tag, "tag")
        self.assertEqual(nd.value, "value")
        self.assertEqual(nd.children, [child])
        self.assertEqual(nd.props, {"field_1": "value_1"})

        nd = HTMLNode(
            tag="tag", value="value", children=[child], props={"field_1": "value_1"}
        )
        self.assertEqual(nd.tag, "tag")
        self.assertEqual(nd.value, "value")
        self.assertEqual(nd.children, [child])
        self.assertEqual(nd.props, {"field_1": "value_1"})

    def test_node_leaf(self):
        nd = LeafNode(tag="p", value="val val")
        self.assertIsNotNone(nd.tag)
        self.assertIsNotNone(nd.value)
        self.assertIsNone(nd.children)
        self.assertIsNone(nd.props)

        res = nd.to_html()
        self.assertEqual(res, "<p>val val</p>")

        nd.props = {"field_1": "value_1"}

        res = nd.to_html()
        self.assertEqual(res, '<p field_1="value_1">val val</p>')

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
