class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              # string representing a tag, eg. p, a, h1
        self.value = value          # string representing a value of the tag eg. text inside paragraph
        self.children = children    # list of HTMLNode objects representing children of this node
        self.props = props          # dictionary - representing attributes of the tag eg {"href": "www.example.com"}

    def to_html(self):
        # child classes will override this to render themselves as HTML
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        attributes = ""
        if self.props is not None:
            for attr, val in self.props.items():
                attributes += f' {attr}="{val}"'
        return attributes
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("No value in leaf node")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children nodes")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
