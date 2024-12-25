import unittest
from nodes.blocknode import BlockType
from nodes.textnode import TextNode, TextType
from markdown_parser import block_to_block_type, extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class MarkdownParserTest(unittest.TestCase):

    def test_markdown_to_blocks(self):
        text = "This is a paragraph\n\nThis is another paragraph"
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, ["This is a paragraph", "This is another paragraph"])

    def test_markdown_to_blocks_with_empty_lines(self):
        text = "This is a paragraph\n\n\n\nThis is another paragraph"
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, ["This is a paragraph", "This is another paragraph"])

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a list item\n- This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a list item\n2. This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> This is another quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        all_nodes = text_to_textnodes(text)
        self.assertEqual(all_nodes, [TextNode("This is ", TextType.NORMAL), TextNode("text", TextType.BOLD), TextNode(" with an ", TextType.NORMAL), TextNode("italic", TextType.ITALIC), TextNode(" word and a ", TextType.NORMAL), TextNode(
            "code block", TextType.CODE), TextNode(" and an ", TextType.NORMAL), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.NORMAL), TextNode("link", TextType.LINK, "https://boot.dev")])

    def test_split_nodes_delimiter(self):
        """Test normal case with multiple delimiters nested"""
        old_nodes = [
            TextNode("This *is **a** unicorn* paragraph", TextType.NORMAL)]
        delimiter = "*"
        text_type = TextType.ITALIC
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, [
            TextNode("This ", TextType.NORMAL),
            TextNode("is ", text_type),
            TextNode("", TextType.NORMAL),
            TextNode("a", text_type),
            TextNode("", TextType.NORMAL),
            TextNode(" unicorn", text_type),
            TextNode(" paragraph", TextType.NORMAL)
        ])

    def test_split_nodes_delimiter_throws_with_only_one_delimiter(self):
        """Test error case with single delimiter"""
        old_nodes = [TextNode("This *is a unicorn paragraph", TextType.NORMAL)]
        delimiter = "*"
        text_type = TextType.ITALIC
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_split_nodes_delimiter_first(self):
        """Test case with delimiter at start of string"""
        old_nodes = [TextNode("*This is* a unicorn paragraph", TextType.NORMAL)]
        delimiter = "*"
        text_type = TextType.ITALIC
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, [
            TextNode("This is", text_type),
            TextNode(" a unicorn paragraph", TextType.NORMAL)
        ])

    def test_split_nodes_delimiter_consecutive(self):
        """Test handling of consecutive delimiters"""
        old_nodes = [TextNode("**double** text", TextType.NORMAL)]
        delimiter = "*"
        text_type = TextType.ITALIC
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, [
            TextNode("", text_type),
            TextNode("double", TextType.NORMAL),
            TextNode("", text_type),
            TextNode(" text", TextType.NORMAL)
        ])

    def test_split_nodes_image(self):
        old_nodes = [TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif), haha", TextType.NORMAL)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.NORMAL), TextNode(
            "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(", haha", TextType.NORMAL)])

    def test_split_nodes_image_with_multiple_images(self):
        old_nodes = [TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.NORMAL), TextNode(
            "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", TextType.NORMAL), TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_split_nodes_image_first_does_not_add_empty_text(self):
        old_nodes = [
            TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and", TextType.NORMAL)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode(
            "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and", TextType.NORMAL)])

    def test_split_nodes_image_last_does_not_add_empty_text(self):
        old_nodes = [TextNode(
            "hello ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.NORMAL)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode("hello ", TextType.NORMAL), TextNode(
            "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")])

    def test_split_nodes_image_no_images(self):
        old_nodes = [
            TextNode("This is text with a link and a bold text", TextType.NORMAL)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode(
            "This is text with a link and a bold text", TextType.NORMAL)])

    def test_split_nodes_link(self):
        old_nodes = [TextNode(
            "This is text with a [link](https://www.example.com), haha", TextType.NORMAL)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.NORMAL), TextNode(
            "link", TextType.LINK, "https://www.example.com"), TextNode(", haha", TextType.NORMAL)])

    def test_split_nodes_link_with_multiple_links(self):
        old_nodes = [TextNode(
            "This is text with a [link](https://www.example.com) and [another link](https://www.example.com/2)", TextType.NORMAL)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.NORMAL), TextNode(
            "link", TextType.LINK, "https://www.example.com"), TextNode(" and ", TextType.NORMAL), TextNode("another link", TextType.LINK, "https://www.example.com/2")])

    def test_split_nodes_link_first_does_not_add_empty_text(self):
        old_nodes = [
            TextNode("[link](https://www.example.com) and", TextType.NORMAL)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, [TextNode(
            "link", TextType.LINK, "https://www.example.com"), TextNode(" and", TextType.NORMAL)])

    def test_split_nodes_link_last_does_not_add_empty_text(self):
        old_nodes = [
            TextNode("hello [link](https://www.example.com)", TextType.NORMAL)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, [TextNode("hello ", TextType.NORMAL), TextNode(
            "link", TextType.LINK, "https://www.example.com")])

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                         ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_images_without_any(self):
        text = "This is text with a link and a bold text"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

    def text_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another link](https://www.example.com/2)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("link", "https://www.example.com"),
                         ("another link", "https://www.example.com/2")])

    def text_extract_links_without_any(self):
        text = "This is text with a bold text and a image"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])
