# ROLE FOR: RENZ SALTA

from utils.helpers import select_from_list
from services.report_service import (
    daily_delivered_report,
    driver_performance_report,
    delayed_deliveries_report,
    export_report_csv,
)

def reports_menu():
    while True:
        choice = select_from_list(
            [
                "Daily Report",
                "Driver Performance Report",
                "Route Efficiency Report",
                "Export Report to CSV",
            ],
            "Reverting to main menu...",
            "Back to Main Menu",
            "====== REPORTS ======",
        )

        if choice == 1:
            daily_delivered_report()
        elif choice == 2:
            driver_performance_report()
        elif choice == 3:
            delayed_deliveries_report()
        elif choice == 4:
            export_report_csv()
        elif choice is None:
            break
