from flask import Flask, render_template, jsonify, request
import sqlite3
import os
import sys

# Add parent directory to path to import moltbook modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'moltbook.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    conn = get_db_connection()
    stats = {
        'posts': conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0],
        'comments': conn.execute('SELECT COUNT(*) FROM comments').fetchone()[0],
        'agents': conn.execute('SELECT COUNT(*) FROM agents').fetchone()[0]
    }
    conn.close()
    return jsonify(stats)

@app.route('/api/posts')
def get_posts():
    limit = request.args.get('limit', 20, type=int)
    conn = get_db_connection()
    posts = conn.execute('''
        SELECT p.*, a.twitter_handle 
        FROM posts p 
        LEFT JOIN agents a ON p.author_name = a.name 
        ORDER BY p.crawled_at DESC 
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in posts])

@app.route('/api/post/<post_id>/comments')
def get_comments(post_id):
    conn = get_db_connection()
    comments = conn.execute('SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC', (post_id,)).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in comments])

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print(f"Warning: Database not found at {DB_PATH}. Please run the crawler first.")
    app.run(debug=True, port=5000)
