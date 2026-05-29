class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props 

    def to_html(self):
        raise NotImplemented
    
    def props_to_html(self):
        if self.props is None:
            return ''
        output = ''
        for k,v in self.props.items():
            output += ' '+k+'='+'"'+v+'"'
        
        return output 

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
        return NotImplemented

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value)
        self.props = props
    
    def to_html(self):
        if self is None:
            raise ValueError 
        if self.tag is None:
            return self.value 

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    
    
    def __repr__(self):
       return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children)
        self.tag = tag
        self.children=children
        self.props = props         

    def to_html(self):
        if self.tag is None:
            raise ValueError 
        if self.children is None: 
            raise ValueError("Children should not be empty")
        return f'<{self.tag}{self.props_to_html()}>{''.join(list(map(lambda x: x.to_html(), self.children)))}</{self.tag}>'
        