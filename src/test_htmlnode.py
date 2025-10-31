import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "Hello world!",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "Hello world!",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "i",
            "abcd",
            None,
            {"href": "https://gmail.com"}
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(i, abcd, children: None, {'href': 'https://gmail.com'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as assert_error:
            node.to_html()
        self.assertEqual(assert_error.exception.args[0], "node has no value")

    def test_children(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )


if __name__ == "__main__":
    unittest.main()
