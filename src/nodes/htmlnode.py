

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, attributes: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.attributes = attributes
        pass

    def to_html(self):
        children_html = ""
        if (self.children is not None):
            for child in self.children:
                children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{self.value if self.value != None else ""}{children_html}</{self.tag}>"
    
    def props_to_html(self):
        if self.attributes is None:
            return ""
        
        props = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])

        return f" {props}" if len(props) > 0 else ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.attributes})"