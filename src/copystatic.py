import os
import shutil


def copy_dir_tree(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for filename in os.listdir(src):
        from_path = os.path.join(src, filename)
        dest_path = os.path.join(dst, filename)
        print(f" * {from_path} -> {dest_path}")

        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_dir_tree(from_path, dest_path)
