import unittest

from nodes.htmlnode import HTMLNode


class HTMLNodeTest(unittest.TestCase):

    def props_to_html(self):
        html_node = HTMLNode("p", "This is a paragraph", None, {"class": "paragraph"})
        self.assertEqual(html_node.props_to_html(), 'class="paragraph"')
    
    def multiple_props_to_html(self):
        html_node = HTMLNode("p", "This is a paragraph", None, {"class": "paragraph", "id": "paragraph1"})
        self.assertEqual(html_node.props_to_html(), 'class="paragraph" id="paragraph1"')