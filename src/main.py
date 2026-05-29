import shutil
import os
import sys
from textnode import *
from htmlnode import LeafNode
from code import *

stat = "./static"
src = "./content"
dest = "./public"
temp = "./template.html"

def main():
   
   basepath = ""

   if len(sys.argv) > 1:
      basepath = sys.argv[1]
   elif len(sys.argv) == 1:
      basepath = "/"
   else:
      raise ValueError("Too many arguments")



   prep_folders(stat, dest)

   print("finished copying")

   # generate page from content/index. using template.html
   # generate_page("./content/index.md", "template.html", "./public/index.html")
   generate_pages_recursive(src, temp, dest)
   




def prep_folders(source_dir_path: str, dest_dir_path: str) -> None:
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            prep_folders(from_path, dest_path)


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
