from re import template
from block_markdown import extract_title, markdown_to_html_node
from textnode import TextNode
import os
import shutil
import sys

SOURCE_DIR = "static"
DESTINATION_DIR = "docs"
basepath = '/docs'

def main():
    # Clean Destination
    if os.path.exists(DESTINATION_DIR):
        shutil.rmtree(DESTINATION_DIR)
    copy_directory(SOURCE_DIR, DESTINATION_DIR)
    print(sys.argv)
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", DESTINATION_DIR)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_string = ""
    with open(from_path) as file:
        markdown_string = file.read()

    if not markdown_string or markdown_string == -1:
        raise Exception(f"Failed to read: {from_path}")

    html_string = ""
    with open(template_path) as file:
        html_string = file.read()

    if not html_string or html_string == -1:
        raise Exception(f"Failed to read: {template_path}")

    markdown_to_html_string = markdown_to_html_node(markdown_string).to_html()
    title = extract_title(markdown_string)
    if not title:
        title = "No Title"
    html_string = html_string.replace("{{ Title }}", title).replace('href="/', f'href="{basepath}')
    html_string = html_string.replace("{{ Content }}", markdown_to_html_string).replace('src="/', f'src="{basepath}')

    directory_dest = os.path.dirname(dest_path)
    if not os.path.exists(directory_dest):
        os.makedirs(directory_dest)

    with open(dest_path, "w") as file:
        file.write(html_string)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_files = os.listdir(dir_path_content)
    for file in content_files:
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        print(file_path, dest_path)
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, dest_path.replace(".md",".html"))
        elif os.path.isdir(file_path):
            generate_pages_recursive(file_path, template_path, dest_path)

def copy_directory(src_dir, dest_dir):
    if os.path.exists(src_dir):
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        files = os.listdir(src_dir)
        for file in files:
            file_path = os.path.join(src_dir, file)
            dest_path = os.path.join(dest_dir, file)
            if os.path.isfile(file_path):
                shutil.copy(file_path, dest_path)
            elif os.path.isdir(file_path):
                copy_directory(file_path, dest_path)
    else:
        raise Exception("Invalid source provided")


main()
