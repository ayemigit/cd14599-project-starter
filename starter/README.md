Order Tracker — Reflection
Validation order as a design decision: In OrderTracker, status is validated before any storage call in both add_order and update_order_status. This "fail fast" approach means invalid input never touches the database layer, which keeps unit tests simpler — a test for a bad status doesn't need to mock storage at all, and test_update_order_status_raises_for_invalid_status explicitly asserts that get_order is never called.
A test that caught a real bug: Writing test_update_order_status_does_not_mutate_original revealed that naively doing existing["status"] = new_status would silently mutate the dict returned by storage. Switching to {**existing, "status": new_status} fixed it — the test would have passed unnoticed otherwise.
Storage interface mismatch: The provided InMemoryStorage.save_order took (order_id, order_data) as separate arguments, but OrderTracker passes a single dict. Aligning the interface to save_order(order: dict) was the right fix — business logic shouldn't need to know how storage keys its records.
Next steps: A DELETE /api/orders/<order_id> endpoint and persistent storage (e.g. SQLite via SQLAlchemy) would be the most valuable additions, along with stricter input validation on the API layer (type-checking quantity before it reaches OrderTracker).

# Udatracker Starter Code

This directory contains the starter code for the Udatracker project. The initial structure of directories and files is described below.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```
