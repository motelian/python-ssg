import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_eq_false(self):
        node = TextNode("This is a text nde", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)
    
    def test_eq_false2(self):
        node = TextNode("This is a text node", "bold", "www.example.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_false3(self):
        node = TextNode("This is a text node", "bold", "www.example.com")
        node2 = TextNode("This is a text node", "italic", "www.example.com")
        self.assertNotEqual(node, node2)

    def test_eq_false3(self):
        node = TextNode("This is a text node", "bold", "www.example.com")
        node2 = TextNode("This is a text node", "italci", "www.example.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "www.example.com")
        self.assertEqual(
            "TextNode(This is a text node, bold, www.example.com)", repr(node)
        )
    
    def test_text_node_to_html_node(self):
        node = TextNode("Girl in a jacket", "image", "img_girl.jpg")
        self.assertEqual(
            '<img src="img_girl.jpg" alt="Girl in a jacket"></img>',
            text_node_to_html_node(node).to_html()
        )


if __name__ == "__main__":
    unittest.main()
