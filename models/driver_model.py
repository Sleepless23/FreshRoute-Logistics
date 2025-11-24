# ROLE FOR: NICOLE JOHN GARCIA

driver_model.py
from database.connection import get_connection


class DriverModel:
    @staticmethod
    def create_driver(user_id: int, license_number: str | None, phone: str | None) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO drivers (user_id, license_number, phone) VALUES (%s, %s, %s)",
                (user_id, license_number, phone),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def list_drivers() -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT d.driver_id, u.full_name, u.username, d.license_number, d.phone, d.assigned_today
                FROM drivers d
                JOIN users u ON u.user_id = d.user_id
                ORDER BY d.driver_id DESC
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_driver_assigned_route(driver_id: int) -> dict | None:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT r.route_id, r.route_name, r.route_date, r.fuel_estimate
                FROM routes r
                WHERE r.driver_id = %s
                ORDER BY r.route_date DESC, r.route_id DESC
                LIMIT 1
                """,
                (driver_id,),
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