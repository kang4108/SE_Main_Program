import requests
import unittest


class AuthServiceTest(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"

    def setUp(self):
        requests.post(
            f"{self.BASE_URL}/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password",
            },
        )
        login_response = requests.post(
            f"{self.BASE_URL}/login",
            json={"username": "testuser", "password": "password"},
        )
        self.token = login_response.json().get("access_token")

    def tearDown(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        requests.delete(f"{self.BASE_URL}/update", headers=headers)

    def test_user_registration(self):
        response = requests.post(
            f"{self.BASE_URL}/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "password",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created successfully", response.json().get("message", ""))

        # delete newuser
        login_response = requests.post(
            f"{self.BASE_URL}/login",
            json={"username": "newuser", "password": "password"},
        )
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        requests.delete(f"{self.BASE_URL}/update", headers=headers)

    def test_user_login(self):
        response = requests.post(
            f"{self.BASE_URL}/login",
            json={"username": "testuser", "password": "password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_user_update(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.put(
            f"{self.BASE_URL}/update",
            headers=headers,
            json={
                "username": "updateduser",
                "email": "updated@example.com",
                "password": "newpassword",
                "current_password": "password",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "User information updated successfully", response.json().get("message", "")
        )

        profile_response = requests.get(f"{self.BASE_URL}/profile", headers=headers)
        self.assertEqual(profile_response.status_code, 200)
        profile_data = profile_response.json()
        self.assertEqual(profile_data["username"], "updateduser")
        self.assertEqual(profile_data["email"], "updated@example.com")

    def test_user_delete(self):
        requests.post(
            f"{self.BASE_URL}/register",
            json={
                "username": "deleteuser",
                "email": "delete@example.com",
                "password": "password",
            },
        )

        login_response = requests.post(
            f"{self.BASE_URL}/login",
            json={"username": "deleteuser", "password": "password"},
        )
        token = login_response.json().get("access_token")

        headers = {"Authorization": f"Bearer {token}"}
        delete_response = requests.delete(f"{self.BASE_URL}/update", headers=headers)
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn(
            "User account deleted successfully",
            delete_response.json().get("message", ""),
        )


if __name__ == "__main__":
    unittest.main()