import hashlib
from app.domain.exceptions.user_not_found_error import UserNotFound
from app.domain.exceptions.user_registration_error import UserRegistrationError
from app.domain.models.person import Person
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository


class UserRepositoryDB(UserRepository):
    def __init__(self, session):
        self.session = session
        self.table = "FeedbackTable"

    def save(self, user: User) -> User:
        try:
            self.session.put_item(
                TableName=self.table,
                Item={
                    "user_email": {"S": user.user.email},
                    "USER": {
                        "M": {
                            "email": {"S": user.user.email},
                            "password": {"S": user.hashed_password},
                            "name": {"S": user.user.name},
                        }
                    },
                    "FEEDBACK": {"M": {"peers": {"L": []}, "action_items": {"L": []}}},
                },
            )
            return user
        except Exception:
            raise UserRegistrationError(
                f"Error inserting this user {user.user.email} into the DB"
            )

    def hash_password(self, new_pasword: str) -> str:
        hash_obj = hashlib.sha256()
        hash_obj.update(new_pasword.encode("utf-8"))
        hashed_password = hash_obj.hexdigest()

        return hashed_password

    def get_by_email(self, email: str) -> User:
        try:
            item = self.session.get_item(
                TableName=self.table, Key={"user_email": {"S": email}}
            )

            if "Item" not in item:
                return None

            user_saved = item.get("Item").get("USER").get("M")
            email_saved = user_saved.get("email")["S"]
            person = Person(email=email_saved, name=user_saved.get("name")["S"])
            user = User(user=person, hashed_password=user_saved.get("password")["S"])
            if email_saved:
                return user
        except Exception:
            raise UserNotFound(f"Not user found with this email {email}")

    def verify_password(self, hashed_password: str, email: str) -> bool:
        try:
            item = self.session.get_item(
                TableName=self.table, Key={"user_email": {"S": email}}
            )

            if "Item" not in item:
                return None

            user_saved = item.get("Item", None).get("USER").get("M")
            hashed_password_saved = user_saved.get("password")["S"]
            if hashed_password == hashed_password_saved:
                return True
            return False
        except Exception:
            raise UserNotFound(f"Not user found with this email {email}")
