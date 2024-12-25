
import unittest
from nodes.leafnode import LeafNode

class LeafNodeTest(unittest.TestCase):

    def test_to_html(self):
        leaf_node = LeafNode("This is a paragraph", "p", {"class": "paragraph"})
        self.assertEqual(leaf_node.to_html(), '<p class="paragraph">This is a paragraph</p>')

    def test_to_html_no_tag(self):
        leaf_node = LeafNode("This is a paragraph", None, {"class": "paragraph"})
        self.assertEqual(leaf_node.to_html(), 'This is a paragraph')

    def test_to_html_no_value(self):
        leaf_node = LeafNode(None, "p", {"class": "paragraph"})
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_to_html_no_attributes(self):
        leaf_node = LeafNode("This is a paragraph", "p")
        self.assertEqual(leaf_node.to_html(), '<p>This is a paragraph</p>')