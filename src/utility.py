import os
import re
import shutil

from htmlnode import *
from textnode import *


class MarkdownBlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception("Unknown text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for item in old_nodes:
        node: TextNode = item
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        nodetext: str = node.text
        if nodetext.count(delimiter) % 2 != 0:
            raise Exception(f"Closing {delimiter} delimiter missing")
        nodetextsplit: list = nodetext.split(delimiter)
        for i in range(len(nodetextsplit)):
            if len(nodetextsplit[i]) == 0:
                continue
            if i == 0 or i == len(nodetextsplit) - 1:
                new_nodes.append(TextNode(nodetextsplit[i], TextType.TEXT, None))
            else:
                new_nodes.append(TextNode(nodetextsplit[i], text_type, None))
    return new_nodes


def extract_markdown_images(text):
    result = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return result
    """
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    """


def extract_markdown_links(text):
    result = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return result
    """
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    #"""


def split_nodes_image(old_nodes):
    new_nodes = []
    for item in old_nodes:
        node: TextNode = item
        nodetext: str = node.text
        markdown_link_tuples = extract_markdown_images(nodetext)
        if node.text_type != TextType.TEXT or len(markdown_link_tuples) == 0:
            new_nodes.append(node)
            continue
        for markdown_tuple in markdown_link_tuples:
            image_alt, image_link = markdown_tuple
            nodetextsplit: list = nodetext.split(f"![{image_alt}]({image_link})", 1)
            if len(nodetextsplit[0]) > 0:
                new_nodes.append(TextNode(nodetextsplit[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if len(nodetextsplit[1]) > 0:
                new_nodes.append(TextNode(nodetextsplit[1], TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for item in old_nodes:
        node: TextNode = item
        nodetext: str = node.text
        markdown_link_tuples = extract_markdown_links(nodetext)
        if node.text_type != TextType.TEXT or len(markdown_link_tuples) == 0:
            new_nodes.append(node)
            continue
        for markdown_tuple in markdown_link_tuples:
            anchor_text, url = markdown_tuple
            nodetextsplit: list = nodetext.split(f"[{anchor_text}]({url})", 1)
            if len(nodetextsplit[0]) > 0:
                new_nodes.append(TextNode(nodetextsplit[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            if len(nodetextsplit[1]) > 0:
                new_nodes.append(TextNode(nodetextsplit[1], TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text=text, text_type=TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(filter(lambda x: x.strip() != "", map(lambda x: x.strip(), blocks)))
    return blocks


def block_to_block_type(block):
    if not block:
        return MarkdownBlockType.PARAGRAPH

    lines = block.split("\n")
    expected_number = 1
    is_ordered_list = True

    for line in lines:
        if not line:
            return MarkdownBlockType.PARAGRAPH

        if re.match(r"^#{1,6} ", line):
            return MarkdownBlockType.HEADING

        if re.match(r"^```", line):
            return MarkdownBlockType.CODE

        if re.match(r"^> ", line):
            return MarkdownBlockType.QUOTE

        if re.match(r"^- ", line) or re.match(r"^\* ", line):
            return MarkdownBlockType.UNORDERED_LIST

        match = re.match(r"^(\d+)\. ", line)
        if match:
            number = int(match.group(1))
            if number != expected_number:
                is_ordered_list = False
            expected_number += 1
        else:
            is_ordered_list = False

    return (
        MarkdownBlockType.ORDERED_LIST
        if is_ordered_list and expected_number > 2
        else MarkdownBlockType.PARAGRAPH
    )


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes


def markdown_to_html_node(markdown):
    parent_node = ParentNode(tag="div", children=[])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == MarkdownBlockType.HEADING:
            heading_level = len(re.match(r"^(#{1,6}) ", block).group(1))
            block_node = ParentNode(
                tag=f"h{heading_level}",
                children=text_to_children(block[heading_level + 1 :]),
            )
        elif block_type == MarkdownBlockType.CODE:
            code_content = "\n".join(block.split("\n")[1:-1])
            block_node = ParentNode(
                tag="pre", children=[LeafNode(tag="code", value=code_content)]
            )
        elif block_type == MarkdownBlockType.QUOTE:
            quote_content = "\n".join(line[2:] for line in block.split("\n"))
            block_node = ParentNode(
                tag="blockquote", children=text_to_children(quote_content)
            )
        elif block_type == MarkdownBlockType.UNORDERED_LIST:
            list_items = block.split("\n")
            list_nodes = [
                ParentNode(tag="li", children=text_to_children(item[2:]))
                for item in list_items
            ]
            block_node = ParentNode(tag="ul", children=list_nodes)
        elif block_type == MarkdownBlockType.ORDERED_LIST:
            list_items = block.split("\n")
            list_nodes = [
                ParentNode(
                    tag="li",
                    children=text_to_children(re.match(r"^\d+\. (.*)", item).group(1)),
                )
                for item in list_items
            ]
            block_node = ParentNode(tag="ol", children=list_nodes)
        else:
            block_node = ParentNode(tag="p", children=text_to_children(block))

        parent_node.children.append(block_node)

    return parent_node


def copy_directory_contents(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_directory_contents(s, d)
        else:
            shutil.copy2(s, d)
            print(f"Copied file: {s} to {d}")


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if re.match(r"^# ", line):
            return line[2:]
        else:
            raise Exception("No title found in markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    html_output = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    with open(dest_path, "w") as file:
        file.write(html_output)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, dir_path_content)
                dest_dir = os.path.join(dest_dir_path, relative_path)
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, file.replace(".md", ".html"))
                generate_page(from_path, template_path, dest_path)
