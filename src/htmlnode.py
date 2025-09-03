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