import json

from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
BLOG_POSTS_JSON_PATH = PROJECT_ROOT / "blog_posts.json"


def load_blogs_posts() -> list[dict]:
    try:
        with open(BLOG_POSTS_JSON_PATH, 'r', encoding='utf-8') as fileobj:
            return json.loads(fileobj.read())
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def main():
    print(load_blogs_posts())


if __name__ == '__main__':
    main()