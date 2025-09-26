from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# -------------------------
# Sample Data
# -------------------------

# Users for /users/<id> and /sorted-users
users = [
    {"id": 1, "name": "Alice", "company": {"name": "OpenAI"}},
    {"id": 2, "name": "Bob", "company": {"name": "OpenAI"}},
    {"id": 3, "name": "Charlie", "company": {"name": "Google"}},
    {"id": 4, "name": "David", "company": {"name": "Google"}},
    {"id": 5, "name": "Eve", "company": {"name": "Microsoft"}},
    {"id": 6, "name": "Frank", "company": {"name": "Microsoft"}},
    {"id": 7, "name": "Grace", "company": {"name": "OpenAI"}},
    {"id": 8, "name": "Heidi", "company": {"name": "Amazon"}},
    {"id": 9, "name": "Ivan", "company": {"name": "Amazon"}},
    {"id": 10, "name": "Judy", "company": {"name": "Google"}},
]

# Richer /items dataset (50 items, 10 per page) with prices
items = [
    {
        "id": i,
        "name": f"Item {i}",
        "price": round(random.uniform(10, 200), 2)  # price between $10 and $200
    }
    for i in range(1, 51)
]

# Orders with variety for visualization
orders = {
    1001: {"id": 1001, "amount": 50, "currency": "USD", "status": "confirmed"},
    1002: {"id": 1002, "amount": 120, "currency": "USD", "status": "pending"},
    1003: {"id": 1003, "amount": 200, "currency": "USD", "status": "confirmed"},
    1004: {"id": 1004, "amount": 80, "currency": "USD", "status": "pending"},
    1005: {"id": 1005, "amount": 300, "currency": "USD", "status": "confirmed"},
}

# For unstable endpoint
unstable_counter = {"count": 0}

# -------------------------
# Endpoints
# -------------------------

@app.route('/login', methods=['POST'])
def login():
    # Always return a token with expiry (30s)
    return jsonify({
        "token": "abc123",
        "expires_in": 30
    })

@app.route('/protected', methods=['GET'])
def protected():
    auth = request.headers.get("Authorization")
    if auth == "Bearer abc123":
        return jsonify({"message": "Protected data access granted"})
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return jsonify({
        "id": random.randint(100, 999),
        "username": data.get("username"),
        "email": data.get("email"),
        "createdAt": datetime.utcnow().isoformat() + "Z"
    })

@app.route('/user/<int:uid>', methods=['GET'])
def get_user(uid):
    # Return schema-valid user for validation
    return jsonify({
        "id": uid,
        "username": f"user{uid}",
        "email": f"user{uid}@example.com",
        "roles": ["member", "tester"]
    })

@app.route('/users/<int:uid>', methods=['GET'])
def get_user_with_company(uid):
    u = next((u for u in users if u["id"] == uid), None)
    if not u:
        return jsonify({"error": "User not found"}), 404
    return jsonify(u)

@app.route('/book/<int:bid>', methods=['GET'])
def get_book(bid):
    return jsonify({
        "id": bid,
        "title": "The Testing Book",
        "authors": ["Author One", "Author Two"],
        "published": True
    })

@app.route('/items', methods=['GET'])
def get_items():
    page = int(request.args.get("page", 1))
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    page_items = items[start:end]
    next_page = page + 1 if end < len(items) else None
    return jsonify({"items": page_items, "nextPage": next_page})

@app.route('/unstable', methods=['GET'])
def unstable():
    unstable_counter["count"] += 1
    if unstable_counter["count"] % 2 == 0:
        return jsonify({"message": "Success after retry"})
    return jsonify({"error": "Temporary failure"}), 500

@app.route('/event', methods=['GET'])
def event():
    start = datetime.utcnow()
    end = start + timedelta(hours=2)
    return jsonify({
        "name": "Conference",
        "start": start.isoformat() + "Z",
        "end": end.isoformat() + "Z"
    })

@app.route('/order/<int:oid>', methods=['GET'])
def order(oid):
    return jsonify(orders.get(oid, {"error": "not found"}))

@app.route('/sorted-users', methods=['GET'])
def sorted_users():
    # Return descending by ID
    return jsonify({"users": sorted(users, key=lambda u: u["id"], reverse=True)})

# -------------------------
# Run
# -------------------------

if __name__ == "__main__":
    app.run(port=3000, debug=True)
