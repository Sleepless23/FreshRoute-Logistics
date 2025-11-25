# ROLE FOR: ANGEL JARED DELA CRUZ
from database.connection import get_connection

class DeliveryModel:
    """Data access for delivery-related operations using packages and delivery_updates tables."""

    @staticmethod
    def update_package_status(package_id: int, status: str, note: str | None = None) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE packages SET status=%s WHERE package_id=%s",
                (status, package_id),
            )
            cursor.execute(
                "INSERT INTO delivery_updates (package_id, status, note) VALUES (%s, %s, %s)",
                (package_id, status, note),
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_note(package_id: int, note: str) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO delivery_updates (package_id, status, note) VALUES (%s, (SELECT status FROM packages WHERE package_id=%s), %s)",
                (package_id, package_id, note),
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_delivery_history(package_id: int) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT du.update_id, du.status, du.note, du.timestamp
                FROM delivery_updates du
                WHERE du.package_id = %s
                ORDER BY du.timestamp ASC
                """,
                (package_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def list_packages_by_status(status: str | None = None) -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            if status:
                cursor.execute(
                    "SELECT package_id, sender, recipient_name, status FROM packages WHERE status=%s ORDER BY package_id DESC",
                    (status,),
                )
            else:
                cursor.execute(
                    "SELECT package_id, sender, recipient_name, status FROM packages ORDER BY package_id DESC"
                )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def list_packages_by_status_for_user(status: str | None, user_id: int, user_role: str) -> list[dict]:
        if user_role in ["admin", "dispatcher"]:
            return DeliveryModel.list_packages_by_status(status)
        elif user_role == "driver":
            conn = get_connection()
            try:
                cursor = conn.cursor(dictionary=True)
                if status:
                    cursor.execute(
                        """
                        SELECT p.package_id, p.sender, p.recipient_name, p.status
                        FROM packages p
                        JOIN routes r ON p.current_route_id = r.route_id
                        WHERE r.user_id = %s AND p.status = %s
                        ORDER BY p.package_id DESC
                        """,
                        (user_id, status),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT p.package_id, p.sender, p.recipient_name, p.status
                        FROM packages p
                        JOIN routes r ON p.current_route_id = r.route_id
                        WHERE r.user_id = %s
                        ORDER BY p.package_id DESC
                        """,
                        (user_id,),
                    )
                return cursor.fetchall()
            finally:
                cursor.close()
                conn.close()
        else:
            return []
