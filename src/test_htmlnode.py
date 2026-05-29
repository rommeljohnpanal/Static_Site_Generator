import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_propseq(self):
        node = HTMLNode(props = {"href":"https://www.google.com", "target":"_blank"})
        node2 = HTMLNode(props = {"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(node, node2)

    def test_href(self):
        node = HTMLNode(props = {"href":"https://www.boot.dev", "target":"_blank"})
        node2 = HTMLNode(props = {"href":"https://www.google.com", "target":"_blank"})
        self.assertNotEqual(node, node2)

    def test_target(self):
        node = HTMLNode(props = {"href":"https://www.google.com", "target":"_blank"})
        node2 = HTMLNode(props = {"href":"https://www.google.com", "target":"home"})
        self.assertNotEqual(node, node2)

    def test_propstohtml(self):
        node = HTMLNode(props = {"href":"https://www.google.com", "target":"_blank"})        
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    
    def test_leaf_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
