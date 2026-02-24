import sqlite3
import os
from typing import List, Dict, Any
from src.exceptions import DatabaseError

class DatabaseManager:
    """
    Handles SQLite database connections, table creation, and CRUD operations.
    Ensures data persistence without needing an external database server.
    """
    def __init__(self, db_path: str = "database/reviews.db"):
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._initialize_database()

    def _get_connection(self):
        """Creates and returns a connection to the SQLite database."""
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            raise DatabaseError(f"Failed to connect to database at {self.db_path}: {e}")

    def _initialize_database(self):
        """Creates the necessary tables if they don't already exist."""
        query = """
        CREATE TABLE IF NOT EXISTS product_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            raw_comment TEXT NOT NULL,
            is_satisfied BOOLEAN NOT NULL,
            reason TEXT,
            estimated_score INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to initialize database tables: {e}")

    def insert_review(self, product_id: int, raw_comment: str, ai_data: Dict[str, Any]):
        """Inserts a single AI-analyzed review into the database."""
        query = """
        INSERT INTO product_reviews (product_id, raw_comment, is_satisfied, reason, estimated_score)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    product_id, 
                    raw_comment, 
                    ai_data.get("is_satisfied", False), 
                    ai_data.get("reason", "نامشخص"), 
                    ai_data.get("estimated_score", 5)
                ))
                conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to insert review into database: {e}")

    def get_product_reviews(self, product_id: int) -> List[Dict[str, Any]]:
        """Retrieves all stored reviews for a specific product."""
        query = "SELECT is_satisfied, reason, estimated_score FROM product_reviews WHERE product_id = ?"
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row  # Returns rows as dictionaries
                cursor = conn.cursor()
                cursor.execute(query, (product_id,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch reviews for product {product_id}: {e}")