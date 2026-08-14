# This file provides a simple in-memory storage implementation for orders.
# Data stored here will be lost when the application restarts.

class InMemoryStorage:
    """
    A simple in-memory implementation of the storage interface.
    Stores orders in a Python dictionary keyed by order_id.
    """
    def __init__(self):
        self._orders = {}

    def save_order(self, order: dict):
        """Insert or overwrite an order, keyed by its order_id."""
        self._orders[order["order_id"]] = order.copy()

    def get_order(self, order_id: str):
        """Return a copy of the order dict, or None if not found."""
        order = self._orders.get(order_id)
        return order.copy() if order else None

    def get_all_orders(self):
        """Return all orders as a list of dicts."""
        return [v.copy() for v in self._orders.values()]

    def clear(self):
        """Reset storage — used between tests."""
        self._orders = {}