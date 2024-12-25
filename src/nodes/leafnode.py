from nodes.htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str | None = None, attributes: dict = None):
        super().__init__(tag, value, None, attributes)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return self.value
        
        return super().to_html()