import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
