import os
from pathlib import Path
from block_markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f" * Generating page from {from_path} -> {dest_path} using {template_path}")

    from_f = open(from_path, mode="r")
    md = from_f.read()
    from_f.close()

    templ_f = open(template_path, mode="r")
    template = templ_f.read()
    templ_f.close()

    md_as_html_node = markdown_to_html_node(md)
    html = md_as_html_node.to_html()

    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    dest_f = open(dest_path, mode="w")
    dest_f.write(template)
    dest_f.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        to_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path) and filename[-2:] == "md":
            new_file = Path(filename.replace("md", "html"))
            to_path = os.path.join(dest_dir_path, new_file)
            generate_page(from_path, template_path, to_path)
        else:
            generate_pages_recursive(from_path, template_path, to_path)

