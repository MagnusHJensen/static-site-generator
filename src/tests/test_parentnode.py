

import unittest

from nodes.leafnode import LeafNode
from nodes.parentnode import ParentNode
from nodes.textnode import TextNode, TextType


class ParentNodeTest(unittest.TestCase):

    def test_to_html_raises_error_if_tag_is_empty(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("", []).to_html()
        
        self.assertEqual("Tag is empty", str(context.exception))

    def test_to_html_raises_error_if_children_is_empty(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", []).to_html()
        
        self.assertEqual("Children is empty", str(context.exception))
    
    def test_to_html_returns_html(self):
        node = ParentNode("div", [LeafNode(value="Test")])
        self.assertEqual("<div>Test</div>", node.to_html())

    def test_to_html_with_attributes(self):
        node = ParentNode("div", [LeafNode(value="Test")], {"class": "test"})
        self.assertEqual('<div class="test">Test</div>', node.to_html())

    def test_to_html_multiple_children(self):
        node = ParentNode("div", [LeafNode(value="Test"), ParentNode(tag="p", children=[LeafNode("TextNode")])])
        self.assertEqual("<div>Test<p>TextNode</p></div>", node.to_html())
