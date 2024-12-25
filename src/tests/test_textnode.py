import unittest

from nodes.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_eq_not_instance(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "This is a text node")

    def test_eq_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.example.com")
        self.assertEqual(node, node2)
    
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.example.com/2")
        self.assertNotEqual(node, node2)

    def test_to_html_node_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node.to_html_node().to_html(), "This is a text node")

    def test_to_html_node_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.to_html_node().to_html(), "<b>This is a text node</b>")
    
    def test_to_html_node_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.to_html_node().to_html(), "<i>This is a text node</i>")

    def test_to_html_node_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node.to_html_node().to_html(), "<code>This is a text node</code>")
    
    def test_to_html_node_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.example.com")
        self.assertEqual(node.to_html_node().to_html(), '<a href="https://www.example.com">This is a text node</a>')

    def test_to_html_node_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.example.com")
        self.assertEqual(node.to_html_node().to_html(), '<img src="https://www.example.com" alt="This is a text node"></img>')


if __name__ == "__main__":
    unittest.main()