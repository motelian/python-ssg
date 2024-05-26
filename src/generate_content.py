import os
import shutil
from markdown_blocks import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for file in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(from_path):
            if not file.split(".")[-1] == "md":
                continue
            html_content = generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)




def generate_page(from_path, template_path, dest_path):
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        md = f.read()

    with open(template_path, "r") as f:
        template = f.read()
    
    html_content = markdown_to_html_node(md)
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content.to_html())

    full_file_name = os.path.basename(dest_path)
    file_name_parts = full_file_name.split(".")
    suffix = file_name_parts[-1]
    name = "".join(file_name_parts[:-1])
    if not (suffix == "html"):
        file_name = name + ".html"
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    file_path = os.path.join(dest_dir_path, file_name)
    with open(file_path, "w") as f:
        f.write(template)

def extract_title(markdown:str):
    lines = markdown.split("\n")
    h1_text = ""
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            h1_text = line.split("#")[-1].strip()
            break
    if h1_text:
        return h1_text
    raise Exception("Markdown has no h1 header")
