from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
   TEXT = None
   # PLAIN = "plain"
   BOLD = "b"
   ITALIC = "i"
   CODE = "code"
   LINK = "a"
   IMAGE = "img"

class BlockType(Enum):
   PARAGRAPH = "paragraph"
   HEADING = "heading"
   CODE = "code"
   QUOTE = "quote"
   OLIST = "ordered_list"
   ULIST = "unordered_list"

class TextNode():
   def __init__(self, text, text_type, url=None):
      self.text  = text
      self.text_type = text_type
      self.url = url

   def __eq__(self, other):
      if isinstance(other, TextNode):
         return self.text == other.text and self.text_type == other.text_type and self.url == other.url
      return NotImplemented

   def __repr__(self):
      return f"TextNode({self.text}, {self.text_type}, {self.url})"
