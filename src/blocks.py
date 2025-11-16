from enum import Enum

from textnode import TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text):
    return [block.strip() for block in text.split("\n\n") if block != ""]


def block_to_block_type(block):
    # heading block
    if block.startswith("#"):
        has_hash_prefix = True
        ends_with_space = False
        for idx in range(0, min(7, len(block))):
            if block[idx] == " ":
                ends_with_space = True
                break
            if block[idx] != "#":
                has_hash_prefix = False
                break
        if has_hash_prefix and ends_with_space:
            return BlockType.HEADING

    # code block
    if block.startswith("```") and block.endswith("\n```"):
        return BlockType.CODE

    # quote block
    is_quote = True
    while is_quote:
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        break

    if is_quote:
        return BlockType.QUOTE

    # unordered-list block
    is_unordered_list = True
    while is_unordered_list:
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("-"):
                is_unordered_list = False
                break
        break

    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    # ordered-list block
    is_ordered_list = True
    i = 1
    while is_ordered_list:
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(f"{i}. "):
                is_ordered_list = False
                break
            i += 1
        break

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    # paragraph block
    return BlockType.PARAGRAPH
