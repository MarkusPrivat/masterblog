import json

from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
BLOG_POSTS_JSON_PATH = PROJECT_ROOT / "blog_posts.json"
ERROR_LOAD_JSON = "Could not load blog_post.json"
DONE = "Done"
ID_NOT_FOUND = "Post ID not found!"


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
            return True, DONE
    except Exception as error:
        return False, str(error)



def append_blog_post(blog_post: dict) -> tuple[bool, str]:
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        return False, ERROR_LOAD_JSON
    blog_posts.append(blog_post)
    is_executed, msg = save_blog_posts(blog_posts)
    if not is_executed:
        return False, f"Unexpected error: {msg}"
    return True, DONE


def delete_blog_post(post_id: str) -> tuple[bool, str]:
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        return False, ERROR_LOAD_JSON
    for index, post in enumerate(blog_posts):
        if post['id'] == post_id:
            del blog_posts[index]
            is_executed, msg = save_blog_posts(blog_posts)
            if not is_executed:
                return False, msg
            return True, DONE
    return False, ID_NOT_FOUND


def update_blog_post(new_post: dict, post_id: str) -> tuple[bool, str]:
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        return False, ERROR_LOAD_JSON
    for post in blog_posts:
        if post['id'] == post_id:
            post.update(new_post)
            is_executed, msg = save_blog_posts(blog_posts)
            if not is_executed:
                return False, msg
            return True, DONE
    return False, ID_NOT_FOUND


def fetch_post_by_id(post_id) -> tuple[bool, dict | str]:
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        return False, ERROR_LOAD_JSON
    for post in blog_posts:
        if post['id'] == post_id:
            return True, post
    return False, ID_NOT_FOUND


def main():
    print(load_blog_posts())


if __name__ == '__main__':
    main()
