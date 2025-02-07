import sqlite3
from models import connect_db, add_turn_db, get_turns_db, cancel_turn_db, update_turn_db
from datetime import datetime, timedelta
from reminders import reserve_reminder_email
import re


# 🔹 Función para validar los datos del turno antes de agregarlos a la BD
def validate_turn_data(data):
    errors = {}

    name_pattern = r'^[A-Za-záéíóúÁÉÍÓÚñÑ]+(?: [A-Za-záéíóúÁÉÍÓÚñÑ]+)*$'
    if not data.get("name") or len(data["name"]) < 2 or not re.match(name_pattern, data["name"]):
        errors["name"] = "El nombre debe tener al menos 2 caracteres y solo puede contener letras."
    
    if not data.get("last_name") or len(data["last_name"]) < 2 or not re.match(name_pattern, data["last_name"]):
        errors["last_name"] = "El apellido debe tener al menos 2 caracteres y solo puede contener letras."

    # Validación de fecha
    try:
        turn_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        if turn_date < datetime.today().date():
            errors["date"] = "La fecha no puede ser anterior a hoy."
        elif turn_date == datetime.today().date():
            errors["date"] = "La fecha debe ser al menos un día posterior al día de hoy."
    except ValueError:
        errors["date"] = "Formato de fecha inválido (debe ser YYYY-MM-DD)."
    # Validación de hora
    try:
        datetime.strptime(data["hour"], "%H:%M")
    except ValueError:
        errors["hour"] = "Formato de hora inválido (debe ser HH:MM)."

    # Validación de email
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if "email" in data and not re.match(email_pattern, data["email"]):
        errors["email"] = "Correo electrónico no válido."

    # Validación de teléfono (10 a 15 dígitos)
    if "phone" in data and (not data["phone"].isdigit() or not (10 <= len(data["phone"]) <= 15)):
        errors["phone"] = "El número de teléfono debe tener entre 10 y 15 dígitos."

    if errors:
        raise ValueError(errors)  # Lanzar errores para ser manejados en las funciones de reserva o modificación

    return data


# 🔹 Manejo de lógica de reserva de turnos
def reserve_turn(data):
    """
    Reserva un turno después de validar los datos.

    Parámetros:
    - data (dict): Diccionario con los datos del turno (name, last_name, date, hour, email, phone).
    """
    try:
        validate_turn_data(data)  # Validar datos antes de guardarlos en la BD
        add_turn_db(data['name'], data['last_name'], data['date'], data['hour'], data['email'], data['phone'])
        print(f"Turno reservado para {data['name']} {data['last_name']}.")
        
        # Enviar correo de confirmación
        reserve_reminder_email(
            data['email'], 
            "✔️ Reserva de turno", 
            f"Hola {data['name']} {data['last_name']}, tu turno ha sido reservado para el día {data['date']} a las {data['hour']}."
        )
        return {"success": True}  # Devuelve un diccionario con éxito
    except ValueError as e:
        return {"success": False, "errors": e.args[0]}  # Devuelve errores en un diccionario
    except Exception as e:
        return {"success": False, "errors": {"general": str(e)}}  # Maneja errores inesperados


# 🔹 Manejo de lógica de actualización de turnos
def modify_turn(data, id):
    """
    Actualiza un turno existente después de validar los datos.

    Parámetros:
    - data (dict): Diccionario con los nuevos datos del turno (name, last_name, date, hour, email, phone).
    - id (int): ID del turno a actualizar.
    """
    try:
        validate_turn_data(data)  # Validar antes de actualizar
        update_turn_db(id, data['name'], data['last_name'], data['date'], data['hour'], data['email'], data['phone'])
         # Enviar correo de confirmación
        reserve_reminder_email(
            data['email'], 
            "✔️ Reserva de turno", 
            f"Hola {data['name']} {data['last_name']}, tu turno ha sido actualizado para el día {data['date']} a las {data['hour']}."
        )
        print(f"✅ Turno con ID {id} actualizado correctamente.")
        return {"success": True}  # Devuelve un diccionario con éxito
    except ValueError as e:
        return {"success": False, "errors": e.args[0]}  # Devuelve errores en un diccionario
    except Exception as e:
        return {"success": False, "errors": {"general": str(e)}}  # Maneja errores inesperados


# 🔹 Manejo de lógica de obtención de turnos
def show_turns():
    """Obtiene y muestra todos los turnos."""
    try:
        return get_turns_db()
    except ValueError as e:
        return {"success": False, "errors": e.args[0]}  # Devuelve errores en un diccionario
    except Exception as e:
        return {"success": False, "errors": {"general": str(e)}}  # Maneja errores inesperados


# 🔹 Manejo de lógica de cancelación de turnos
def delete_turn(id, name, email, last_name):
    """Cancela un turno por su ID."""
    try:
        cancel_turn_db(id)
        print(f"✅ Turno con ID {id} cancelado correctamente.")
        reserve_reminder_email(
            email,
            "✔️ Reserva de turno", 
            f"Hola {name} {last_name}, tu turno ha sido cancelado."  # 
        )
        return {"success": True}  # Devuelve un diccionario con éxito
    except ValueError as e:
        return {"success": False, "errors": e.args[0]}  # Devuelve errores en un diccionario
    except Exception as e:
        return {"success": False, "errors": {"general": str(e)}}  # Maneja errores inesperados


# 🔹 Obtener turnos en una fecha específica
def get_turns_by_date(date):
    """Obtiene turnos en una fecha específica."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, email, hora FROM turns WHERE fecha = ?", (date,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ Error al obtener turnos: {e}")
        return []


# 🔹 Buscar turnos para mañana y enviar recordatorios
def get_tomorrow_turns():
    """Busca turnos para mañana y envía recordatorios."""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"🔔 Ejecutando get_tomorrow_turns a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    tomorrow_turns = get_turns_by_date(tomorrow)

    for name, email, hour in tomorrow_turns:
        subject = "📅 Recordatorio de turno"
        message = f"Hola {name}, este es un recordatorio de tu turno de mañana a las {hour}. ¡Nos vemos!"
        reserve_reminder_email(email, subject, message)
