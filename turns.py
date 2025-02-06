import sqlite3
from models import connect_db, add_turn_db, get_turns_db, cancel_turn_db, update_turn_db
from datetime import datetime, timedelta
from reminders import reserve_reminder_email


# Manejo de lógica de los turnos

# Manejo de lógica de reserva de turnos
def reserve_turn(data):
    """
    Parámetros:
    - data (dict): Diccionario con los datos del turno (name, last_name, date, hour, email, phone).
    """
    
    try:
        add_turn_db(data['name'], data['last_name'], data['date'], data['hour'], data['email'], data['phone'])
        print(f"Turno reservado para {data['name']} {data['last_name']}.")
        reserve_reminder_email(data['email'], "✔️ Reserva de turno", f"Hola {data['name']} {data['last_name']}, tu turno ha sido reservado para el día {data['date']} a las {data['hour']}.")
    except Exception as e:
        print(f"Error al reservar turno: {e}")
        
# Manejo de lógica de obtención de turnos
def show_turns():
    """
    Obtiene y muestra todos los turnos.
    
    Retorna:
    - Lista de turnos.
    """
    try:
        turns = get_turns_db()
        return turns
    except Exception as e:
        print(f"Error al obtener turnos: {e}")
        return []

# Manejo de lógica de cancelación de turnos
def delete_turn(id):
    """
    Cancela un turno por su ID.
    
    Parámetros:
    - id (int): ID del turno.
    """
    try:
        cancel_turn_db(id)
        print(f"Turno con ID {id} cancelado.")
    except Exception as e:
        print(f"Error al cancelar turno: {e}")

# Manejo de lógica de actualización de turnos
def modify_turn(data, id):
    """
    Actualiza un turno existente.
    
    Parámetros:
    - data (dict): Diccionario con los nuevos datos del turno (name, last_name, date, hour, email, phone).
    - id (int): ID del turno a actualizar.
    """
    try:
        update_turn_db(id, data['name'], data['last_name'], data['date'], data['hour'], data['email'], data['phone'])
        print(f"Turno con ID {id} actualizado.")
    except Exception as e:
        print(f"Error al actualizar turno: {e}")
        
def get_turns_by_date(date):
    """Obtener turnos en una fecha específica."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, email, hora FROM turns WHERE fecha = ?", (date,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ Error al obtener turnos: {e}")
        return []

def get_tomorrow_turns():
    """Buscar turnos para mañana y enviar recordatorios."""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Ejecutando get_tomorrow_turns a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tomorrow_turns = get_turns_by_date(tomorrow)
    
    for name, email, hour in tomorrow_turns:
        subject = "📅 Recordatorio de turno"
        message = f"Hola {name}, este es un recordatorio de tu turno de mañana a las {hour}. ¡Nos vemos!"
        reserve_reminder_email(email, subject, message)
    
    
