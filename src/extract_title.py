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
