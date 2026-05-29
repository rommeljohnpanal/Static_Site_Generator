import shutil
import os
from textnode import *
from htmlnode import LeafNode

print("hello world")

def main():
   test = TextNode("This is some anchor text", TextType.LINK.value, "http://www.boot.dev")
   print(test)
   
   copy_from_to("./static", "./public")
   print("finished copying")


def copy_from_to(src, dest):
   if not os.path.exists(dest):
      raise FileNotFoundError(f"The folder does not exist: {dest}")
   if not os.path.exists(src):
      raise FileNotFoundError(f"The folder does not exist: {src}")
   
   print(f"source: {src} || dest: {dest}")

   dest_list = os.listdir(dest):

   for content in dest_list:
      if os.path.isfile(content):
         os.remove(content)
      elif os.path.isdir(content):
         shutil.rmtree(content)
   
   src_list = os.listdir(src)

   for item in src_list:      
      if os.path.isfile(item):
         shutil.copy(item, dest)
      elif os.path.isdir(item):
         new_folder = os.mkdir(os.path.join(dest, item))
         copy_from_to(item, new_folder)
      



if __name__ == "__main__":
   main()
