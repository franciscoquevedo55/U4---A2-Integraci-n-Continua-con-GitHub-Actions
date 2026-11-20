
from models import db, Juego


def insertar_juego(nombre, descripcion, precio):
    juego = Juego(nombre=nombre, descripcion=descripcion, precio=precio)
    db.session.add(juego)
    db.session.commit()


def obtener_juegos():
    return Juego.query.all()


def obtener_juego_por_id(id):
    return db.session.get(Juego, id)


def actualizar_juego(nombre, descripcion, precio, id):
    juego = db.session.get(Juego, id)

    if juego:
        juego.nombre = nombre
        juego.descripcion = descripcion
        juego.precio = precio
        db.session.commit()


def eliminar_juego(id):
    juego = db.session.get(Juego, id)

    if juego:
        db.session.delete(juego)
        db.session.commit()
