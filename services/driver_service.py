# ROLE FOR: NICOLE JOHN GARCIA
from utils.helpers import select_from_list, input_string
from models.driver_model import DriverModel
from services.user_service import update_user_service


def register_driver():
    print("=== Register Driver ===")

    # ensure we are linking to an existing user with role 'driver'
    username = input_string("Driver's username (or 'exit' to cancel): ", exit_message="Cancelled.")
    if username is None:
        return
    user = DriverModel.get_user_by_username(username)
    if not user:
        print(f"user '{username}' not found.")
        create_new = input("Would you like to create a new driver? (y/N): ").strip().lower()
        if create_new == 'y':
            # Create new user as driver
            full_name = input_string("Driver's full name: ", "Cancelled.")
            if full_name is None:
                return
            password = input_string("Password: ", "Cancelled.", [], True)
            if password is None:
                return
            confirm_password = input_string("Confirm Password: ", "Cancelled.", [], True)
            if confirm_password is None:
                return
            if password != confirm_password:
                print("Passwords do not match.")
                return
            # Create user
            from services.user_service import create_user_service
            success = create_user_service(full_name, username, password, 'driver')
            if success:
                print(f"Driver '{username}' created successfully!")
            else:
                print("Failed to create driver.")
        return
    if user['role'] == 'driver':
        print(f"User {user['username']} is already a driver.")
        return

    # Update role to driver
    try:
        success = update_user_service(user['user_id'], user['full_name'], user['username'], 'driver')
        if success:
            print(f"User {user['username']} has been registered as a driver.")
        else:
            print("Failed to update user role.")
    except ValueError as e:
        print(e)


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
        f"Fuel Estimate: {route['fuel_estimate']}")
