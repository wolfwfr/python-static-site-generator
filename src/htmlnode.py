class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join([f'{k}="{self.props[k]}"' for k in self.props])


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return f"{self.value}"

        props_string = self.props_to_html()
        if len(props_string) > 0:
            props_string = " " + props_string

        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("'tag' field cannot be None")
        if self.children is None:
            raise ValueError("'children' field cannot be None")

        props_string = self.props_to_html()
        if len(props_string) > 0:
            props_string = " " + props_string

        child_strings = [v.to_html() for v in self.children]
        child_string = "".join(child_strings)

        # TODO: replace above line with the following:
        # child_string = "\n".join(child_strings)
        # if len(child_string) > 0:
        #     child_string = "\n" + child_string + "\n"

        return f"<{self.tag}{props_string}>{child_string}</{self.tag}>"
