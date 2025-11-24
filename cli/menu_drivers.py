# ROLE FOR: NICOLE JOHN GARCIA

from services.driver_service import (
    register_driver,
    view_all_drivers,
    view_driver_assigned_route
)
from utils.helpers import select_from_list

def driver_menu():
    while True:
        choice = select_from_list(
            ["Register Driver", "View All Drivers", "View Driver Assigned Route"], 
            "Reverting to main menu...",
            "Back to Main Menu",
            "====== DRIVER MANAGEMENT ======"
        )

        if choice == 1:
            register_driver()
        elif choice == 2:
            view_all_drivers()
        elif choice == 3:
            view_driver_assigned_route()
        elif choice == None:
            break