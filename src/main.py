from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from utility import *


def main():
    copy_directory_contents("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")


main()
