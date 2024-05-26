import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

block_type_pattern = {
    block_type_heading: r"^#{1,6}\s+\w+",
    block_type_quote: r"^>.*",
    block_type_ulist: r"^[*-]\s+.*",
    block_type_olist: r"^\d+\.\s+.*"
}

def markdown_to_html_node(markdown:str):
    block_texts = markdown_to_blocks(markdown)
    html_items = []
    for b in block_texts:
        html_items.append(block_to_html_node(b))
    return ParentNode("div", html_items)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")   

def markdown_to_blocks(markdown:str):
    blocks = map(lambda x: x.strip(), markdown.split("\n\n"))
    filtered = filter(lambda x:x, blocks)
    return list(filtered)

def paragraph_to_html_node(block):
    items = block.split("\n")
    lines = map(lambda x: x.strip(), [pattern_match(x) for x in items])
    paragraph = " ".join(lines)
    children_nodes = text_to_html_node(paragraph)
    return ParentNode("p", children_nodes)

def code_to_html_node(block):
    children_nodes = text_to_html_node(block)
    return ParentNode("pre", children_nodes)

def quote_to_html_node(block):
    pattern = r"^>.(.*)"
    items = block.split("\n")
    lines = map(lambda x: x.strip(), [pattern_match(x, pattern) for x in items])
    text = " ".join(lines)
    return ParentNode("blockquote", text_to_html_node(text))

def olist_to_html_node(block):
    pattern = r"^\d+\.(.*)"
    items = block.split("\n")
    lines = map(lambda x: x.strip(), [pattern_match(x, pattern) for x in items])
    children_nodes = []
    for line in lines:
        children_nodes.append(ParentNode("li", text_to_html_node(line)))
    return ParentNode("ol", children_nodes)

def ulist_to_html_node(block):
    pattern = r"^[*-](.*)"
    items = block.split("\n")
    lines = map(lambda x: x.strip(), [pattern_match(x, pattern) for x in items])
    children_nodes = []
    for line in lines:
        children_nodes.append(ParentNode("li", text_to_html_node(line)))
    return ParentNode("ul", children_nodes)

def heading_to_html_node(block):
    pattern = r"^#{1,6}(.*)"
    def header_level(line):
        ranks = {''.join(i*["#"]): f"h{i}" for i in range(1,7)}
        hashtags = re.match(r"^(#{1,6})", line).group(1)
        if hashtags in ranks:
            return ranks[hashtags]
        raise ValueError(f"Invalid heading level: {hashtags}") 
    line = pattern_match(block,pattern).strip()
    return ParentNode(header_level(block), text_to_html_node(line))

def text_to_html_node(text):
    textnodes = text_to_textnodes(text)
    children = list(map(lambda x: text_node_to_html_node(x), textnodes))
    return children

def block_to_block_type(block:str):
    def is_match(pattern):
        def inner_func(line):
            return re.match(pattern, line) is not None
        return inner_func
    
    def valid_ordered_list(lines:list[str]):
        # ordered list has to start with 1 and incremented by 1
        for i, line in enumerate(lines):
            num = re.findall(r"^\d+", line)[0]
            if num:
                if int(num) == i+1:
                    continue
            return False
        return True

    # conditions only applies to blocks
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    
    if is_match(block_type_pattern[block_type_heading])(block):
        return block_type_heading

    # check for the rest of block types: should satisfy conditions for all lines
    lines = block.split("\n")
    for bt in (block_type_quote, block_type_ulist, block_type_olist):
        passed = list(map(is_match(block_type_pattern[bt]), lines))
        if all(passed):
            if bt == block_type_olist and not valid_ordered_list(lines):
                continue
            return bt
    return block_type_paragraph

def pattern_match(string, pattern=None):
    if pattern is None:
        return string
    return re.match(pattern, string).group(1)

