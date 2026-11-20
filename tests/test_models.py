import unittest
from flask import Flask
from models import db, Juego, User


class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/juegos_test"

        db.init_app(self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_crear_juego(self):
        juego = Juego(
            nombre="Minecraft",
            descripcion="Juego de construccion",
            precio=599
        )
        db.session.add(juego)
        db.session.commit()

        self.assertIsNotNone(juego.id)
        self.assertEqual(juego.nombre, "Minecraft")

    def test_crear_usuario(self):
        usuario = User(username="admin")
        usuario.password = "123456"

        db.session.add(usuario)
        db.session.commit()

        self.assertIsNotNone(usuario.id)
        self.assertTrue(usuario.verify_password("123456"))


if __name__ == "__main__":
    unittest.main()
