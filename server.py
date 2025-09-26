from flask import Flask, jsonify, request
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# ----------------------------
# Sample data
# ----------------------------
users = [
    {"id": 1, "name": "Alice", "company": {"name": "OpenAI"}},
    {"id": 2, "name": "Bob", "company": {"name": "OpenAI"}},
    {"id": 3, "name": "Charlie", "company": {"name": "Google"}}
]

items = [{"id": i, "name": f"Item {i}"} for i in range(1, 21)]  # 20 items

unstable_counter = 0

# ----------------------------
# Endpoints
# ----------------------------

@app.route("/login", methods=["POST"])
def login():
    return jsonify({"token": "abc123", "expires_in": 60})  # token with expiry

@app.route("/protected", methods=["GET"])
def protected():
    auth = request.headers.get("Authorization")
    if auth == "Bearer abc123":
        return jsonify({"message": "This is protected"})
    return jsonify({"error": "Unauthorized"}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return jsonify({
        "id": random.randint(1000, 9999),
        "username": data.get("username"),
        "email": data.get("email"),
        "createdAt": datetime.utcnow().isoformat() + "Z"
    })

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify({
        "id": user_id,
        "email": f"user{user_id}@mail.com",
        "roles": ["admin", "editor"]
    })

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_with_company(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route("/book/<int:book_id>", methods=["GET"])
def get_book(book_id):
    return jsonify({
        "id": book_id,
        "title": "API Testing with Postman",
        "authors": ["Jane Doe", "John Smith"],
        "published": True
    })

@app.route("/items", methods=["GET"])
def get_items():
    page = int(request.args.get("page", 1))
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    data = items[start:end]
    next_page = page + 1 if end < len(items) else None
    return jsonify({"items": data, "nextPage": next_page})

@app.route("/unstable", methods=["GET"])
def unstable():
    global unstable_counter
    unstable_counter += 1
    if unstable_counter % 2 == 1:
        return jsonify({"error": "Temporary failure"}), 500
    return jsonify({"message": "Success after retry"})

@app.route("/event", methods=["GET"])
def event():
    start = datetime.utcnow()
    end = start + timedelta(hours=1)
    return jsonify({
        "start": start.isoformat() + "Z",
        "end": end.isoformat() + "Z"
    })

@app.route("/order/<int:order_id>", methods=["GET"])
def order(order_id):
    return jsonify({
        "id": order_id,
        "amount": random.randint(50, 500),
        "currency": "USD",
        "status": random.choice(["confirmed", "pending"])
    })

@app.route("/sorted-users", methods=["GET"])
def sorted_users():
    sorted_list = sorted(users, key=lambda u: u["id"], reverse=True)
    return jsonify({"users": sorted_list})

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run(port=3000, debug=True)
