import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

delim_type_backtick = "`"
delim_type_bold = "**"
delim_type_italic = "*"


def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, text_type_text)], delim_type_bold, text_type_bold)
    nodes = split_nodes_delimiter(nodes, delim_type_italic, text_type_italic)
    nodes = split_nodes_delimiter(nodes, delim_type_backtick, text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if (
        (delimiter == delim_type_backtick and text_type != text_type_code)
        or (delimiter == delim_type_bold and text_type != text_type_bold)
        or (delimiter == delim_type_italic and text_type != text_type_italic)
    ):
        raise Exception(f"Invalid delimiter({delimiter}) type for {text_type}")
    
    new_nodes = []
    for oldnode in old_nodes:
        if oldnode.text_type != text_type_text:
            new_nodes.append(oldnode)
            continue
        sections = oldnode.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("Invalid markdown, formatted section not enclosed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i%2 == 0:
                new_nodes.append(TextNode(sections[i], text_type_text))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):

    new_nodes = []
    for oldnode in old_nodes:
        original_text = oldnode.text
        
        if oldnode.text_type != text_type_text:
            new_nodes.append(oldnode)
            continue

        img_list = extract_markdown_images(original_text)
        
        # non-empty textnodes with no images
        if len(img_list) == 0 and oldnode.text.split():
            new_nodes.append(oldnode)
            continue

        split_nodes = []
        for i, img_tup in enumerate(img_list):
            sections = original_text.split(f"![{img_tup[0]}]({img_tup[1]})",1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], text_type=text_type_text))
            if img_tup[0].split() and img_tup[1].split():
                new_nodes.append(TextNode(img_tup[0], text_type=text_type_image, url=img_tup[1]))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, text_type=text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):

    new_nodes = []
    for oldnode in old_nodes:
        original_text = oldnode.text
        
        if oldnode.text_type != text_type_text:
            new_nodes.append(oldnode)
            continue

        link_list = extract_markdown_links(original_text)
        
        # non-empty textnodes with no images
        if len(link_list) == 0 and oldnode.text.split():
            new_nodes.append(oldnode)
            continue

        split_nodes = []
        for i, link_tup in enumerate(link_list):
            sections = original_text.split(f"[{link_tup[0]}]({link_tup[1]})",1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], text_type=text_type_text))
            if link_tup[0].split() and link_tup[1].split():
                new_nodes.append(TextNode(link_tup[0], text_type=text_type_link, url=link_tup[1]))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, text_type=text_type_text))

    return new_nodes

def extract_markdown_images(text:str):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text:str):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)