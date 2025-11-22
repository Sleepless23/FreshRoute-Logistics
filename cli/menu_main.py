from utils.helpers import select_from_list
from auth.register_user import register_user
from cli.menu_drivers import driver_menu
from cli.menu_packages import package_menu
from cli.menu_routes import route_menu
from cli.menu_tracking import tracking_menu
from cli.menu_reports import reports_menu

def menu_main(user_id, user_role, user_full_name, user_username):
    while True:
        menu_options = []
        call_menu_functions = []

        if user_role in ["admin", "dispatcher"]:
            menu_options.append("Package Management")
            menu_options.append("Route Management")
            call_menu_functions.append(package_menu)
            call_menu_functions.append(route_menu)
        if user_role in ["admin", "dispatcher", "driver"]:
            menu_options.append("Delivery Tracking")
            call_menu_functions.append(tracking_menu)
        if user_role in ["admin", "dispatcher", "manager"]:
            menu_options.append("Reports")
            call_menu_functions.append(reports_menu)
        if user_role == "driver":
            menu_options.append("Driver Dashboard")
            call_menu_functions.append(driver_menu)
        if user_role == "admin":
            call_menu_functions.append(register_user)
            menu_options.append("Register New User")

        choice_input = select_from_list(menu_options, "Logging out...", "Log out", "====== MAIN MENU ======")
                
        if choice_input is None or choice_input == 0:
            break

        for options in menu_options:
            if menu_options.index(options) + 1 == choice_input:
                print(f"You selected: {options}")
                call_menu_functions[menu_options.index(options)]()
            
