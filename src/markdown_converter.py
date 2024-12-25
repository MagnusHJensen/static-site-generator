
from markdown_parser import block_to_block_type, markdown_to_blocks, text_to_textnodes
from nodes.blocknode import BlockType
from nodes.htmlnode import HTMLNode
from nodes.leafnode import LeafNode


def markdown_to_html(markdown: str) -> HTMLNode:
    children = []
    
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockType.HEADING:
                children.append(handle_heading_block(block))
            case BlockType.PARAGRAPH:
                children.append(handle_paragraph_block(block))
            case BlockType.ORDERED_LIST:
                children.append(handle_list_block(block, "ol"))
            case BlockType.UNORDERED_LIST:
                children.append(handle_list_block(block, "ul"))
            case BlockType.QUOTE:
                children.append(handle_quote_block(block))
            case BlockType.CODE:
                children.append(handle_code_block(block))


    return HTMLNode("div", None, children, None)

def handle_heading_block(block: str) -> HTMLNode:
    level = block.count("#")
    nodes = text_to_textnodes(" ".join(block.split(" ")[1:]))
    nodes = [node.to_html_node() for node in nodes]
    return HTMLNode(f"h{min(level, 6)}", None, nodes, None)

def handle_paragraph_block(block: str) -> HTMLNode:
    text_nodes = text_to_textnodes(block)
    text_nodes = [node.to_html_node() for node in text_nodes]
    return HTMLNode("p", None, text_nodes, None)

def handle_list_block(block: str, tag: str) -> HTMLNode:
    lines = block.split("\n")
    children = []
    for line in lines:
        nodes = text_to_textnodes(" ".join(line.split(" ")[1:]))
        nodes = [node.to_html_node() for node in nodes]
        children.append(HTMLNode("li", None, nodes, None))
    
    return HTMLNode(tag, None, children, None)

def handle_quote_block(block: str) -> HTMLNode:
    lines = block.split("\n")
    children = []
    for line in lines:
        children.append(LeafNode(line[2:]))
    
    return HTMLNode("blockquote", None, children, None)

def handle_code_block(block: str) -> HTMLNode:
    lines = block.split("\n")
    children = []
    for line in lines[1:-1]:
        children.append(HTMLNode("code", None, [LeafNode(line + "\n")], None))
    
    return HTMLNode("pre", None, children, None)