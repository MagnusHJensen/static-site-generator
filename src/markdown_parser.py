from nodes.blocknode import BlockType
from nodes.textnode import TextNode, TextType
import re


def markdown_to_blocks(markdown: str) -> list:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]

def block_to_block_type(block: str) -> BlockType:
    if (block.startswith("#")):
        return BlockType.HEADING
    
    lines = block.splitlines()
    if all([line.startswith("- ") or line.startswith("* ") for line in lines]):
        return BlockType.UNORDERED_LIST
    
    if all([re.match(r"\d+\. ", line) for line in lines]):
        return BlockType.ORDERED_LIST
    
    if all([line.startswith("> ") for line in lines]):
        return BlockType.QUOTE
    
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    return BlockType.PARAGRAPH

def text_to_textnodes(text: str) -> list:
    all_nodes = [TextNode(text, TextType.NORMAL)]

    all_nodes = split_nodes_delimiter(all_nodes, "**", TextType.BOLD)
    all_nodes = split_nodes_delimiter(all_nodes, "*", TextType.ITALIC)
    all_nodes = split_nodes_delimiter(all_nodes, "`", TextType.CODE)
    all_nodes = split_nodes_image(all_nodes)
    all_nodes = split_nodes_link(all_nodes)

    return all_nodes


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
            
        parts = node.text.split(delimiter)

        if (len(parts) == 1):
            # No delimiter found, just add the node
            new_nodes.append(node)
            continue
        
        # Check if we have at least one delimiter set
        if len(parts) < 3:
            raise ValueError("Delimiter not found in text")
            
        # For each part, alternate between normal and text_type
        for i in range(len(parts)):
            # Skip empty parts at the start if they're followed by more parts
            if i == 0 and parts[i] == "" and len(parts) > 1:
                continue
                
            # Add the part with appropriate text type
            text = parts[i]
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.NORMAL))
            else:
                new_nodes.append(TextNode(text, text_type))
    
    return new_nodes

def split_nodes_image(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
                continue

            value = node.text
            for alt, url in images:
                parts = value.split(f"![{alt}]({url})", 1)
                if len(parts[0]) > 0:
                    new_nodes.append(TextNode(parts[0], TextType.NORMAL))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                value = ''.join(parts[1:])
            
            if (len(value) > 0):
                new_nodes.append(TextNode(value, TextType.NORMAL))

    return new_nodes

def split_nodes_link(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
                continue

            value = node.text
            for text, url in links:
                parts = value.split(f"[{text}]({url})", 1)
                if len(parts[0]) > 0:
                    new_nodes.append(TextNode(parts[0], TextType.NORMAL))
                new_nodes.append(TextNode(text, TextType.LINK, url))
                value = ''.join(parts[1:])
            
            if (len(value) > 0):
                new_nodes.append(TextNode(value, TextType.NORMAL))

    return new_nodes


def extract_markdown_images(text: str):
    matches = re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)
    return matches

def extract_markdown_links(text: str):
    matches = re.findall(r"\[([^\]]*)\]\(([^)]*)\)", text)
    return matches