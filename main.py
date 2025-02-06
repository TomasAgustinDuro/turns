import sys
from turns import get_tomorrow_turns, reserve_turn, show_turns, delete_turn, modify_turn
from models import initialize_db
from reminders import reserve_reminder_email
import threading
import schedule, time

def start_scheduler():
    """Iniciar el planificador de tareas."""
    schedule.every().day.at("09:00").do(get_tomorrow_turns)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Crear y arrancar el hilo del scheduler
scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.daemon = True  # Esto asegura que el hilo se cierre cuando el programa termine
scheduler_thread.start()

# Manejo de menú
def menu():
    initialize_db()
    
    """
    Menú principal del programa.
    
    Objetivo:
    Se encarga de la interacción con el usuario
    
    Parámetros:
    - Ninguno
    """
    
    while True:
        print("\n--- Sacador de Turnos ---")
        print("1. Reservar turno")
        print("2. Mostrar turnos")
        print("3. Modificar turno")
        print("4. Cancelar turno")
        print("5. Salir")
        option = input("Opción: ")

        # Lógica para cada opción del menú
        
        # Opción 1: Reservar turno
        if option == "1":
            name = input("Nombre: ")
            last_name = input("Apellido: ")
            date = input("Fecha (YYYY-MM-DD): ")
            hour = input("Hora (HH:MM): ")
            email = input("Email: ")
            phone = input("Teléfono: ")
            data = {'name': name, 'last_name': last_name, 'date': date, 'hour': hour, 'email': email, 'phone': phone}
            reserve_turn(data)
            
           

        # Opción 2: Mostrar turnos
        elif option == "2":
            turns = show_turns()
            if not turns:
                print("No hay turnos disponibles.")
            else:
                for turn in turns:
                    print(f"{turn['name']} {turn['last_name']} - {turn['date']} {turn['hour']} - {turn['email']} - {turn['phone']}")

        elif option == "3":
            date_turn = input("Fecha del turno que deseas modificar (YYYY-MM-DD): ")
            turns = show_turns()

            filtered_turns = [turn for turn in turns if turn['date'] == date_turn]

            if not filtered_turns:
                print("No hay turnos para esa fecha.")
            else:
                print("\nTurnos disponibles:")
                for idx, turn in enumerate(filtered_turns, start=1):
                    print(f"{idx}. {turn['name']} {turn['last_name']} - {turn['hour']} - {turn['email']} - {turn['phone']}")

                try:
                    selected_index = int(input("\nSelecciona el número del turno a modificar: ")) - 1
                    if 0 <= selected_index < len(filtered_turns):
                        turn_to_modify = filtered_turns[selected_index]
                        print(f"Seleccionaste el turno de {turn_to_modify['name']} {turn_to_modify['last_name']} a las {turn_to_modify['hour']}")

                        # Permitir que el usuario deje valores en blanco para mantener los originales
                        name = input(f"Nombre ({turn_to_modify['name']}): ") or turn_to_modify['name']
                        last_name = input(f"Apellido ({turn_to_modify['last_name']}): ") or turn_to_modify['last_name']
                        date = input(f"Fecha ({turn_to_modify['date']} - YYYY-MM-DD): ") or turn_to_modify['date']
                        hour = input(f"Hora ({turn_to_modify['hour']} - HH:MM): ") or turn_to_modify['hour']
                        email = input(f"Email ({turn_to_modify['email']}): ") or turn_to_modify['email']
                        phone = input(f"Teléfono ({turn_to_modify['phone']}): ") or turn_to_modify['phone']

                        # Crear diccionario con los datos actualizados
                        data = {
                            'name': name,
                            'last_name': last_name,
                            'date': date,
                            'hour': hour,
                            'email': email,
                            'phone': phone
                        }

                        # Llamar a la función para modificar el turno
                        modify_turn(data, turn_to_modify['id'])
                    else:
                        print("Selección inválida.")
                except ValueError:
                    print("Por favor, ingresa un número válido.")

        elif option == "4":
            date_turn = input("Fecha del turno que deseas eliminar (YYYY-MM-DD): ")
            
            turns = show_turns()
            
            filtered_turns = [turn for turn in turns if turn['date'] == date_turn]
            
            if not filtered_turns:
                print("No hay turnos para esa fecha.")
            else:
                print("\nTurnos disponibles:")
                for idx, turn in enumerate(filtered_turns, start=1):
                    print(f"{idx}. {turn['name']} {turn['last_name']} - {turn['hour']} - {turn['email']} - {turn['phone']}")

                try:
                    selected_index = int(input("\nSelecciona el número del turno a eliminar: ")) - 1
                    if 0 <= selected_index < len(filtered_turns):
                        delete_turn(filtered_turns[selected_index]['id'])
                        print("Turno eliminado correctamente.")
                    else:
                        print("Selección inválida.")
                except ValueError:
                    print("Por favor, ingresa un número válido.")

        elif option == "5":
            print("Saliendo del programa...")
            sys.exit(0)  # Sale del programa correctamente

        else:
            print("Opción no válida, intenta nuevamente.")

# Ejecutar el menú
menu()
