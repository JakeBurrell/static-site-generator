class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method has not been implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        elif isinstance(self.props, dict):
            props_list = []
            for key, value in self.props.items():
                props_list.append(f' {key}="{value}"')

            return "".join(props_list)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, Children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a value")
        if self.children is None:
            raise ValueError("All parent nodes must have a child")
        childrens_html = [html.to_html() for html in self.children]
        return f"<{self.tag}>{"".join(childrens_html)}</{self.tag}>"
