from datetime import datetime
from database_manager import DatabaseManager
import random

class ChallengeRepository:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all_challenges(self, category=None) -> list[dict]:
        if category:
            query = """
                SELECT * FROM challenges WHERE category = :category
            """
            challenges = self.db.execute_query(query, {"category": category})
        else:
            query = """
                SELECT * FROM challenges
            """
            challenges = self.db.execute_query(query)

        return challenges

    def create_challenge(self, challenge_data):
        return self.db.execute_query(
            "INSERT INTO challenges (title, description, category) VALUES (:title, :description, :category)",
            challenge_data
        )

    def get_weekly_challenge(self) -> dict:
        query = """
            SELECT * FROM challenges
        """
        challenges = self.db.execute_query(query)
        
        if not challenges:
            return None
            
        return random.choice(challenges if isinstance(challenges, list) else [challenges])

    def delete_challenge(self, challenge_id):

        query = """
            DELETE FROM challenges WHERE id = :challenge_id
        """
        self.db.execute_query(query, {"challenge_id": challenge_id})

        return True
    
    def get_challenge_by_id(self, challenge_id):
        query = """
            SELECT * FROM challenges WHERE id = :challenge_id
        """
        return self.db.execute_query(query, {"challenge_id": challenge_id})
    