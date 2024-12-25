
import os
import shutil
from markdown_converter import markdown_to_html
from nodes.textnode import TextNode, TextType


def main():
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")




def copy_files(from_dir, to_dir):
    from_dir = os.path.join(os.curdir, from_dir)
    to_dir = os.path.join(os.curdir, to_dir)
    print(f"Copying files from {from_dir} to {to_dir}")
    if not os.path.exists(from_dir):
        return
    
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    else:
        shutil.rmtree(to_dir)

    shutil.copytree(from_dir, to_dir)
    
def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    if len(lines) == 0:
        return ""
    
    first_line = lines[0]
    if first_line.startswith("# "):
        return first_line[2:]
    
    raise ValueError("First line must be an h1 heading")

def generate_pages_recursive(from_dir: str, template_path: str, dest_dir: str):
    from_dir = os.path.join(os.curdir, from_dir)
    template_path = os.path.join(os.curdir, template_path)
    dest_dir = os.path.join(os.curdir, dest_dir)
    print(f"Generating pages from {from_dir} using template {template_path} to {dest_dir}")

    if not os.path.exists(from_dir):
        return
    
    for root, dirs, files in os.walk(from_dir):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, os.path.relpath(from_path, start=from_dir)).replace(".md", ".html")
                generate_page(from_path, template_path, dest_path)

def generate_page(from_path: str, template_path: str, dest_path: str):
    from_path = os.path.join(os.curdir, from_path)
    template_path = os.path.join(os.curdir, template_path)
    dest_path = os.path.join(os.curdir, dest_path)
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")

    markdown = ""
    with open(from_path, "r") as f:
        markdown = f.read()

    template = ""
    with open(template_path, "r") as f:
        template = f.read()

    html_content = markdown_to_html(markdown).to_html()
    title = extract_title(markdown)
    html = template.replace("{{title}}", title).replace("{{content}}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html)


if __name__ == "__main__":  
    main()