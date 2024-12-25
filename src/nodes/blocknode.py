
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"
    QUOTE = "quote"
    CODE = "code"

class BlockNode:
    def __init__(self, content: str, block_type: BlockType):
        self.content = content
        self.block_type = block_type
        pass