import unittest
import jwt
from datetime import datetime, timedelta, timezone

from app.config.enviroment import Settings
from app.infraestructure.api.config.auth import Auth


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.auth = Auth()
        self.data = {"sub": "user1"}
        self.secret_key = Settings.SECRET_KEY
        self.algorithm = Settings.ALGORITHM

    def test_create_access_token_with_default_expiration(self):
        token = self.auth.create_access_token(self.data)
        decoded_data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

        self.assertIn("expire", decoded_data)
        expire_time = datetime.fromisoformat(decoded_data["expire"])
        expected_expire_time = datetime.now(timezone.utc) + timedelta(minutes=15)
        self.assertAlmostEqual(
            expire_time, expected_expire_time, delta=timedelta(seconds=5)
        )

    def test_create_access_token_with_custom_expiration(self):
        expires_delta = timedelta(hours=1)
        token = self.auth.create_access_token(self.data, expires_delta=expires_delta)
        decoded_data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

        self.assertIn("expire", decoded_data)
        expire_time = datetime.fromisoformat(decoded_data["expire"])
        expected_expire_time = datetime.now(timezone.utc) + expires_delta
        self.assertAlmostEqual(
            expire_time, expected_expire_time, delta=timedelta(seconds=5)
        )

    def test_create_access_token_contains_data(self):
        token = self.auth.create_access_token(self.data)
        decoded_data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

        for key, value in self.data.items():
            self.assertEqual(decoded_data[key], value)
