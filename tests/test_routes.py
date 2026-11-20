import unittest
from app import app


class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_login(self):
        respuesta = self.client.get("/auth/login")
        self.assertEqual(respuesta.status_code, 200)

    def test_juegos_sin_login(self):
        respuesta = self.client.get("/juegos")
        self.assertEqual(respuesta.status_code, 302)

    def test_logout_sin_login(self):
        respuesta = self.client.get("/auth/logout")
        self.assertEqual(respuesta.status_code, 302)


if __name__ == "__main__":
    unittest.main()
