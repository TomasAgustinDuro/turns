import sqlite3
from datetime import datetime

# Conexión a la base de datos
def connect_db():
    return sqlite3.connect('data.db')

# Manejo lógica de creación de tabla de turnos
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

# Manejo lógica de inserción de turnos
def add_turn_db(name, last_name, date, hour, email, phone):
    """
    Parámetros:
    - name (str): Nombre del cliente.
    - last_name (str): Apellido del cliente.
    - date (str): Fecha del turno (formato: AAAA-MM-DD).
    - hour (str): Hora del turno (formato: HH:MM).
    - email (str): Email del cliente.
    - phone (str): Teléfono del cliente.

    Retorna:
    - None
    """
    try:
        with connect_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''INSERT INTO turns(nombre, apellido, fecha, hora, email, telefono) 
                              VALUES(?, ?, ?, ?, ?, ?)''', (name, last_name, date, hour, email, phone))
            conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al agregar turno: {e}")

# Manejo lógica de obtención de turnos
def get_turns_db():
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
        print(f"Error al obtener turnos: {e}")
        return []

# Manejo lógica de cancelación de turno
def cancel_turn_db(id):
    """Cancelar un turno por su ID."""
    try:
        with connect_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM turns WHERE id = ?', (id,))
            conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al cancelar turno: {e}")

# Manejo lógica de actualización de turnos
def update_turn_db(id, name, last_name, date, hour, email, phone):
    try:
        with connect_db() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''UPDATE turns 
                              SET nombre = ?, apellido = ?, fecha = ?, hora = ?, email = ?, telefono = ? 
                              WHERE id = ?''', (name, last_name, date, hour, email, phone, id))
            conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al actualizar turno: {e}")
        
# Manejo lógica de turnos
def initialize_db():
    # Crear la tabla de turnos
    create_table_db()