# ROLE FOR: NICOLE JOHN GARCIA
from database.connection import get_connection


class DriverModel:
    @staticmethod
    def list_drivers() -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT user_id, full_name, username
                FROM users
                WHERE role = 'driver'
                ORDER BY user_id DESC
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_user_assigned_route(user_id: int) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT r.route_id, r.route_name, r.route_date, r.fuel_estimate
                FROM routes r
                WHERE r.user_id = %s
                ORDER BY r.route_date DESC, r.route_id DESC
                LIMIT 1
                """,
                (user_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_user_by_username(username: str) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id, full_name, username, role FROM users WHERE username=%s",
                (username,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
