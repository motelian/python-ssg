import shutil
import os
from copystatic import copy_recursive
from generate_content import generate_pages_recursive


if __name__ == "__main__":

    # copy from static to public
    src_dir_path = "./static"
    dest_dir_path = "./public"
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    else:
        os.mkdir(dest_dir_path)
    
    copy_recursive(src_dir_path, dest_dir_path)
    generate_pages_recursive("./content", "./template.html", "./public")




