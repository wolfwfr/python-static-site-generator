import unittest

from textnode import TextNode, TextType
from node_conversion import text_node_to_html_node


class TestNodeConversion(unittest.TestCase):
    # def test_node_conversion(self):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        txt = "This is a link node"
        url = "my-url"
        node = TextNode(txt, TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, txt)
        self.assertTrue("href" in html_node.props)
        self.assertEqual(html_node.props["href"], url)

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_image(self):
        txt = "This is a image node"
        url = "urlycurly"
        node = TextNode(txt, TextType.IMAGE, url=url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertTrue("src" in html_node.props)
        self.assertTrue("alt" in html_node.props)
        self.assertEqual(html_node.props["src"], url)
        self.assertEqual(html_node.props["alt"], txt)
