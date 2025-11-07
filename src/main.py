from pathlib import Path
import os
import shutil
from textnode import TextType
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode
from delimiter import split_nodes_delimiter, split_nodes_image, text_to_textnodes
from block_markdown import (
    block_to_block_type,
    markdown_to_blocks,
)
from markdown import markdown_to_html_node, extract_title


def main():
    generate_public()
    generate_pages_recursive("./content/", "./template.html", "./public/")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_path = Path(dir_path_content)
    template = Path(template_path)
    dest_path = Path(dest_dir_path)
    walk(content_path, content_path, dest_path, template)


def walk(current_dir, content_root, dest_root, template):
    for entry in current_dir.iterdir():
        if entry.is_dir():
            walk(entry, content_root, dest_root, template)
        elif entry.is_file() and entry.suffix == ".md":
            relative = entry.relative_to(content_root)
            out_relative = (relative.with_name(
                "index.html") if relative.name == "index.md" else relative.with_suffix(".html"))
            out_path = dest_root / out_relative
            out_path.parent.mkdir(parents=True, exist_ok=True)
            generate_page(str(entry), str(template), str(out_path))


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}...")
    with open(from_path) as f:
        md = f.read()
    f.close()
    with open(template_path) as f:
        temp = f.read()
    f.close()
    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)
    temp = temp.replace("{{ Title }}", title)
    temp = temp.replace("{{ Content }}", html)
    with open(dest_path, "w") as f:
        f.write(temp)
    f.close()


def generate_public():
    print("Clearing public directory...")
    clear_dir("./public/")
    print("Copying static files to public directory...")
    copy_dir("./static/", "./public/")


def copy_dir(src, dst):
    for item in os.listdir(src):
        item_path = os.path.join(src, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dst)
        elif os.path.isdir(item_path):
            dir_path = os.path.join(dst, item)
            os.mkdir(dir_path)
            copy_dir(item_path, dir_path)


def clear_dir(path):
    if not os.path.exists(path):
        raise Exception("not valid path")
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


main()
