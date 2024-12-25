from nodes.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, attributes: dict = None):
        super().__init__(tag, None, children, attributes)


    def to_html(self):
        if self.tag is "":
            raise ValueError("Tag is empty")
        
        if len(self.children) == 0:
            raise ValueError("Children is empty")
        
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        
        html += f"</{self.tag}>"
        return html