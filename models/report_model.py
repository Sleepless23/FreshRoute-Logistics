# ROLE FOR: RENZ SALTA
from database.connection import get_connection


class ReportModel:
    @staticmethod
    def daily_delivered(date_str: str) -> list[dict]:
        """Packages marked Delivered on the given date (DATE(delivery_updates.timestamp) = date_str)."""
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    p.package_id,
                    p.sender,
                    p.recipient_name,
                    p.recipient_address,
                    p.phone,
                    r.route_id,
                    r.route_name,
                    r.route_date,
                    u.full_name AS driver_name,
                    du.timestamp AS delivered_at
                FROM delivery_updates du
                JOIN packages p ON p.package_id = du.package_id
                LEFT JOIN routes r ON r.route_id = p.current_route_id
                LEFT JOIN drivers d ON d.driver_id = r.driver_id
                LEFT JOIN users u ON u.user_id = d.user_id
                WHERE du.status = 'Delivered' AND DATE(du.timestamp) = %s
                ORDER BY du.timestamp ASC
                """,
                (date_str,),
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def driver_performance(date_str: str) -> list[dict]:
        """Count of delivered packages per driver for the given date."""
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    u.full_name AS driver_name,
                    COALESCE(COUNT(DISTINCT p.package_id), 0) AS delivered_count
                FROM delivery_updates du
                JOIN packages p ON p.package_id = du.package_id
                LEFT JOIN routes r ON r.route_id = p.current_route_id
                LEFT JOIN drivers d ON d.driver_id = r.driver_id
                LEFT JOIN users u ON u.user_id = d.user_id
                WHERE du.status = 'Delivered' AND DATE(du.timestamp) = %s
                GROUP BY u.full_name
                ORDER BY delivered_count DESC, driver_name ASC
                """,
                (date_str,),
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delayed_deliveries(threshold_days: int) -> list[dict]:
        """Packages still Pending older than threshold_days."""
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    p.package_id,
                    p.sender,
                    p.recipient_name,
                    p.recipient_address,
                    p.phone,
                    p.created_at,
                    TIMESTAMPDIFF(DAY, p.created_at, NOW()) AS age_days
                FROM packages p
                WHERE p.status = 'Pending' AND p.created_at < (NOW() - INTERVAL %s DAY)
                ORDER BY p.created_at ASC
                """,
                (threshold_days,),
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()
