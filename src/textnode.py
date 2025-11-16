from enum import Enum
import re


class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return (
            self.text == node.text
            and self.text_type == node.text_type
            and self.url == node.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return [
        item
        for node in old_nodes
        for item in split_node_delimiter(node, delimiter, text_type)
    ]


def split_node_delimiter(old_node, delimiter, text_type):
    if old_node.text_type != TextType.TEXT:
        return [old_node]

    if len(old_node.text) < len(delimiter):
        return [old_node]

    special_start = old_node.text.startswith(delimiter)
    special_end = old_node.text.endswith(delimiter)

    typ = TextType.TEXT
    if special_start:
        typ = text_type

    elements = [elem for elem in old_node.text.split(delimiter) if elem != ""]

    expectedEvennes = 1  # 1 is uneven
    if special_start ^ special_end:  # xor
        expectedEvennes = 0
    if len(elements) % 2 != expectedEvennes:
        raise Exception("invalid markdown syntax")

    switch_type = lambda x: TextType.TEXT if x == text_type else text_type

    res = []
    for elem in elements:
        res.append(TextNode(elem, typ))
        typ = switch_type(typ)
    return res


def extract_markdown_images(text):
    regex = r"\!\[(.*?)\]\((.*?)\)"
    return extract_with_double_catch_regex(text, regex)


def extract_markdown_links(text):
    regex = r"\[(.*?)\]\((.*?)\)"
    return extract_with_double_catch_regex(text, regex)


def extract_with_double_catch_regex(text, regex):
    matches = re.findall(regex, text)
    res = []
    for match in matches:
        res.append((match[0], match[1]))
    return res


def split_nodes_image(old_nodes):
    return [item for node in old_nodes for item in split_node_image(node)]


def split_node_image(old_node):
    def delim_func(x):
        return f"![{x[0]}]({x[1]})"

    return split_node_on_delim(
        old_node, extract_markdown_images, delim_func, TextType.IMAGE
    )


def split_nodes_link(old_nodes):
    return [item for node in old_nodes for item in split_node_link(node)]


def split_node_link(old_node):
    def delim_func(x):
        return f"[{x[0]}]({x[1]})"

    return split_node_on_delim(
        old_node, extract_markdown_links, delim_func, TextType.LINK
    )


# TODO: there must be a cleaner way
def split_node_on_delim(old_node, extract_func, delim_func, text_type):
    res = []
    if old_node.text_type != TextType.TEXT:
        return [old_node]

    matches = extract_func(old_node.text)
    if len(matches) == 0:
        return [old_node]

    text = old_node.text

    delim = delim_func(matches[0])
    starts_with_match = text[: len(delim)] == delim
    first_iteration = True

    for match in matches:
        delim = delim_func(match)
        split = text.split(delim, 1)

        img_node = TextNode(match[0], text_type, match[1])
        if not first_iteration or not starts_with_match:
            res.append(TextNode(split[0], TextType.TEXT))
        res.append(img_node)

        first_iteration = False
        text = split[1]

    if len(text) > 0:
        res.append(TextNode(text, TextType.TEXT))

    return res


def text_to_textnodes(text):
    original = TextNode(text, TextType.TEXT, "")

    def split_bold(nodes):
        return split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def split_italic(nodes):
        return split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    def split_code(nodes):
        return split_nodes_delimiter(nodes, "`", TextType.CODE)

    # NOTE: order matters!
    functions = [
        split_nodes_image,
        split_nodes_link,
        split_code,
        split_italic,
        split_bold,
    ]

    nodes = [original]
    for func in functions:
        nodes = func(nodes)

    return nodes
