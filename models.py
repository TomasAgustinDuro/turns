import sqlite3
import re
from datetime import datetime

# Conexión a la base de datos
def connect_db():
    return sqlite3.connect('data.db')

# Validaciones
def is_valid_email(email):
    """Verifica que el email tenga un formato válido."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def is_valid_phone(phone):
    """Verifica que el teléfono contenga solo números y tenga una longitud adecuada."""
    return phone.isdigit() and (7 <= len(phone) <= 15)

def is_valid_date(date):
    """Verifica que la fecha tenga el formato correcto (YYYY-MM-DD) y sea una fecha válida."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_hour(hour):
    """Verifica que la hora tenga el formato correcto (HH:MM)."""
    try:
        datetime.strptime(hour, "%H:%M")
        return True
    except ValueError:
        return False

def turno_existe(date, hour):
    """Verifica si ya existe un turno en la misma fecha y hora."""
    with connect_db() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM turns WHERE fecha = ? AND hora = ?", (date, hour))
        return cursor.fetchone() is not None

# Creación de la tabla si no existe
def create_table_db():
    try:
        with connect_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS turns(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefono TEXT NOT NULL
                )
            ''')
            conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")

# Inserción de turnos con validaciones
def add_turn_db(name, last_name, date, hour, email, phone):
    """Inserta un nuevo turno en la base de datos con validaciones previas."""
    if not (name and last_name and date and hour and email and phone):
        print("❌ Error: Todos los campos son obligatorios.")
        return False

    if not is_valid_email(email):
        print("❌ Error: Email inválido.")
        return False

    if not is_valid_phone(phone):
        print("❌ Error: Teléfono inválido.")
        return False

    if not is_valid_date(date):
        print("❌ Error: Formato de fecha incorrecto. Usa YYYY-MM-DD.")
        return False

    if not is_valid_hour(hour):
        print("❌ Error: Formato de hora incorrecto. Usa HH:MM.")
        return False

    if turno_existe(date, hour):
        print("❌ Error: Ya existe un turno en esa fecha y hora.")
        return False

    try:
        with connect_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''INSERT INTO turns(nombre, apellido, fecha, hora, email, telefono) 
                              VALUES(?, ?, ?, ?, ?, ?)''', (name, last_name, date, hour, email, phone))
            conexion.commit()
            print("✅ Turno agregado correctamente.")
            return True
    except sqlite3.Error as e:
        print(f"❌ Error al agregar turno: {e}")
        return False

# Obtención de turnos
def get_turns_db():
    """Devuelve una lista de turnos en formato diccionario."""
    try:
        with connect_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM turns')
            turns = cursor.fetchall()
        return [
            {
                "id": turn[0],
                "name": turn[1],
                "last_name": turn[2],
                "date": turn[3],
                "hour": turn[4],
                "email": turn[5],
                "phone": turn[6]
            }
            for turn in turns
        ]
    except sqlite3.Error as e:
        print(f"❌ Error al obtener turnos: {e}")
        return []

# Cancelación de turnos con validación
def cancel_turn_db(id):
    """Cancela un turno si existe."""
    if not id:
        print("❌ Error: ID de turno no proporcionado.")
        return False

    with connect_db() as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT id FROM turns WHERE id = ?', (id,))
        turno = cursor.fetchone()

        if turno is None:
            print("❌ Error: No se encontró un turno con ese ID.")
            return False

        try:
            cursor.execute('DELETE FROM turns WHERE id = ?', (id,))
            conexion.commit()
            print(f"✅ Turno con ID {id} cancelado correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error al cancelar turno: {e}")
            return False

# Actualización de turnos con validaciones
def update_turn_db(id, name, last_name, date, hour, email, phone):
    """Actualiza un turno si cumple con las validaciones."""
    if not (id and name and last_name and date and hour and email and phone):
        print("❌ Error: Todos los campos son obligatorios.")
        return False

    if not is_valid_email(email):
        print("❌ Error: Email inválido.")
        return False

    if not is_valid_phone(phone):
        print("❌ Error: Teléfono inválido.")
        return False

    if not is_valid_date(date):
        print("❌ Error: Formato de fecha incorrecto.")
        return False

    if not is_valid_hour(hour):
        print("❌ Error: Formato de hora incorrecto.")
        return False

    with connect_db() as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT id FROM turns WHERE id = ?', (id,))
        turno = cursor.fetchone()

        if turno is None:
            print("❌ Error: No se encontró un turno con ese ID.")
            return False

        try:
            cursor.execute('''UPDATE turns 
                              SET nombre = ?, apellido = ?, fecha = ?, hora = ?, email = ?, telefono = ? 
                              WHERE id = ?''', (name, last_name, date, hour, email, phone, id))
            conexion.commit()
            print("✅ Turno actualizado correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error al actualizar turno: {e}")
            return False

# Inicialización de la base de datos
def initialize_db():
    """Inicializa la base de datos creando la tabla de turnos si no existe."""
    create_table_db()
