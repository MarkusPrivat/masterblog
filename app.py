from data.storage import load_blogs_posts
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home():
    blog_posts = load_blogs_posts()
    return render_template('index.html', blog_posts=blog_posts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
