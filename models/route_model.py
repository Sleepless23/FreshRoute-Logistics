# ROLE FOR: JOHN GABRIEL GALANG

from database.connection import get_connection


class RouteModel:
    @staticmethod
    def create_route(route_name: str, route_date: str, fuel_estimate: float | None = None, driver_id: int | None = None) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO routes (route_name, route_date, user_id, fuel_estimate)
                VALUES (%s, %s, %s, %s)
                """,
                (route_name, route_date, driver_id, fuel_estimate),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def assign_driver_to_route(route_id: int, driver_id: int) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE routes SET user_id=%s WHERE route_id=%s", (driver_id, route_id))
            conn.commit()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def list_all_routes() -> list[dict]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT r.route_id, r.route_name, r.route_date, r.fuel_estimate, r.created_at,
                       r.user_id AS driver_id, u.full_name AS driver_name
                FROM routes r
                LEFT JOIN users u ON u.user_id = r.user_id AND u.role = 'driver'
                ORDER BY r.route_date DESC, r.route_id DESC
                """
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_packages_in_route(route_id: int) -> list[dict]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT p.package_id, p.sender, p.recipient_name, p.status, rp.assigned_at
                FROM route_packages rp
                JOIN packages p ON p.package_id = rp.package_id
                WHERE rp.route_id = %s
                ORDER BY p.package_id ASC
                """,
                (route_id,),
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def list_drivers() -> list[dict]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT u.user_id AS driver_id, u.full_name, u.username
                FROM users u
                WHERE u.role = 'driver'
                ORDER BY u.full_name ASC
                """
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()
