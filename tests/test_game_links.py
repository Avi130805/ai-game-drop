import os
import re

INDEX_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'index.html')

def main():
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    # regex to find href="games/dayX/index.html"
    pattern = re.compile(r'href="(games/day\d+/index\.html)"')
    links = pattern.findall(content)
    missing = []
    for link in links:
        path = os.path.join(os.path.dirname(INDEX_FILE), link)
        if not os.path.isfile(path):
            missing.append(link)
    if missing:
        print('Missing game files:', ', '.join(missing))
        exit(1)
    print('All linked game files exist.')

if __name__ == '__main__':
    main()
