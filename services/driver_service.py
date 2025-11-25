# ROLE FOR: NICOLE JOHN GARCIA
from utils.helpers import select_from_list, input_string
from models.driver_model import DriverModel


def register_driver():
    print("=== Register Driver ===")

    # ensure we are linking to an existing user with role 'driver'
    username = input_string("Driver's username (or 'exit' to cancel): ", exit_message="Cancelled.")
    if username is None:
        return
    user = DriverModel.get_user_by_username(username)
    if not user:
        print("User not found.")
        return
    if user['role'] != 'driver':
        print("User exists but role is not 'driver'. Update user role first.")
        return

    print(f"User {user['username']} is already a driver.")


def view_all_drivers():
    print("=== All Drivers ===")
    try:
        drivers = DriverModel.list_drivers()
    except Exception as e:
        print("Failed to load drivers:", e)
        return

    if not drivers:
        print("No drivers found.")
        return

    for d in drivers:
        print(f"#{d['user_id']} | {d['full_name']} (@{d['username']})")


def view_driver_assigned_route(driver_id=None):
    print("=== View Driver Assigned Route ===")
    # If driver_id provided, use it; else choose from list
    if driver_id is None:
        try:
            drivers = DriverModel.list_drivers()
        except Exception as e:
            print("Failed to load drivers:", e)
            return

        if not drivers:
            print("No drivers found.")
            return

        options = [f"#{d['user_id']} | {d['full_name']} (@{d['username']})" for d in drivers]
        pick = select_from_list(options, "Returning...", "Back", "== Select Driver ==")
        if pick is None:
            return

        driver = drivers[pick - 1]
        selected_driver_id = driver['user_id']
    else:
        selected_driver_id = driver_id

    try:
        route = DriverModel.get_user_assigned_route(selected_driver_id)
    except Exception as e:
        print("Failed to fetch route:", e)
        return

    if not route:
        print("Driver has no assigned route.")
        return

    print(
        f"Route #{route['route_id']} | {route['route_name']} | Date: {route['route_date']} | "
        f"Fuel Estimate: {route['fuel_estimate']}"
    )
