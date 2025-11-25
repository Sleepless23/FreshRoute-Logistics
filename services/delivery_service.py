# ROLE FOR: ANGEL JARED DELA CRUZ
from utils.helpers import select_from_list, input_string
from models.delivery_model import DeliveryModel

VALID_STATUSES = ['Pending', 'Out for Delivery', 'Delivered']

def _select_package_by_status(user_id: int, user_role: str) -> int | None:
    status_choice = select_from_list(
        ["Any Status", *VALID_STATUSES],
        "Returning...",
        "Back",
        "== Filter Packages by Status ==",
    )
    if status_choice is None:
        return None

    status_filter = None if status_choice == 1 else VALID_STATUSES[status_choice - 2]
    packages = DeliveryModel.list_packages_by_status_for_user(status_filter, user_id, user_role)
    if not packages:
        print("No packages found for the selected filter.")
        return None

    options = [f"#{p['package_id']} | {p['recipient_name']} | {p['status']}" for p in packages]
    pick = select_from_list(options, "Returning...", "Back", "== Select Package ==")
    if pick is None:
        return None
    return packages[pick - 1]['package_id']


def update_delivery_status(user_id: int, user_role: str):
    print("=== Update Delivery Status ===")
    package_id = _select_package_by_status(user_id, user_role)
    if package_id is None:
        return

    status_index = select_from_list(VALID_STATUSES, "Cancelled.", "Cancel", "== Select New Status ==")
    if status_index is None:
        return
    new_status = VALID_STATUSES[status_index - 1]

    note = input_string("Optional note (or 'exit' to skip): ", exit_message="Skipping note...", required_input=[], allow_pass=False)
    if note is None:
        note = None

    try:
        DeliveryModel.update_package_status(package_id, new_status, note)
        print(f"Package #{package_id} updated to '{new_status}'.")
    except Exception as e:
        print("Failed to update status:", e)


def add_delivery_note(user_id: int, user_role: str):
    print("=== Add Delivery Note ===")
    package_id = _select_package_by_status(user_id, user_role)
    if package_id is None:
        return

    note = input_string("Enter note (or 'exit' to cancel): ", exit_message="Cancelled.")
    if note is None:
        return

    try:
        DeliveryModel.add_note(package_id, note)
        print(f"Note added to package #{package_id}.")
    except Exception as e:
        print("Failed to add note:", e)


def view_delivery_history(user_id: int, user_role: str):
    print("=== View Delivery History ===")
    package_id = _select_package_by_status(user_id, user_role)
    if package_id is None:
        return

    try:
        history = DeliveryModel.get_delivery_history(package_id)
    except Exception as e:
        print("Failed to fetch history:", e)
        return

    if not history:
        print("No history found for this package.")
        return

    print("\n-- Delivery History --")
    for h in history:
        note = h.get('note') or ''
        print(f"[{h['timestamp']}] {h['status']} - {note}")
