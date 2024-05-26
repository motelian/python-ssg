import os
import shutil
def copy_recursive(src_dir_path, dest_dir_path):

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    for file in os.listdir(src_dir_path):
        from_path = os.path.join(src_dir_path,file)
        dest_path = os.path.join(dest_dir_path,file)
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_recursive(from_path, dest_path)