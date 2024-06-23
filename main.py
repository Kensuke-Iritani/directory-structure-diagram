import glob
import os

NUM_INDENTS = 1
BRANCH = " " * NUM_INDENTS + "├── "
LEAF = " " * NUM_INDENTS + "└── "
LINE = " " * NUM_INDENTS + "│   "
SPACE = " " * NUM_INDENTS + "    "


def make_line(lst):
    result = ""
    for item in lst:
        if item == 0:
            result += SPACE
        elif item == 1:
            result += LINE
    return result


def make_branch(item, depth, shape=BRANCH):
    return make_line(depth) + shape + item + "\n"


def explore_directory(directory, depth=[], ignore_files=[]):
    result = ""
    items = os.listdir(directory)
    items.sort()

    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        if path in ignore_files:  # is igunored?
            continue

        if os.path.isdir(path):
            if index == len(items) - 1:
                result += make_branch(item, depth, shape=LEAF)
                add_depth = 0
            else:
                result += make_branch(item, depth)
                add_depth = 1
            result += explore_directory(
                path, depth + [add_depth], ignore_files=ignore_files
            )
        else:
            if index == len(items) - 1:
                result += make_branch(item, depth, shape=LEAF)
                depth = depth[:-1] + [0]
            else:
                result += make_branch(item, depth)
    return result


def read_gitignore():
    gitignore_path = ".gitignore"
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    # Replace '/' with os.sep to handle cross-platform compatibility
                    patterns.append(line.replace("/", os.sep))
    return patterns


def output_directory_structure(directory, ignore_files=[]):
    for key in read_gitignore():
        ignore_files += glob.glob(key)
    ignore_files = [os.path.abspath(path) for path in ignore_files]  # フルパス化
    structure = explore_directory(directory, ignore_files=ignore_files)
    with open("directory_structure.txt", "w", encoding="utf-8") as file:
        file.write(directory + "\n")
        file.write(structure)


directory = os.getcwd()
ignore_files = [os.path.basename(__file__), ".git"]
output_directory_structure(directory, ignore_files=ignore_files)
