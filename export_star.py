#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime

now = datetime.now()
now_str = f"{now.year}_{now.month}_{now.day}"
OUTPUT_HTML = f"edge_favorites_{now_str}.html"
OUTPUT_FILE = f"edge_favorites_{now_str}.json"
BOOKMARKS_PATH = os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Bookmarks"
)

def load_bookmarks(path):

    if not os.path.exists(path):
        print("Bookmarks file not found.")
        return None

    print(f"Find the target:{path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("Read data sucessfully")
        return data
    except Exception as e:
        print(f"Failed to read bookmarks: {e}")
        return None

def parse_node(node):
    node_type = node.get("type")
    new_node = {
        "type": node_type,
        "name": node.get("name", ""),
    }

    # 保留 id 等
    for key in ["id",  "meta_info"]:
        if key in node:
            new_node[key] = node[key]

    if node_type == "folder":
        children = node.get("children", [])
        new_node["children"] = [parse_node(child) for child in children]

    # URL
    elif node_type == "url":
        new_node["url"] = node.get("url", "")

    return new_node

def export_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Export complete -> {filename}")
    except Exception as e:
        print(f"[ERROR] Export failed: {e}")
def generate_html_node(node):
    """递归生成HTML内容"""
    node_type = node.get("type")
    name = node.get("name", "Unnamed")

    if node_type == "folder":
        children = node.get("children", [])
        if not children:
            return f"<li>{name}</li>\n"
        inner_html = "".join([generate_html_node(child) for child in children])
        return f"<li>{name}<ul>\n{inner_html}</ul></li>\n"
    elif node_type == "url":
        url = node.get("url", "#")
        return f'<li><a href="{url}" target="_blank">{name}</a></li>\n'
    else:
        return ""  # 其他类型忽略

def export_html(bookmarks, filename):
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Edge Bookmarks</title>
</head>
<body>
<h1>Edge Bookmarks</h1>
<ul>
"""
    # 遍历根节点
    for root_name, root_node in bookmarks.items():
        if root_name=="synced" or root_name=="workspaces_v2":
            continue
        html_content += f"<li>{root_name}<ul>\n"
        html_content += generate_html_node(root_node)
        html_content += "</ul></li>\n"

    html_content += "</ul>\n</body>\n</html>"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[INFO] HTML export complete -> {filename}")

def generate_md_node(node, level=0):
    md_content = ""
    indent = "    " * level  # 每级缩进 4 空格

    node_type = node.get("type")
    name = node.get("name", "")

    if node_type == "folder":
        md_content += f"{indent}* **{name}**\n"
        for child in node.get("children", []):
            md_content += generate_md_node(child, level + 1)
    elif node_type == "url":
        url = node.get("url", "")
        md_content += f"{indent}* [{name}]({url})\n"

    return md_content


def export_md(bookmarks, filename):
    md_content = f"# Edge Bookmarks\n\n> 常用的 Edge 浏览器收藏夹 | 更新时间: {now_str}\n\n---\n"

    for root_name, root_node in bookmarks.items():
        # 跳过不需要的根节点
        if root_name in ("synced", "workspaces_v2"):
            continue

        md_content += f"* **{root_name}**\n"
        md_content += generate_md_node(root_node, level=1)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[INFO] Markdown export complete -> {filename}")
def main():
    print("[INFO] Edge Bookmark Export Tool")
    print("--------------------------------")

    data = load_bookmarks(BOOKMARKS_PATH)
    if not data:
        return

    roots = data.get("roots", {})
    new_roots = {}

    for root_name in ["bookmark_bar", "other", "synced"]:
        if root_name in roots:
            new_roots[root_name] = parse_node(roots[root_name])

    new_data = {
        "checksum": data.get("checksum", ""),
        "roots": new_roots,
        "version": 1
    }

    export_json(new_data, OUTPUT_FILE)
    export_html(roots, OUTPUT_HTML)
    export_md(new_roots, "README.md")

if __name__ == "__main__":
    main()