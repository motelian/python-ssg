import os
from markdown_blocks import markdown_to_html_node

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

    file_name = os.path.basename(dest_path)
    if not (file_name.split(".")[-1] == "html"):
        file_name = "index.html"
    
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
