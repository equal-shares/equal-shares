import os
from typing import Any

from dotenv import load_dotenv
from locust import HttpUser, task
from pydantic import BaseModel

load_dotenv()

LOCUST_ADMIN_KEY = os.getenv("LOCUST_ADMIN_KEY", "")


class FakeEmails:
    def __init__(self) -> None:
        self.email_index = 0

    def generate(self) -> str:
        email = f"test-{self.email_index}@example.com"
        self.email_index += 1
        return email


fake_emails = FakeEmails()


class CreateTokenResponse(BaseModel):
    email: str
    token: str
    verify: bool
    quety: str


class LoadTestUser(HttpUser):
    user_email: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user_email = fake_emails.generate()

    @task
    def full_form(self) -> None:
        self.client.get("/health-check")

        res = self.client.get(f"/admin/create-token?admin_key={LOCUST_ADMIN_KEY}&email={self.user_email}")
        if res.status_code != 200:
            raise Exception(f"Failed to create token, status code: {res.status_code}")

        payload = CreateTokenResponse(**res.json())

        if payload.email != self.user_email:
            raise Exception("Email mismatch")

        quety = payload.quety

        res = self.client.post(f"/form/data{quety}")

        if res.status_code != 200:
            raise Exception("Failed to get form data")

        self.stop()
