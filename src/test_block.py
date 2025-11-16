import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks


class BlockTest(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """
# I'm a header

Table of contents:
  - item 1
  - item 2

and finally the rest
"""

        blocks = markdown_to_blocks(text)
        self.assertEqual(3, len(blocks))
        self.assertListEqual(
            [
                "# I'm a header",
                "Table of contents:\n  - item 1\n  - item 2",
                "and finally the rest",
            ],
            blocks,
        )

    def test_block_to_block_type_headings(self):
        headings = [
            "# heading1\n",
            "## heading2\n",
            "### heaading3\n",
            "#### heading4\n",
            "##### heading5\n",
            "###### heading6\n",
        ]

        for heading in headings:
            res = block_to_block_type(heading)
            self.assertEqual(res, BlockType.HEADING)

        false_headings = [
            "#",
            "##",
            "###",
            "####",
            "#####",
            "######",
            "####### heading7",
            "#nospace1",
            "##nospace2",
            "###nospace3",
            "####nospace4",
            "#####nospace5",
            "######nospace6",
        ]

        for heading in false_headings:
            res = block_to_block_type(heading)
            self.assertEqual(res, BlockType.PARAGRAPH)

    def test_block_to_block_type_code_blocks(self):
        code_block_1 = "```python\nmy_var = 1\n```"

        code_block_2 = "```\nundesignated-code\n```"
        code_blocks = [code_block_1, code_block_2]

        for block in code_blocks:
            res = block_to_block_type(block)
            self.assertEqual(res, BlockType.CODE)

        false_code_1 = "``\nmy-code\n``"
        false_code_2 = "```\nmy-code```"

        false_blocks = [false_code_1, false_code_2]

        for block in false_blocks:
            res = block_to_block_type(block)
            self.assertEqual(res, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_blocks(self):
        quote_1 = "> [!NOTE]\n> \n> please be aware."
        quote_2 = "> [!WARNING]\n> \n> please be aware."
        quote_3 = "> simple quote"

        quotes = [quote_1, quote_2, quote_3]

        for block in quotes:
            res = block_to_block_type(block)
            self.assertEqual(res, BlockType.QUOTE)

        false_quote_1 = "> blahblah\ncontinue without arrow"

        false_quotes = [false_quote_1]

        for block in false_quotes:
            res = block_to_block_type(block)
            self.assertEqual(res, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_blocks(self):
        list_1 = "- items and items \n-item2 \n-item3"

        lists = [list_1]

        for block in lists:
            res = block_to_block_type(block)
            self.assertEqual(res, BlockType.UNORDERED_LIST)

        false_list_1 = "- item 1\n* item 2 \n-item 3"
        false_list_2 = "- item 1\n - item 2 \n-item 3"

        false_lists = [false_list_1, false_list_2]

        for block in false_lists:
            res = block_to_block_type(block)
            self.assertEqual(res, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_blocks(self):
        list_1 = "1. items and items \n2. item2 \n3. item3"

        lists = [list_1]

        for block in lists:
            res = block_to_block_type(block)
            self.assertEqual(res, BlockType.ORDERED_LIST)

        false_list_1 = "1. item 1\n3. item 2 \n2. item 3"
        false_list_2 = "1. item 1\n3. item 2 \n4. item 3"
        false_list_3 = "2. item 1\n3. item 2 \n4. item 3"

        false_lists = [false_list_1, false_list_2, false_list_3]

        for block in false_lists:
            res = block_to_block_type(block)
            self.assertEqual(res, BlockType.PARAGRAPH)
