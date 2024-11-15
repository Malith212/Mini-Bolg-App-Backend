from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Import models (defined in models.py)
from models import Post, Comment

# Create the database tables
with app.app_context():
    db.create_all()

# Route to get all posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "comments": [{"id": c.id, "content": c.content} for c in post.comments]
    } for post in posts])

# Route to add a new post
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created"}), 201

# Route to add a comment to a post
@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    data = request.get_json()
    new_comment = Comment(post_id=post.id, content=data['content'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added"}), 201

if __name__ == '__main__':
    app.run(debug=True)
