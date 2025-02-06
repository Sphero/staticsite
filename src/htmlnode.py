class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # string
        self.value = value  # string
        self.children = children  # list
        self.props = props  # dict

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        result = ""
        for key, value in self.props.items():
            result += " " + key + " " + value
        return result

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("value required")
        if self.tag == None:
            return self.value
        result = f"<{self.tag}"
        if self.props == None:
            result += ">"
        else:
            for item in self.props:
                result += f" {item}={self.props[item]}"
            result += ">"
        result += f"{self.value}</{self.tag}>"
        return result


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("ParentNode needs a tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("ParentNode needs children")
        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result
