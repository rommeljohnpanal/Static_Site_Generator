import re
from textnode import *
from htmlnode import *


def text_node_to_html_node(text_node):
   if text_node.text_type == TextType.IMAGE:
      return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
   return LeafNode(text_node.text_type.value, text_node.text, text_node.url)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):        
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)    
    
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def block_to_html_node(block, block_type):
    # CODE, ULIST and OLIST will have children nodes, but how do I pull the children in? 
    if block_type.value == "code":
        block_cleaned = block[3:-3].strip().lstrip("\n")
        text_node = TextNode(block_cleaned, TextType.CODE)
        return ParentNode("pre", [text_node_to_html_node(text_node)])
    if block_type.value == "unordered_list":
        block_list = block.split("\n")
        children = []
        for item in block_list:
            block_cleaned = item[2:]
            children.append(ParentNode(tag="li", children=text_to_children(block_cleaned)))
        return ParentNode(tag="ul", children=children)
    if block_type.value == "ordered_list":
        block_list = block.split("\n")
        children = []
        for item in block_list:
            block_cleaned = item.split(" ", 1)[1]
            children.append(ParentNode(tag="li", children=text_to_children(block_cleaned)))
        return ParentNode(tag="ol", children=children)
    raise ValueError(f"invalid block type: {block_type}")



    # paragraph, heading, quote 
    if block_type.value == "paragraph":
        block_cleaned = block.replace("\n", " ")
        return ParentNode(tag="p", children=text_to_children(block_cleaned))
    if block_type.value == "heading":
        level = block.split()[0].count("#")
        return ParentNode(tag=f"h{level}", children=text_to_children(block))
    if block_type.value == "quote":
        block_cleaned = block.replace("> ", "", 1).strip()
        return ParentNode(tag="blockquote", children=text_to_children(block_cleaned))


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:         
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        children.append(block_node)
    
    return ParentNode("div", children)



def extract_title(markdown):
   if markdown.startswith("# "):
      raise Exception("Exception: no h1 header")
   return markdown[2:].strip()