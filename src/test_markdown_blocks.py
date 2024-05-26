import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    code_to_html_node,
    olist_to_html_node,
    quote_to_html_node,
    ulist_to_html_node,
    heading_to_html_node,
    markdown_to_html_node,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_ulist,
    block_type_olist,

)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
            ]
        )

    def test_markdown_to_blocks_new_lines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
            ]
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "1. list\n2. items\n4. items"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_block_to_html_node(self):
        code_block = """```
# test python code block 
def sum(a,b): 
    return a+b```"""
        self.assertEqual(
            """<pre><code>
# test python code block 
def sum(a,b): 
    return a+b</code></pre>""",
            code_to_html_node(code_block).to_html()
        )
        olist_block = """1. first item
2. second item
3. third item"""
        self.assertEqual(
            """<ol><li>first item</li><li>second item</li><li>third item</li></ol>""",
            olist_to_html_node(olist_block).to_html()
        )

        quote_block = """>     Words can be like X-rays, if you use them properly—they will go through anything. You read and you are pierced.
> —Aldous Huxley, *Brave New World*"""
        self.assertEqual(
            """<blockquote>Words can be like X-rays, if you use them properly—they will go through anything. You read and you are pierced. —Aldous Huxley, <i>Brave New World</i></blockquote>""",
            quote_to_html_node(quote_block).to_html()
        )

        ulist_block = """- This is a list
- with items
- and *more* and `more` items"""
        self.assertEqual(
            """<ul><li>This is a list</li><li>with items</li><li>and <i>more</i> and <code>more</code> items</li></ul>""",
            ulist_to_html_node(ulist_block).to_html()
        )

        header_block = """### Level three header"""
        self.assertEqual(
            """<h3>Level three header</h3>""",
            heading_to_html_node(header_block).to_html()
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
if __name__ == "__main__":   
    unittest.main()