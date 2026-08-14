import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty list
    mock.get_all_orders.return_value = []
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

# ---------------------------------------------------------------------------
# add_order — provided examples
# ---------------------------------------------------------------------------

def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")

    # We expect save_order to be called once
    mock_storage.save_order.assert_called_once()

def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises a ValueError."""
    # Simulate that the storage finds an existing order
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    with pytest.raises(ValueError, match="Order with ID 'ORD_EXISTING' already exists."):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")

# ---------------------------------------------------------------------------
# add_order — learner tests
# ---------------------------------------------------------------------------

def test_add_order_defaults_status_to_pending(order_tracker, mock_storage):
    """When no status is supplied the stored order should have status 'pending'."""
    order_tracker.add_order("ORD002", "Mouse", 2, "CUST002")

    saved = mock_storage.save_order.call_args[0][0]
    assert saved["status"] == "pending"

def test_add_order_stores_all_fields_correctly(order_tracker, mock_storage):
    """The dict passed to save_order must contain every supplied field."""
    order_tracker.add_order("ORD003", "Keyboard", 3, "CUST003")

    saved = mock_storage.save_order.call_args[0][0]
    assert saved["order_id"] == "ORD003"
    assert saved["item_name"] == "Keyboard"
    assert saved["quantity"] == 3
    assert saved["customer_id"] == "CUST003"

def test_add_order_accepts_explicit_valid_status(order_tracker, mock_storage):
    """An explicit valid status should be stored as-is."""
    order_tracker.add_order("ORD004", "Monitor", 1, "CUST004", status="processing")

    saved = mock_storage.save_order.call_args[0][0]
    assert saved["status"] == "processing"

def test_add_order_raises_for_invalid_status(order_tracker):
    """An unrecognised initial status must raise ValueError."""
    with pytest.raises(ValueError, match="Invalid status 'dispatched'"):
        order_tracker.add_order("ORD005", "Desk", 1, "CUST005", status="dispatched")

def test_add_order_raises_for_zero_quantity(order_tracker):
    """quantity=0 is not a positive integer and must raise ValueError."""
    with pytest.raises(ValueError, match="'quantity' must be a positive integer"):
        order_tracker.add_order("ORD006", "Chair", 0, "CUST006")

def test_add_order_raises_for_negative_quantity(order_tracker):
    """Negative quantities must raise ValueError."""
    with pytest.raises(ValueError, match="'quantity' must be a positive integer"):
        order_tracker.add_order("ORD007", "Lamp", -1, "CUST007")

def test_add_order_raises_for_empty_order_id(order_tracker):
    """An empty order_id string must raise ValueError."""
    with pytest.raises(ValueError, match="'order_id' must be a non-empty string"):
        order_tracker.add_order("", "Pen", 1, "CUST008")

def test_add_order_raises_for_empty_item_name(order_tracker):
    """An empty item_name must raise ValueError."""
    with pytest.raises(ValueError, match="'item_name' must be a non-empty string"):
        order_tracker.add_order("ORD009", "", 1, "CUST009")

def test_add_order_raises_for_empty_customer_id(order_tracker):
    """An empty customer_id must raise ValueError."""
    with pytest.raises(ValueError, match="'customer_id' must be a non-empty string"):
        order_tracker.add_order("ORD010", "Stapler", 1, "")

def test_add_order_does_not_save_on_validation_failure(order_tracker, mock_storage):
    """save_order must NOT be called when validation fails."""
    with pytest.raises(ValueError):
        order_tracker.add_order("", "Pen", 1, "CUST011")

    mock_storage.save_order.assert_not_called()

# ---------------------------------------------------------------------------
# get_order_by_id
# ---------------------------------------------------------------------------

def test_get_order_by_id_returns_existing_order(order_tracker, mock_storage):
    """Should return the order dict when the ID exists in storage."""
    expected = {
        "order_id": "ORD100", "item_name": "Laptop",
        "quantity": 1, "customer_id": "CUST100", "status": "pending",
    }
    mock_storage.get_order.return_value = expected

    result = order_tracker.get_order_by_id("ORD100")

    assert result == expected
    mock_storage.get_order.assert_called_once_with("ORD100")

def test_get_order_by_id_returns_none_for_nonexistent_order(order_tracker, mock_storage):
    """Should return None when the ID is not in storage."""
    result = order_tracker.get_order_by_id("DOES_NOT_EXIST")
    assert result is None

def test_get_order_by_id_raises_for_empty_id(order_tracker):
    """An empty string ID must raise ValueError — not silently return None."""
    with pytest.raises(ValueError, match="'order_id' must be a non-empty string"):
        order_tracker.get_order_by_id("")

def test_get_order_by_id_raises_for_whitespace_id(order_tracker):
    """A whitespace-only ID must also raise ValueError."""
    with pytest.raises(ValueError, match="'order_id' must be a non-empty string"):
        order_tracker.get_order_by_id("   ")

# ---------------------------------------------------------------------------
# update_order_status
# ---------------------------------------------------------------------------

def test_update_order_status_successfully(order_tracker, mock_storage):
    """Happy path: existing order gets its status changed and is re-saved."""
    mock_storage.get_order.return_value = {
        "order_id": "ORD200", "item_name": "Tablet",
        "quantity": 1, "customer_id": "CUST200", "status": "pending",
    }

    result = order_tracker.update_order_status("ORD200", "shipped")

    assert result["status"] == "shipped"
    mock_storage.save_order.assert_called_once()

def test_update_order_status_preserves_other_fields(order_tracker, mock_storage):
    """Fields other than status must be preserved after the update."""
    mock_storage.get_order.return_value = {
        "order_id": "ORD201", "item_name": "Phone",
        "quantity": 2, "customer_id": "CUST201", "status": "pending",
    }

    result = order_tracker.update_order_status("ORD201", "processing")

    assert result["order_id"] == "ORD201"
    assert result["item_name"] == "Phone"
    assert result["quantity"] == 2
    assert result["customer_id"] == "CUST201"

def test_update_order_status_does_not_mutate_original(order_tracker, mock_storage):
    """update_order_status should work on a copy, leaving the original dict intact."""
    original = {
        "order_id": "ORD202", "item_name": "X",
        "quantity": 1, "customer_id": "C", "status": "pending",
    }
    mock_storage.get_order.return_value = original

    order_tracker.update_order_status("ORD202", "delivered")

    assert original["status"] == "pending"

def test_update_order_status_raises_for_invalid_status(order_tracker, mock_storage):
    """An unrecognised status must raise ValueError BEFORE storage is queried."""
    with pytest.raises(ValueError, match="Invalid status 'lost'"):
        order_tracker.update_order_status("ORD203", "lost")

    mock_storage.get_order.assert_not_called()

def test_update_order_status_raises_for_nonexistent_order(order_tracker, mock_storage):
    """Updating a non-existent order must raise ValueError."""
    mock_storage.get_order.return_value = None

    with pytest.raises(ValueError, match="Order with ID 'GHOST' not found"):
        order_tracker.update_order_status("GHOST", "shipped")

def test_update_order_status_raises_for_empty_order_id(order_tracker):
    """An empty order_id must raise ValueError."""
    with pytest.raises(ValueError, match="'order_id' must be a non-empty string"):
        order_tracker.update_order_status("", "shipped")

def test_update_order_status_raises_for_whitespace_order_id(order_tracker):
    """A whitespace-only order_id must raise ValueError."""
    with pytest.raises(ValueError, match="'order_id' must be a non-empty string"):
        order_tracker.update_order_status("   ", "shipped")

# ---------------------------------------------------------------------------
# list_all_orders
# ---------------------------------------------------------------------------

def test_list_all_orders_returns_empty_list_when_no_orders(order_tracker, mock_storage):
    """Should return an empty list when storage is empty."""
    result = order_tracker.list_all_orders()
    assert result == []

def test_list_all_orders_returns_all_orders(order_tracker, mock_storage):
    """Should return every order that storage holds."""
    orders = [
        {"order_id": "A", "item_name": "X", "quantity": 1, "customer_id": "C1", "status": "pending"},
        {"order_id": "B", "item_name": "Y", "quantity": 2, "customer_id": "C2", "status": "shipped"},
        {"order_id": "C", "item_name": "Z", "quantity": 3, "customer_id": "C3", "status": "delivered"},
    ]
    mock_storage.get_all_orders.return_value = orders

    result = order_tracker.list_all_orders()

    assert len(result) == 3
    assert {o["order_id"] for o in result} == {"A", "B", "C"}

def test_list_all_orders_returns_single_order_as_list(order_tracker, mock_storage):
    """A single order should come back as a one-element list."""
    mock_storage.get_all_orders.return_value = [
        {"order_id": "SOLO", "item_name": "Pen", "quantity": 5,
         "customer_id": "C99", "status": "processing"},
    ]

    result = order_tracker.list_all_orders()

    assert len(result) == 1
    assert result[0]["order_id"] == "SOLO"

# ---------------------------------------------------------------------------
# list_orders_by_status
# ---------------------------------------------------------------------------

def test_list_orders_by_status_returns_only_matching_orders(order_tracker, mock_storage):
    """Should filter down to orders whose status matches the argument."""
    mock_storage.get_all_orders.return_value = [
        {"order_id": "A", "item_name": "X", "quantity": 1, "customer_id": "C1", "status": "shipped"},
        {"order_id": "B", "item_name": "Y", "quantity": 2, "customer_id": "C2", "status": "pending"},
        {"order_id": "C", "item_name": "Z", "quantity": 3, "customer_id": "C3", "status": "shipped"},
    ]

    result = order_tracker.list_orders_by_status("shipped")

    assert len(result) == 2
    assert all(o["status"] == "shipped" for o in result)

def test_list_orders_by_status_returns_empty_when_none_match(order_tracker, mock_storage):
    """Should return an empty list when no orders have the given status."""
    mock_storage.get_all_orders.return_value = [
        {"order_id": "A", "item_name": "X", "quantity": 1, "customer_id": "C1", "status": "pending"},
    ]

    result = order_tracker.list_orders_by_status("delivered")

    assert result == []

def test_list_orders_by_status_returns_empty_when_storage_empty(order_tracker):
    """Should return an empty list when storage has nothing."""
    result = order_tracker.list_orders_by_status("pending")
    assert result == []

def test_list_orders_by_status_raises_for_empty_status(order_tracker):
    """An empty status string must raise ValueError."""
    with pytest.raises(ValueError, match="'status' must be a non-empty string"):
        order_tracker.list_orders_by_status("")

def test_list_orders_by_status_raises_for_whitespace_status(order_tracker):
    """A whitespace-only status must raise ValueError."""
    with pytest.raises(ValueError, match="'status' must be a non-empty string"):
        order_tracker.list_orders_by_status("   ")

def test_list_orders_by_status_raises_for_invalid_status(order_tracker):
    """An unrecognised status must raise ValueError."""
    with pytest.raises(ValueError, match="Invalid status 'archived'"):
        order_tracker.list_orders_by_status("archived")