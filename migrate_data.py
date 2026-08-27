"""
One-off migration script: copies data from the old SQLite comments.db
into the new Postgres database, via the web container.
"""
import sqlite3
from flask_app import app, db, User, Comment

# --- Step 1: Read everything from the old SQLite database ---
sqlite_conn = sqlite3.connect("/app/comments_old.db")
sqlite_conn.row_factory = sqlite3.Row  # lets us access columns by name
cursor = sqlite_conn.cursor()

cursor.execute("SELECT id, username, password_hash FROM users")
old_users = cursor.fetchall()

cursor.execute("SELECT id, content, posted, commenter_id FROM comments")
old_comments = cursor.fetchall()

sqlite_conn.close()

print(f"Found {len(old_users)} users and {len(old_comments)} comments in the old database.")

# --- Step 2: Insert into Postgres using the Flask app's models ---
with app.app_context():
    for row in old_users:
        user = User(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
        )
        db.session.add(user)

    db.session.commit()
    print(f"Inserted {len(old_users)} users into Postgres.")

    for row in old_comments:
        comment = Comment(
            id=row["id"],
            content=row["content"],
            posted=row["posted"],
            commenter_id=row["commenter_id"],
        )
        db.session.add(comment)

    db.session.commit()
    print(f"Inserted {len(old_comments)} comments into Postgres.")

print("Migration complete.")
