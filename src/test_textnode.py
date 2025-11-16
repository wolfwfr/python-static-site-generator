import unittest

from textnode import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


def getEqualNodes():
    text = "This is a text node"
    node = TextNode(text, TextType.BOLD)
    node2 = TextNode(text, TextType.BOLD)
    return node, node2


class TestTextNode(unittest.TestCase):
    def test_eq_text(self):
        node1, node2 = getEqualNodes()
        self.assertEqual(node1, node2)

        node1.text = "this is a different text node"
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        url_text = "url-text"
        node1, node2 = getEqualNodes()
        node1.url = url_text

        self.assertNotEqual(node1, node2)

        node2.url = url_text

        self.assertEqual(node1, node2)

        node1.url = None
        node2.url = None

        self.assertEqual(node1, node2)

    def test_eq_text_type(self):
        text_type_1 = TextType.BOLD
        text_type_2 = TextType.ITALIC

        node1, node2 = getEqualNodes()

        node1.text_type = text_type_1
        node2.text_type = text_type_1

        self.assertEqual(node1, node2)

        node1.text_type = text_type_2

        self.assertNotEqual(node1, node2)

    # TODO: finish test
    def test_split_nodes(self):
        text_node_simple = TextNode("text", TextType.TEXT)

        res = split_nodes_delimiter([text_node_simple], "**", TextType.BOLD)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].text, "text")

        text_node_bold_insert = TextNode(
            "this is some **bold text** as an insert", TextType.TEXT
        )

        res = split_nodes_delimiter([text_node_bold_insert], "**", TextType.BOLD)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].text, "this is some ")
        self.assertEqual(res[1].text, "bold text")
        self.assertEqual(res[2].text, " as an insert")
        self.assertEqual(res[0].text_type, TextType.TEXT)
        self.assertEqual(res[1].text_type, TextType.BOLD)
        self.assertEqual(res[2].text_type, TextType.TEXT)

        text_node_bold_border = TextNode("this is some **bold text**", TextType.TEXT)
        res = split_nodes_delimiter([text_node_bold_border], "**", TextType.BOLD)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].text, "this is some ")
        self.assertEqual(res[1].text, "bold text")
        self.assertEqual(res[0].text_type, TextType.TEXT)
        self.assertEqual(res[1].text_type, TextType.BOLD)

        text_node_bold_prefix = TextNode("**this** is some bold text", TextType.TEXT)
        res = split_nodes_delimiter([text_node_bold_prefix], "**", TextType.BOLD)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].text, "this")
        self.assertEqual(res[1].text, " is some bold text")
        self.assertEqual(res[0].text_type, TextType.BOLD)
        self.assertEqual(res[1].text_type, TextType.TEXT)

        image_node = TextNode("image subtext", TextType.IMAGE, "image-url")
        res = split_nodes_delimiter([image_node], "[]", TextType.IMAGE)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], image_node)

        link_node = TextNode("link node", TextType.LINK, "link-url")
        res = split_nodes_delimiter([link_node], "[]", TextType.LINK)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], link_node)

        code_node = TextNode("code node", TextType.CODE, "")
        res = split_nodes_delimiter([code_node], "`", TextType.CODE)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], code_node)

        text_node_with_code = TextNode("text node `with code`", TextType.TEXT, "")
        res = split_nodes_delimiter([text_node_with_code], "`", TextType.CODE)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].text, "text node ")
        self.assertEqual(res[1].text, "with code")
        self.assertEqual(res[0].text_type, TextType.TEXT)
        self.assertEqual(res[1].text_type, TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images(
            "This is text with two ![image](https://i.imgur.com/zjjcJKZ.png) ![image2](https://imgur.com/gallery/golang-f45xU7y)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://imgur.com/gallery/golang-f45xU7y"),
            ],
            matches,
        )

        matches = extract_markdown_images(
            "This is text with identical ![image](https://i.imgur.com/zjjcJKZ.png) ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links(
            "This is text with two [link](https://i.imgur.com/zjjcJKZ.png) [link2](https://imgur.com/gallery/golang-f45xU7y)"
        )
        self.assertListEqual(
            [
                ("link", "https://i.imgur.com/zjjcJKZ.png"),
                ("link2", "https://imgur.com/gallery/golang-f45xU7y"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a duplicate ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a duplicate ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and a duplicate [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a duplicate ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        res = text_to_textnodes(input)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            res,
        )


if __name__ == "__main__":
    unittest.main()
