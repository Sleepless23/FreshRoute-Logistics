# ROLE FOR: RENZ SALTA
from utils.helpers import select_from_list, input_string
from models.report_model import ReportModel
from utils.export_csv import export_to_csv


def _prompt_export(rows: list[dict], default_prefix: str) -> None:
    if not rows:
        print("No data to export.")
        return
    choice = select_from_list(["Export to CSV"], "Skipping export...", "Skip", "== Export Options ==")
    if choice is None:
        return
    try:
        filename = export_to_csv(rows, default_prefix)
        print(f"Report exported to {filename}")
    except Exception as e:
        print("Failed to export report:", e)


def daily_delivered_report():
    print("=== Daily Delivered Report ===")
    date_str = input_string("Enter date (YYYY-MM-DD) or 'exit' to cancel: ", exit_message="Cancelled.")
    if date_str is None:
        return

    try:
        rows = ReportModel.daily_delivered(date_str)
    except Exception as e:
        print("Failed to generate report:", e)
        return

    if not rows:
        print("No delivered packages on this date.")
        return

    print("\n-- Delivered Packages --")
    for r in rows:
        print(
            f"#{r['package_id']} | {r['sender']} -> {r['recipient_name']} | "
            f"Route: {r.get('route_name') or '-'} | Driver: {r.get('driver_name') or '-'} | "
            f"Delivered At: {r['delivered_at']}"
        )

    _prompt_export(rows, f"daily_delivered_{date_str}")


def driver_performance_report():
    print("=== Driver Performance Report ===")
    date_str = input_string("Enter date (YYYY-MM-DD) or 'exit' to cancel: ", exit_message="Cancelled.")
    if date_str is None:
        return

    try:
        rows = ReportModel.driver_performance(date_str)
    except Exception as e:
        print("Failed to generate report:", e)
        return

    if not rows:
        print("No deliveries found for the given date.")
        return

    print("\n-- Driver Performance --")
    for r in rows:
        print(f"{r.get('driver_name') or '-'}: {r['delivered_count']} delivered")

    _prompt_export(rows, f"driver_performance_{date_str}")


def delayed_deliveries_report():
    print("=== Delayed Deliveries Report ===")
    while True:
        days_str = input_string("Enter threshold days (e.g., 2) or 'exit' to cancel: ", exit_message="Cancelled.")
        if days_str is None:
            return
        try:
            threshold_days = int(days_str)
            if threshold_days < 0:
                print("Please enter a non-negative number.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    try:
        rows = ReportModel.delayed_deliveries(threshold_days)
    except Exception as e:
        print("Failed to generate report:", e)
        return

    if not rows:
        print("No delayed deliveries beyond the threshold.")
        return

    print("\n-- Delayed Deliveries --")
    for r in rows:
        print(
            f"#{r['package_id']} | {r['sender']} -> {r['recipient_name']} | "
            f"Created: {r['created_at']} | Age (days): {r['age_days']}"
        )

    _prompt_export(rows, f"delayed_deliveries_{threshold_days}d")


def export_report_csv():
    print("=== Export Reports ===")
    # This function provides a quick path to export any of the three reports directly
    choice = select_from_list(
        [
            "Daily Delivered Report",
            "Driver Performance Report",
            "Delayed Deliveries Report",
        ],
        "Returning...",
        "Back",
        "== Choose Report to Export ==",
    )

    if choice is None:
        return

    if choice == 1:
        daily_delivered_report()
    elif choice == 2:
        driver_performance_report()
    elif choice == 3:
        delayed_deliveries_report()
