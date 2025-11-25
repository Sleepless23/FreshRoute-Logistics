# ROLE FOR: JOHN GABRIEL GALANG

from services.route_service import (
    create_route,
    assign_driver_to_route,
    view_packages_in_route,
    list_all_routes,
)
from utils.helpers import select_from_list


def route_menu():
    while True:
        choice = select_from_list(
            [
                "Create Route",
                "Assign Driver to Route",
                "View Packages in Route",
                "List All Routes",
            ],
            "Reverting to main menu...",
            "Back to Main Menu",
            "====== ROUTE MANAGEMENT ======",
        )

        if choice == 1:
            create_route()
        elif choice == 2:
            assign_driver_to_route()
        elif choice == 3:
            view_packages_in_route()
        elif choice == 4:
            list_all_routes()
        elif choice is None:
            break