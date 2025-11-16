import os
import sys
import shutil

from extract_title import extract_title
from to_html import markdown_to_html_node


def main():
    args = sys.argv
    basepath = len(args) > 1 and args[1] or "/"

    # assuming function is called from project root
    src = "static"
    dst = "docs"

    if not os.path.exists(dst):
        raise Exception(f"destination directory at {os.path.abspath(dst)} not found")

    if not os.path.exists(src):
        raise Exception(f"source directory at {os.path.abspath(src)} not found")

    shutil.rmtree(dst)
    os.mkdir(dst)
    recursive_copy(src, dst)

    generate_pages_recursive(basepath, "content", "template.html", dst)


def recursive_copy(src, dst):
    contents = os.listdir(src)
    sub_content = lambda a, b: a + "/" + b
    for content in contents:
        sub_src = sub_content(src, content)
        sub_dst = sub_content(dst, content)
        if os.path.isdir(sub_src):
            os.mkdir(sub_dst)
            recursive_copy(sub_src, sub_dst)
            continue
        shutil.copy(sub_src, sub_dst)


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_content = ""
    template_content = ""
    with open(from_path, "r") as f:
        from_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(from_content)
    html = html_node.to_html()
    title = extract_title(from_content)
    text = template_content.replace("{{ Title }}", title)
    text = text.replace("{{ Content }}", html)
    text = text.replace('href="/', f'href="{basepath}')
    text = text.replace('src="/', f'src="{basepath}')

    dirs, _ = os.path.split(dest_path)
    if len(dirs) > 0:
        os.makedirs(dirs, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(text)


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    sub_content = lambda a, b: a + "/" + b

    contents = os.listdir(dir_path_content)
    for content in contents:
        this_content_path = sub_content(dir_path_content, content)
        if os.path.isdir(this_content_path):
            generate_pages_recursive(
                basepath,
                this_content_path,
                template_path,
                sub_content(dest_dir_path, content),
            )
            continue
        generate_page(
            basepath,
            sub_content(dir_path_content, content),
            template_path,
            sub_content(dest_dir_path, content.replace(".md", ".html")),
        )


main()
