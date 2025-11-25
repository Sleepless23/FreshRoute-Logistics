# ROLE FOR: JOHN GABRIEL GALANG

from utils.helpers import select_from_list, input_string
from models.route_model import RouteModel


def _pick_route() -> dict | None:
    routes = RouteModel.list_all_routes()
    if not routes:
        print("No routes available.")
        return None
    options = [f"#{r['route_id']} | {r['route_name']} | {r['route_date']} | Driver: {r.get('driver_name') or '-'}" for r in routes]
    idx = select_from_list(options, "Returning...", "Back", "== Select Route ==")
    if idx is None:
        return None
    return routes[idx - 1]


def _pick_driver() -> dict | None:
    drivers = RouteModel.list_drivers()
    if not drivers:
        print("No drivers available.")
        return None
    options = [f"#{d['driver_id']} | {d['full_name']} (@{d['username']}) | Assigned Today: {'Yes' if d.get('assigned_today') else 'No'}" for d in drivers]
    idx = select_from_list(options, "Returning...", "Back", "== Select Driver ==")
    if idx is None:
        return None
    return drivers[idx - 1]


def create_route():
    print("=== Create Route ===")
    route_name = input_string("Route name (or 'exit' to cancel): ", exit_message="Cancelled.")
    if route_name is None:
        return

    route_date = input_string("Route date (YYYY-MM-DD) (or 'exit' to cancel): ", exit_message="Cancelled.")
    if route_date is None:
        return

    # optional fuel estimate
    while True:
        fuel = input_string("Fuel estimate (optional, e.g., 50.5) or 'exit' to skip: ", exit_message="Skipping...")
        if fuel is None:
            fuel_est = None
            break
        try:
            fuel_est = float(fuel)
            break
        except ValueError:
            print("Please enter a valid number.")

    # optional driver assignment
    assign_now = select_from_list(["Assign a driver now"], "Skipping driver assignment...", "Skip", "== Driver Assignment ==")
    driver_id = None
    if assign_now is not None:
        d = _pick_driver()
        if d:
            driver_id = d['driver_id']

    try:
        route_id = RouteModel.create_route(route_name, route_date, fuel_est, driver_id)
        print(f"Route created with ID {route_id}.")
    except Exception as e:
        print("Failed to create route:", e)


def assign_driver_to_route():
    print("=== Assign Driver to Route ===")
    r = _pick_route()
    if not r:
        return
    d = _pick_driver()
    if not d:
        return

    try:
        RouteModel.assign_driver_to_route(r['route_id'], d['driver_id'])
        print(f"Assigned driver #{d['driver_id']} to route #{r['route_id']}.")
    except Exception as e:
        print("Failed to assign driver:", e)


def view_packages_in_route():
    print("=== Packages in Route ===")
    r = _pick_route()
    if not r:
        return

    try:
        packages = RouteModel.get_packages_in_route(r['route_id'])
    except Exception as e:
        print("Failed to load packages:", e)
        return

    if not packages:
        print("No packages assigned to this route.")
        return

    print(f"\n-- Packages in {r['route_name']} ({r['route_date']}) --")
    for p in packages:
        print(f"#{p['package_id']} | {p['sender']} -> {p['recipient_name']} | {p['status']} | Assigned: {p['assigned_at']}")


def list_all_routes():
    print("=== All Routes ===")
    try:
        routes = RouteModel.list_all_routes()
    except Exception as e:
        print("Failed to load routes:", e)
        return

    if not routes:
        print("No routes found.")
        return

    for r in routes:
        print(
            f"#{r['route_id']} | {r['route_name']} | {r['route_date']} | "
            f"Fuel: {r.get('fuel_estimate') or '-'} | Driver: {r.get('driver_name') or '-'} | Created: {r['created_at']}"
        )