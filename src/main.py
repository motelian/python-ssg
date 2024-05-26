import shutil
import os
from copystatic import copy_recursive
from generate_page import generate_page


if __name__ == "__main__":

    # copy from static to public
    src_dir_path = "./static"
    dest_dir_path = "./public"
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    else:
        os.mkdir(dest_dir_path)
    
    copy_recursive(src_dir_path, dest_dir_path)
    generate_page("./content/index.md", "./template.html", "./public/index.html")




