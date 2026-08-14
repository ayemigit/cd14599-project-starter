from flask import Flask, request, jsonify, send_from_directory
from backend.order_tracker import OrderTracker
from backend.in_memory_storage import InMemoryStorage

app = Flask(__name__, static_folder='../frontend')
in_memory_storage = InMemoryStorage()
order_tracker = OrderTracker(in_memory_storage)
 
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')
 
 
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)
 
 
@app.route('/api/orders', methods=['POST'])
def add_order_api():
    data = request.get_json(silent=True) or {}
    try:
        order = order_tracker.add_order(
            order_id=data.get("order_id"),
            item_name=data.get("item_name"),
            quantity=data.get("quantity"),
            customer_id=data.get("customer_id"),
            status=data.get("status", "pending"),
        )
        return jsonify(order), 201
    except ValueError as e:
        msg = str(e)
        # Duplicate ID → 409 Conflict; any other validation error → 400
        code = 409 if "already exists" in msg else 400
        return jsonify({"error": msg}), code
 
 
@app.route('/api/orders/<string:order_id>', methods=['GET'])
def get_order_api(order_id):
    try:
        order = order_tracker.get_order_by_id(order_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
 
    if order is None:
        return jsonify({"error": f"Order with ID '{order_id}' not found."}), 404
    return jsonify(order), 200
 
 
@app.route('/api/orders/<string:order_id>/status', methods=['PUT'])
def update_order_status_api(order_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get("new_status")
    try:
        updated = order_tracker.update_order_status(order_id, new_status)
        return jsonify(updated), 200
    except ValueError as e:
        msg = str(e)
        code = 404 if "not found" in msg else 400
        return jsonify({"error": msg}), code
 
 
@app.route('/api/orders', methods=['GET'])
def list_orders_api():
    status = request.args.get("status")
    if status:
        try:
            orders = order_tracker.list_orders_by_status(status)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify(orders), 200
    return jsonify(order_tracker.list_all_orders()), 200
 
 
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
 