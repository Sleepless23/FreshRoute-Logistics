# ROLE FOR: NICOLE JOHN GARCIA

driver_service.py
from utils.helpers import select_from_list, input_string
from models.driver_model import DriverModel


def register_driver():
    print("=== Register Driver ===")

    # ensure we are linking to an existing user with role 'driver'
    while True:
        username = input_string("Driver's username (or 'exit' to cancel): ", exit_message="Cancelled.")
        if username is None:
            return
        user = DriverModel.get_user_by_username(username)
        if not user:
            print("User not found. Try again or type 'exit'.")
            continue
        if user['role'] != 'driver':
            print("User exists but role is not 'driver'. Update user role before registering as driver.")
            continue
        break

    license_number = input_string("License number (or 'exit' to skip): ", exit_message="Skipping...")
    if license_number is None:
        license_number = None

    phone = input_string("Phone (or 'exit' to skip): ", exit_message="Skipping...")
    if phone is None:
        phone = None

    try:
        driver_id = DriverModel.create_driver(user['user_id'], license_number, phone)
        print(f"Driver registered with ID {driver_id} for user {user['username']}.")
    except Exception as e:
        print("Failed to register driver:", e)


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
        print(
            f"#{d['driver_id']} | {d['full_name']} (@{d['username']}) | "
            f"License: {d.get('license_number') or '-'} | Phone: {d.get('phone') or '-'} | "
            f"Assigned today: {'Yes' if d.get('assigned_today') else 'No'}"
        )


def view_driver_assigned_route():
    print("=== View Driver Assigned Route ===")
    # Choose a driver from the list
    try:
        drivers = DriverModel.list_drivers()
    except Exception as e:
        print("Failed to load drivers:", e)
        return

    if not drivers:
        print("No drivers found.")
        return

    options = [f"#{d['driver_id']} | {d['full_name']} (@{d['username']})" for d in drivers]
    pick = select_from_list(options, "Returning...", "Back", "== Select Driver ==")
    if pick is None:
        return

    driver = drivers[pick - 1]

    try:
        route = DriverModel.get_driver_assigned_route(driver['driver_id'])
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