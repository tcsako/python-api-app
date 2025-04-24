from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Mock data
products = [
    {"id": 1, "title": "Product 1", "description": "Description of Product 1", "price": 29.99, "stock": 100, "category": "Electronics"},
    {"id": 2, "title": "Product 2", "description": "Description of Product 2", "price": 49.99, "stock": 50, "category": "Books"},
    {"id": 3, "title": "Product 3", "description": "Description of Product 3", "price": 19.99, "stock": 200, "category": "Home"},
]

users = [
    {"id": 1, "username": "admin", "password": "adminpassword", "email": "admin@example.com", "role": "admin", "token": "admin_token"},
    {"id": 2, "username": "user1", "password": "user1password", "email": "user1@example.com", "role": "user", "token": "user1_token"},
    {"id": 3, "username": "user2", "password": "user2password", "email": "user2@example.com", "role": "user", "token": "user2_token"}
]

carts = {user['id']: {"items": [], "total": 0} for user in users}
orders = {user['id']: [] for user in users}

def log_request_response(func):
    """Decorator to log request and response."""
    def wrapper(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            logging.debug(f"Request: {request.method} {request.url} - {request.json}")
        else:
            logging.debug(f"Request: {request.method} {request.url}")
        response = func(*args, **kwargs)
        if isinstance(response, tuple):
            response_data, status_code = response
            logging.debug(f"Response: {status_code} - {response_data}")
        else:
            logging.debug(f"Response: {response.status_code} - {response.get_json()}")
        return response
    wrapper.__name__ = func.__name__  # Ensure unique function names
    return wrapper

@app.route('/products', methods=['GET'])
@log_request_response
def get_products():
    """Endpoint to list all products."""
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
@log_request_response
def get_product(product_id):
    """Endpoint to get a specific product by ID."""
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

@app.route('/products', methods=['POST'])
@log_request_response
def add_product():
    """Endpoint to add a new product. Requires admin authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user = next((u for u in users if u['token'] == user_token), None)
    if not user or user['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    new_product = request.json
    required_fields = ["title", "description", "price", "stock", "category"]
    for field in required_fields:
        if field not in new_product:
            return jsonify({"error": f"'{field}' is required"}), 422

    if not isinstance(new_product['price'], (int, float)):
        return jsonify({"error": "'price' must be a number"}), 422
    if not isinstance(new_product['stock'], int):
        return jsonify({"error": "'stock' must be an integer"}), 422

    new_product['id'] = len(products) + 1
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/products/<int:product_id>', methods=['PATCH'])
@log_request_response
def update_product_partial(product_id):
    """Endpoint to partially update an existing product by ID. Requires admin authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user = next((u for u in users if u['token'] == user_token), None)
    if not user or user['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    updated_data = request.json
    for key, value in updated_data.items():
        if key in product:
            product[key] = value

    return jsonify(product)

@app.route('/products/<int:product_id>', methods=['PUT'])
@log_request_response
def update_product(product_id):
    """Endpoint to update an existing product by ID. Requires admin authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user = next((u for u in users if u['token'] == user_token), None)
    if not user or user['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    updated_data = request.json
    for key, value in updated_data.items():
        if key in product:
            product[key] = value

    return jsonify(product)

@app.route('/products/<int:product_id>', methods=['DELETE'])
@log_request_response
def delete_product(product_id):
    """Endpoint to delete a product by ID. Requires admin authentication."""
    global products  # Declare products as global at the start of the function

    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user = next((u for u in users if u['token'] == user_token), None)
    if not user or user['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    # Check if the product exists
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Delete the product
    products = [p for p in products if p['id'] != product_id]
    return '', 204


@app.route('/users/register', methods=['POST'])
@log_request_response
def register_user():
    """Endpoint to register a new user."""
    new_user = request.json
    new_user['id'] = len(users) + 1
    new_user['token'] = f"{new_user['username']}_token"
    users.append(new_user)
    carts[new_user['id']] = {"items": [], "total": 0}
    orders[new_user['id']] = []
    return jsonify({"id": new_user['id'], "username": new_user['username'], "email": new_user['email']}), 201

@app.route('/users/login', methods=['POST'])
@log_request_response
def login_user():
    """Endpoint for user login. Returns a dynamic JWT token."""
    username = request.json.get('username')
    password = request.json.get('password')
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    token = user['token']
    return jsonify({"token": token})

@app.route('/users/<int:user_id>', methods=['PUT'])
@log_request_response
def update_user(user_id):
    """Endpoint to update user profile. Requires authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user_token != user['token']:
        return jsonify({"error": "Unauthorized access"}), 403

    user.update(request.json)
    return jsonify({"id": user['id'], "username": user['username'], "email": user['email']})

@app.route('/users/reset-password', methods=['POST'])
@log_request_response
def reset_password():
    """Endpoint to reset password. Sends a reset link to the user's email."""
    email = request.json.get('email')
    user = next((u for u in users if u['email'] == email), None)
    if not user:
        return jsonify({"error": "Email not found"}), 404
    return jsonify({"message": "Password reset link sent to email."})

@app.route('/cart', methods=['GET'])
@log_request_response
def view_cart():
    """Endpoint to view cart contents. Requires authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user_id = next((u['id'] for u in users if u['token'] == user_token), None)
    if user_id is None:
        return jsonify({"error": "Unauthorized access"}), 403

    cart = carts.get(user_id, {"items": [], "total": 0})
    return jsonify(cart)

@app.route('/cart/add', methods=['POST'])
@log_request_response
def add_to_cart():
    """Endpoint to add product to cart. Requires authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user_id = next((u['id'] for u in users if u['token'] == user_token), None)
    if user_id is None:
        return jsonify({"error": "Unauthorized access"}), 403

    product_id = request.json.get('productId')
    quantity = request.json.get('quantity')
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if user_id not in carts:
        carts[user_id] = {"items": [], "total": 0}
    carts[user_id]['items'].append({"productId": product_id, "quantity": quantity})
    carts[user_id]['total'] += product['price'] * quantity
    return jsonify({"message": "Product added to cart."})

@app.route('/cart/remove', methods=['DELETE'])
@log_request_response
def remove_from_cart():
    """Endpoint to remove product from cart. Requires authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user_id = next((u['id'] for u in users if u['token'] == user_token), None)
    if user_id is None:
        return jsonify({"error": "Unauthorized access"}), 403

    product_id = request.json.get('productId')
    if user_id not in carts:
        return jsonify({"error": "Cart not found"}), 404

    cart = carts[user_id]
    cart['items'] = [item for item in cart['items'] if item['productId'] != product_id]
    return jsonify({"message": "Product removed from cart."})

@app.route('/orders', methods=['POST'])
@log_request_response
def create_order():
    """Endpoint to create an order. Requires authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user_id = next((u['id'] for u in users if u['token'] == user_token), None)
    if user_id is None:
        return jsonify({"error": "Unauthorized access"}), 403

    cart_items = request.json.get('cartItems')
    shipping_address = request.json.get('shippingAddress')
    order_id = len(orders[user_id]) + 1
    total = sum(next(p['price'] for p in products if p['id'] == item['productId']) * item['quantity'] for item in cart_items)
    orders[user_id].append({"orderId": order_id, "status": "Processing", "items": cart_items, "total": total, "shippingAddress": shipping_address})
    return jsonify({"orderId": order_id, "status": "Processing"})

@app.route('/orders/<int:order_id>', methods=['GET'])
@log_request_response
def get_order(order_id):
    """Endpoint to get order status. Requires authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user_id = next((u['id'] for u in users if u['token'] == user_token), None)
    if user_id is None:
        return jsonify({"error": "Unauthorized access"}), 403

    order = next((o for o in orders[user_id] if o['orderId'] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)

@app.route('/orders/<int:order_id>', methods=['DELETE'])
@log_request_response
def delete_order(order_id):
    """Endpoint to delete an order. Requires authentication."""
    token = request.headers.get('Authorization')
    if not token or len(token.split()) != 2 or token.split()[0] != "Bearer":
        return jsonify({"error": "Missing or invalid token"}), 401

    user_token = token.split()[1]
    user_id = next((u['id'] for u in users if u['token'] == user_token), None)
    if user_id is None:
        return jsonify({"error": "Unauthorized access"}), 403

    orders[user_id] = [o for o in orders[user_id] if o['orderId'] != order_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
