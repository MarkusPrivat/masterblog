"""
A Flask-based web application for managing a blog with CRUD operations.

This module implements a web interface for a blog system, allowing users to:
- View all blog posts.
- Add new blog posts.
- Update existing blog posts.
- Delete blog posts with confirmation.

The application uses Flask for routing and templating, and relies on a separate
`data.storage` module for persistent storage operations (e.g., loading, saving,
updating, and deleting blog posts).

Key Features:
-------------
- **CRUD Operations**: Full support for Create, Read, Update, and Delete operations on blog posts.
- **User Feedback**: Flash messages for success, warning, and error states.
- **Input Validation**: Server-side validation for form inputs and deletion confirmations.
- **Error Handling**: Graceful fallbacks for storage errors and missing posts.
- **Unique IDs**: Automatic generation of unique post IDs using microsecond-precision timestamps.

Dependencies:
-------------
- Flask: For web routing, templating, and session management.
- data.storage: For persistent storage operations (load, append, update, delete, fetch).

Routes:
-------
    / (GET):
        Displays the home page with all blog posts.
    /add (GET, POST):
        Handles the creation of new blog posts.
    /delete/<post_id> (GET, POST):
        Manages the deletion of a blog post with confirmation.
    /update/<post_id> (GET, POST):
        Handles the editing of an existing blog post.
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

from data.storage import (load_blog_posts, append_blog_post, delete_blog_post,
                          update_blog_post, fetch_post_by_id)


app = Flask(__name__)
app.secret_key = 'top_secret_secret'
NOT_IN_JSON = "Blog post not in blog_posts.json"
ERROR_LOAD_POSTS = "Error loading Blog posts"
NO_FORM_DELETE = "You did not enter 'DELETE'"


@app.route('/')
def home():
    """
    Renders the home page with all available blog posts.

    Fetches blog posts from the storage module. If the loading process fails,
    a fallback list containing a system error message is displayed to the user
    to prevent the template from crashing.

    Returns:
        str: The rendered HTML content of 'index.html'.
    """
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        blog_posts = [{
            "id": "1",
            "author": "Admin",
            "title": "Sorry, something went wrong.",
            "content": "Blog posts could not be loaded."
        }]
    return render_template('index.html', blog_posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handles the creation of a new blog post.

    GET: Displays the 'add.html' form.
    POST: Processes the form data, generates a unique ID with microsecond
          precision, and attempts to save the new post.
          Uses Flask flashing to provide feedback on success or failure.

    Returns:
        str: The rendered 'add.html' template or a redirect to the home page.
    """
    if request.method == 'POST':
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not author or not title or not content:
            flash("All fields are required and cannot be empty or just whitespace.", "error")
            return redirect(url_for('add'))

        blog_post = {
            'author': author,
            'title': title,
            'content': content
        }
        is_executed, msg = append_blog_post(blog_post)
        if not is_executed:
            flash(msg, 'error')
            return redirect(url_for('home'))
        flash("Blog post created successfully!", 'success')
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/delete/<post_id>', methods=['GET', 'POST'])
def delete(post_id):
    """
    Manages the deletion of a specific blog post.

    GET: Fetches the post by its ID to display a confirmation page.
         If the post doesn't exist, redirects to home with an error.
    POST: Validates that the user typed 'DELETE' in the confirmation form.
          If valid, removes the post from storage.
          Provides feedback via 'success', 'warning', or 'error' flash messages.

    Args:
        post_id (str): The unique identifier of the post to be deleted.

    Returns:
        str: The rendered 'delete.html' template or a redirect to the home page.
    """
    if request.method == 'POST':
        form_delete = request.form.get('delete')
        if form_delete == 'DELETE':
            is_executed, msg = delete_blog_post(post_id)
            if not is_executed:
                flash(msg, 'error')
                return redirect(url_for('home'))
            flash("Post deleted successfully!", 'success')
            return redirect(url_for('home'))
        flash(NO_FORM_DELETE, 'warning')
        return redirect(url_for('home', post_id=post_id))

    is_executed, post = fetch_post_by_id(post_id)
    if not is_executed:
        flash(ERROR_LOAD_POSTS, 'error')
        return redirect(url_for('home'))
    return render_template('delete.html', post=post)



@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handles the editing of an existing blog post.

    Initializes by fetching the post by ID. If the post is not found,
    the user is redirected home with an error message.

    GET: Renders the 'update.html' form pre-populated with current post data.
    POST: Extracts updated data from the form, updates the post object
          (preserving the ID), and saves changes to the storage.
          Displays success or error feedback via flash messages.

    Args:
        post_id (str): The unique identifier of the post to be updated.

    Returns:
        str: The rendered 'update.html' template or a redirect to the home page.
    """
    is_executed, post = fetch_post_by_id(post_id)
    if not is_executed:
        flash(ERROR_LOAD_POSTS, 'error')
        return redirect(url_for('home'))
    if request.method == 'POST':
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not author or not title or not content:
            flash("All fields are required and cannot be empty or just whitespace.", "error")
            return redirect(url_for('add'))

        post.update({
            'author': author,
            'title': title,
            'content': content
        })
        is_executed, msg = update_blog_post(post)
        if not is_executed:
            flash(msg, 'error')
            return redirect(url_for('home'))
        flash("Changes saved successfully!", 'success')
        return redirect(url_for('home'))
    return render_template('update.html', post=post, post_id=post_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
