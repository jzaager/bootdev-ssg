import os
import shutil

from copystatic import copy_dir_tree
from generate_page import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content/index.md"
dir_path_template = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying files to public directory...")
    copy_dir_tree(dir_path_static, dir_path_public)

    generate_page(dir_path_content, dir_path_template, dir_path_public)


if __name__ == "__main__":
    main()
