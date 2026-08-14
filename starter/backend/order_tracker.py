# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.

class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(f"Storage object must implement a callable '{method}' method.")
        self.storage = storage

    def add_order(self, order_id: str, item_name: str, quantity: int, customer_id: str, status: str = "pending"):
        # Validate required string fields
        for field, value in [("order_id", order_id), ("item_name", item_name), ("customer_id", customer_id)]:
            if not value or not isinstance(value, str) or not value.strip():
                raise ValueError(f"'{field}' must be a non-empty string.")
 
        # Validate quantity (bool is a subclass of int in Python, so exclude it explicitly)
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise ValueError("'quantity' must be a positive integer.")
 
        # Validate status before touching storage (fail fast)
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Must be one of: {sorted(VALID_STATUSES)}.")
 
        # Enforce uniqueness
        if self.storage.get_order(order_id) is not None:
            raise ValueError(f"Order with ID '{order_id}' already exists.")
 
        order = {
            "order_id": order_id,
            "item_name": item_name,
            "quantity": quantity,
            "customer_id": customer_id,
            "status": status,
        }
        self.storage.save_order(order)
        return order
 
    def get_order_by_id(self, order_id: str):
        if not order_id or not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("'order_id' must be a non-empty string.")
        return self.storage.get_order(order_id)
 
    def update_order_status(self, order_id: str, new_status: str):
        if not order_id or not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("'order_id' must be a non-empty string.")
 
        # Validate status before hitting storage (fail fast)
        if new_status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Must be one of: {sorted(VALID_STATUSES)}.")
 
        existing = self.storage.get_order(order_id)
        if existing is None:
            raise ValueError(f"Order with ID '{order_id}' not found.")
 
        # Copy rather than mutate the original dict
        updated = {**existing, "status": new_status}
        self.storage.save_order(updated)
        return updated
 
    def list_all_orders(self):
        return self.storage.get_all_orders()
 
    def list_orders_by_status(self, status: str):
        if not status or not isinstance(status, str) or not status.strip():
            raise ValueError("'status' must be a non-empty string.")
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Must be one of: {sorted(VALID_STATUSES)}.")
        return [o for o in self.storage.get_all_orders() if o["status"] == status]
 
