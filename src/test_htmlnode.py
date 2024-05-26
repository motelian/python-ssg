import unittest
from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,       
)

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag = "div",
            value = "Hello, World!",
            children=None,
            props = {"class": "greetings", "href": "www.example.com"}
        )
        self.assertEqual(
            ' class="greetings" href="www.example.com"', node.props_to_html()
        )

    def test_to_html_no_children(self):
        node = LeafNode(
            tag = "p",
            value = "This is a paragraph of text.",
        )
        self.assertEqual(
            '<p>This is a paragraph of text.</p>', node.to_html()
        )

    def test_to_html_no_tag(self):
        node = LeafNode(
            tag=None,
            value = "This is a paragraph of text.",
        )
        self.assertEqual(
            'This is a paragraph of text.', node.to_html()
        )

    def test_to_html1(self):
        node = LeafNode(
            tag = "a",
            value = "Click me!",
            props = {"href": "https://www.google.com"},
        )
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
        )

    def test_repr(self):
        node = LeafNode(
            tag = "a",
            value = "Click me!",
            props = {"href": "https://www.google.com"},
        )
        self.assertEqual(
            "LeafNode(a, Click me!, {'href': 'https://www.google.com'})", repr(node)
        )
    
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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()