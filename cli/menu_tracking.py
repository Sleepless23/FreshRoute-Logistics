# ROLE FOR: ANGEL JARED DELA CRUZ
from services.delivery_service import (
    update_delivery_status,
    add_delivery_note,
    view_delivery_history,
)
from utils.helpers import select_from_list

def tracking_menu(user_id: int, user_role: str):
    while True:
        if user_role == "driver":
            options = [
                "Update My Delivery Status",
                "Add My Delivery Note",
                "View My Delivery History",
            ]
        else:
            options = [
                "Update Delivery Status",
                "Add Delivery Note",
                "View Delivery History",
            ]

        choice = select_from_list(
            options,
            "Reverting to main menu...",
            "Back to Main Menu",
            "====== DELIVERY TRACKING ======",
        )

        if choice == 1:
            update_delivery_status(user_id, user_role)
        elif choice == 2:
            add_delivery_note(user_id, user_role)
        elif choice == 3:
            view_delivery_history(user_id, user_role)
        elif choice is None:
            break
