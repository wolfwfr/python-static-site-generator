from blocks import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import ParentNode
from node_conversion import text_node_to_html_node
from textnode import TextNode, TextType, text_to_textnodes


def markdown_to_html_node(markdown):
    children = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.CODE:
                children.append(code_block_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_block_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(
                    list_block_to_html_node(block, BlockType.UNORDERED_LIST)
                )
            case BlockType.ORDERED_LIST:
                children.append(list_block_to_html_node(block, BlockType.ORDERED_LIST))
            case BlockType.PARAGRAPH:
                children.append(paragraph_block_to_html_node(block))

    root = ParentNode("div", children)
    return root


# code_block_to_html_node() takes a code-block text and returns two levels of
# nodes, one parent with a 'pre' tag, and a leaf with the 'code' tag). It does
# not parse lines into individual TextNodes and instead turns the whole block,
# with first and last lines removed, into a single TextNode.
def code_block_to_html_node(block):
    tag = "pre"

    split = block.split("\n")
    text = "\n".join(split[1 : len(split) - 1])
    text.replace(
        "  ", " "
    )  # replace any double-spaces that were introduced, expecting no issues from replacing actual double-spaces

    text += "\n"

    child_text_node = TextNode(text, TextType.CODE)
    child_html_node = text_node_to_html_node(child_text_node)
    parent = ParentNode(tag, [child_html_node])

    return parent


# list_block_to_html_node() takes a block and the specific type of list the
# block represents. It returns a parent-node with the appropriate tag ('ul' or
# 'ol'). The parent-node will contain one child (with 'li' tag) for each item in
# the list.
def list_block_to_html_node(block, list_type):
    tag = "ul"
    pref = lambda num: "- "
    if list_type == BlockType.ORDERED_LIST:
        tag = "ol"
        pref = lambda num: f"{num}. "
    children = []
    i = 1
    for line in block.split("\n"):
        line = line.removeprefix(pref(i))
        text_nodes = text_to_textnodes(line)
        children.append(
            ParentNode(
                "li", [text_node_to_html_node(text_node) for text_node in text_nodes]
            )
        )
        i += 1
    return ParentNode(tag, children)
    pass


def paragraph_block_to_html_node(block):
    tag = "p"
    text = " ".join([line for line in block.split("\n")])
    text.replace(
        "  ", " "
    )  # replace any double-spaces that were introduced, expecting no issues from replacing actual double-spaces
    text_nodes = text_to_textnodes(text)
    return ParentNode(
        tag, [text_node_to_html_node(text_node) for text_node in text_nodes]
    )


def quote_block_to_html_node(block):
    tag = "blockquote"
    prefix = "> "
    text = " ".join([line[len(prefix) :] for line in block.split("\n")])
    text.replace(
        "  ", " "
    )  # replace any double-spaces that were introduced, expecting no issues from replacing actual double-spaces
    text_nodes = text_to_textnodes(text)
    return ParentNode(
        tag, [text_node_to_html_node(text_node) for text_node in text_nodes]
    )


def heading_to_html_node(block):
    i, old, new = 0, block, block.removeprefix("#")
    while len(old) != len(new):
        i += 1
        old = new
        new = old.removeprefix("#")
    text = new.removeprefix(" ")

    tag = f"h{i}"
    text_nodes = text_to_textnodes(text)
    return ParentNode(
        tag, [text_node_to_html_node(text_node) for text_node in text_nodes]
    )


# example HTML with the various tags
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimal HTML Example</title>
</head>
<body>
    <h1>header here</h1>
    <p>This is a paragraph.</p>
    <pre><code>console.log("This is a code block");</code></pre>
    <blockquote>
        This is a quote.
    </blockquote>
    <ul>
        <li>Unordered list item 1</li>
        <li>Unordered list item 2</li>
    </ul>
    <ol>
        <li>Ordered list item 1</li>
        <li>Ordered list item 2</li>
    </ol>
</body>
</html>
"""
