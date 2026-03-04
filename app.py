from datetime import datetime


from flask import Flask, render_template, request, redirect, url_for

from data.storage import load_blog_posts, append_blog_post






app = Flask(__name__)


@app.route('/')
def home():
    is_executed, blog_posts = load_blog_posts()
    if not is_executed:
        blog_posts = {
            "id": "1",
            "author": "Admin",
            "title": "Sorry, something went wrong.",
            "content": "Blog posts could not be loaded."
        }
    return render_template('index.html', blog_posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        # TODO: Fill this in the next step
        author = request.form.get('author', '')
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        blog_post = {
            'id': str(datetime.now()),
            'author': author,
            'title': title,
            'content': content
        }
        is_executed, msg = append_blog_post(blog_post)
        if not is_executed:
            return msg
        return redirect(url_for('home'))
    return render_template('add.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
