import os

def print_directory_tree(start_path='.', indent=''):
    items = os.listdir(start_path)
    for i, item in enumerate(items):
        path = os.path.join(start_path, item)
        is_last = i == len(items) - 1
        prefix = '└── ' if is_last else '├── '
        print(indent + prefix + item)
        if os.path.isdir(path):
            new_indent = indent + ('    ' if is_last else '│   ')
            print_directory_tree(path, new_indent)

if __name__ == '__main__':
    print("Directory structure of:", os.getcwd())
    print_directory_tree()
