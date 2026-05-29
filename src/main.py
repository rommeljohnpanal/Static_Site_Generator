import shutil
import os
from textnode import *
from htmlnode import LeafNode
from code import *

print("hello world")

def main():
   test = TextNode("This is some anchor text", TextType.LINK.value, "http://www.boot.dev")
   print(test)

   src = "./content"
   dest = "./public"

   prep_folders(src, dest)

   print("finished copying")

   # generate page from content/index. using template.html
   # generate_page("./content/index.md", "template.html", "./public/index.html")
   # generate_pages_recursive(src, "template.html", dest)
   




def prep_folders(src, dest):
   if not os.path.exists(dest):
      os.mkdir(dest)
   if not os.path.exists(src):
      raise FileNotFoundError(f"The folder does not exist: {src}")

   dest_list = os.listdir(dest)

   for content in dest_list:
      content_path = os.path.join(dest, content)
      if os.path.isfile(content_path):
         os.remove(content_path)
         print(f"removing file {content_path}")
      elif os.path.isdir(content_path):
         shutil.rmtree(content_path)
         print(f"removing folder {content_path}")
   
   # copy_from_to(src, dest)
   generate_pages_recursive(src, "template.html", dest)


def copy_from_to(src, dest):
   print(f"source: {src} || dest: {dest}")
   
   src_list = os.listdir(src)

   for item in src_list:
      item_path = os.path.join(src, item)
      if os.path.isfile(item_path):
         shutil.copy(item_path, os.path.join(dest, item))
         print(f"copy item {item_path}")
      elif os.path.isdir(item_path):
         new_folder = os.path.join(dest, item)
         os.mkdir(new_folder)
         print(f"recursing into {new_folder}")
         copy_from_to(item_path, new_folder)



if __name__ == "__main__":
   main()
