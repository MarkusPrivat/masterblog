import json

from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
BLOG_POSTS_JSON_PATH = PROJECT_ROOT / "blog_posts.json"


def load_blog_posts() -> tuple[bool, list[dict]]:
    try:
        with open(BLOG_POSTS_JSON_PATH, 'r', encoding='utf-8') as fileobj:
            return True, json.loads(fileobj.read())
    except (json.JSONDecodeError, FileNotFoundError):
        return False, []


def save_blog_posts(blog_posts: list[dict]) -> tuple[bool, str]:
    try:
        with open(BLOG_POSTS_JSON_PATH, 'w', encoding='utf-8') as fileobj:
            json.dump(blog_posts, fileobj, indent=4)
            return True, "Done"
    except Exception as error:
        return False, error



def append_blog_post(blog_post: dict) -> tuple[bool, str]:
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        return False, "Could not load blog_post.json"
    blog_posts.append(blog_post)
    is_executed, msg = save_blog_posts(blog_posts)
    if not is_executed:
        return False, f"Unexpected error: {msg}"
    return True, "Done"


def main():
    print(load_blog_posts())


if __name__ == '__main__':
    main()