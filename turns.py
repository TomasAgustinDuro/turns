from models import add_turn_db, get_turns_db, get_turn_db, cancel_turn_db, update_turn_db

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