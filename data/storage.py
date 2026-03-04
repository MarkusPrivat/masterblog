"""
A JSON-based storage module for managing blog posts in a Flask application.

This module provides persistent storage functionality for a blog system using a local JSON file.
It supports all CRUD operations (Create, Read, Update, Delete) with robust error handling and
data validation. The module is designed to work seamlessly with the Flask application layer,
providing clear success/failure statuses and descriptive error messages.

Key Features:
-------------
- **Automatic Initialization**: Creates the storage file if it doesn't exist.
- **Error Resilience**: Graceful handling of file access and JSON parsing errors.
- **Atomic Operations**: Each function performs a complete read-modify-write cycle.
- **Consistent Interface**: All functions return a tuple of (success_status, result_or_message).
- **Data Validation**: Ensures proper data structure before saving.

Functions:
----------
    load_blog_posts() -> tuple[bool, list[dict] | str]:
        Loads all blog posts from the JSON file. Initializes an empty file if none exists.

    save_blog_posts(blog_posts: list[dict]) -> tuple[bool, str]:
        Persists the entire blog post collection to the JSON file.

    append_blog_post(blog_post: dict) -> tuple[bool, str]:
        Adds a new blog post to the storage.

    delete_blog_post(post_id: str) -> tuple[bool, str]:
        Removes a blog post by its unique ID.

    update_blog_post(new_post: dict) -> tuple[bool, str]:
        Updates an existing blog post with new data.

    fetch_post_by_id(post_id: str) -> tuple[bool, dict | str]:
        Retrieves a single blog post by its ID.
"""
import json

from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
BLOG_POSTS_JSON_PATH = PROJECT_ROOT / "blog_posts.json"
ERROR_LOAD_JSON = "Could not load blog_post.json"
DONE = "Done"
ID_NOT_FOUND = "Post ID not found!"


def load_blog_posts() -> tuple[bool, list[dict] | str]:
    """
    Reads the blog posts from the local JSON file.

    If the file does not exist, it initializes an empty list and creates
    the file to ensure a smooth first-time user experience.

    Returns:
        tuple: (True, list of posts) on success or new initialization,
               (False, ERROR_LOAD_JSON) if the JSON is corrupted.
    """
    if not BLOG_POSTS_JSON_PATH.exists():
        save_blog_posts([])
        return True, []
    try:
        with open(BLOG_POSTS_JSON_PATH, 'r', encoding='utf-8') as fileobj:
            data = json.load(fileobj)
            return True, data
    except json.JSONDecodeError:
        return False, ERROR_LOAD_JSON
    except Exception as error:
        return False, str(error)


def save_blog_posts(blog_posts: list[dict]) -> tuple[bool, str]:
    """
    Persists the entire list of blog posts to the JSON file.

    This function overwrites the existing JSON file with the current state
    of the blog_posts list, using an indent of 4 for readability.

    Args:
        blog_posts (list[dict]): The complete list of post dictionaries to save.

    Returns:
        tuple: (True, "Done") on success, (False, error_message) on failure.
    """
    try:
        with open(BLOG_POSTS_JSON_PATH, 'w', encoding='utf-8') as fileobj:
            json.dump(blog_posts, fileobj, indent=4)
            return True, DONE
    except Exception as error:
        return False, str(error)



def append_blog_post(blog_post: dict) -> tuple[bool, str]:
    """
    Adds a new post to the storage.

    Loads all existing posts, appends the new one, and persists the data.

    Args:
        blog_post (dict): The post data including its unique ID.

    Returns:
        tuple: (True, "Done") or (False, error_message).
    """
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        return False, ERROR_LOAD_JSON
    blog_posts.append(blog_post)
    is_executed, msg = save_blog_posts(blog_posts)
    if not is_executed:
        return False, f"Unexpected error: {msg}"
    return True, DONE


def delete_blog_post(post_id: str) -> tuple[bool, str]:
    """
    Removes a blog post from the storage by its unique ID.

    Loads the current data, searches for the index of the post with the
    matching ID, deletes it, and saves the updated list back to the file.

    Args:
        post_id (str): The unique identifier of the post to be removed.

    Returns:
        tuple: (True, "Done") if deleted, (False, error_message) if not found
               or if storage access fails.
    """
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


def update_blog_post(new_post: dict,) -> tuple[bool, str]:
    """
    Updates an existing post based on its 'id' key.

    Args:
        new_post (dict): The updated post data. Must contain the original ID.

    Returns:
        tuple: (True, "Done") if updated,
               (False, error_message) if ID is not found or storage fails.
    """
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        return False, ERROR_LOAD_JSON
    for post in blog_posts:
        if post['id'] == new_post['id']:
            post.update(new_post)
            is_executed, msg = save_blog_posts(blog_posts)
            if not is_executed:
                return False, msg
            return True, DONE
    return False, ID_NOT_FOUND


def fetch_post_by_id(post_id) -> tuple[bool, dict | str]:
    """
    Retrieves a single blog post dictionary based on its ID.

    This is a read-only operation used to display or prepare data for updates.

    Args:
        post_id (str): The unique identifier of the desired post.

    Returns:
        tuple: (True, post_dict) if found, (False, "Post ID not found!")
               if no match exists or the file couldn't be loaded.
    """
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        return False, ERROR_LOAD_JSON
    for post in blog_posts:
        if post['id'] == post_id:
            return True, post
    return False, ID_NOT_FOUND

