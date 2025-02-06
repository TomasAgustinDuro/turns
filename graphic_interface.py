import tkinter as tk
from tkinter import messagebox
from turns import (
    show_turns,
    reserve_turn,
    reserve_reminder_email,
    modify_turn as modify_turn_bd,
    cancel_turn_db,
)


def create_entry(frame, label_text, default_value=""):
    label = tk.Label(frame, text=label_text, bg="black", fg="white")
    label.pack(pady=5)
    entry = tk.Entry(frame)
    entry.pack(pady=5)
    return entry


def open_reserve_turn():
    reserve_turn_window = tk.Toplevel(app)
    reserve_turn_window.geometry("720x480")
    reserve_turn_window.configure(bg="black")
    reserve_turn_window.title("Reservar turno")
    label = tk.Label(reserve_turn_window, text="Reservar turno", bg="black", fg="white")
    label.pack()

    # Crear un frame para organizar el texto y el Entry
    frame = tk.Frame(reserve_turn_window)
    frame.pack(pady=20)

    # Crear varios Entry con sus labels
    entry1 = create_entry(frame, "Nombre:")
    entry2 = create_entry(frame, "Apellido:")
    entry3 = create_entry(frame, "Fecha - YYYY-MM-DD:")
    entry4 = create_entry(frame, "Hora - HH:MM:")
    entry5 = create_entry(frame, "Email:")
    entry6 = create_entry(frame, "Teléfono:")

    tk.Button(
        reserve_turn_window,
        text="Reservar",
        bg="blue",
        fg="white",
        command=lambda: reserve_turn(
            {
                "name": entry1.get(),
                "last_name": entry2.get(),
                "date": entry3.get(),
                "hour": entry4.get(),
                "email": entry5.get(),
                "phone": entry6.get(),
            }
        ),
    ).pack(pady=10)


def show_turn():
    show_turn_window = tk.Toplevel(app)
    show_turn_window.configure(bg="black")
    show_turn_window.geometry("720x480")
    show_turn_window.title("Reservar turno")
    label = tk.Label(show_turn_window, text="Todos los turnos", bg="black", fg="white")
    label.pack()

    turns = show_turns()

    for turn in turns:
        turn_label = tk.Label(
            show_turn_window,
            text=f"{turn['name']} {turn['last_name']} - {turn['date']} {turn['hour']} - {turn['email']} - {turn['phone']}",
            bg="black",
            fg="white",
        )
        turn_label.pack()

def modify_turn():
    modify_turn_window = tk.Toplevel(app)
    modify_turn_window.configure(bg="black")
    modify_turn_window.geometry("720x480")
    modify_turn_window.title("Modificar turno")

    label = tk.Label(modify_turn_window, text="Modificar turno", bg="black", fg="white")
    label.pack()

    # Crear un frame para organizar el texto y el Entry
    frame = tk.Frame(modify_turn_window)
    frame.pack(pady=20)

    date_entry = create_entry(
        frame, "Fecha del turno que deseas modificar (YYYY-MM-DD):"
    )

    # Función para actualizar los turnos
    def update_turns():
        # Obtener la fecha desde el Entry
        date_turn = date_entry.get()
        turns = show_turns()
        filtered_turns = [turn for turn in turns if turn["date"] == date_turn]

        # Limpiar la ventana de turnos anteriores
        for widget in modify_turn_window.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        # Mostrar los turnos filtrados o un mensaje si no hay turnos para esa fecha
        if not filtered_turns:
            label = tk.Label(
                modify_turn_window,
                text="No hay turnos para esa fecha.",
                bg="black",
                fg="white",
            )
            label.pack()
        else:
            label = tk.Label(
                modify_turn_window, text="Turnos disponibles:", bg="black", fg="white"
            )
            label.pack()

            for turn in filtered_turns:
                # Usar lambda para pasar el turno específico a la función modify_specific_turn
                button = tk.Button(
                    modify_turn_window,
                    text=f"{turn['name']} {turn['last_name']} - {turn['hour']}",
                    command=lambda t=turn: modify_specific_turn(t),
                )
                button.pack(pady=10)

    for widget in modify_turn_window.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()
    
    # Botón para actualizar la lista de turnos
    update_button = tk.Button(
        modify_turn_window,
        text="Actualizar Turnos",
        bg="blue",
        fg="white",
        command=update_turns,
    )
    update_button.pack(pady=10)


def modify_specific_turn(turn):
    modify_specific_turn_window = tk.Toplevel(app)
    modify_specific_turn_window.configure(bg="black")
    modify_specific_turn_window.geometry("720x480")
    modify_specific_turn_window.title("Modificar turno específico")

    label = tk.Label(
        modify_specific_turn_window,
        text="Modifique solamente los campos que necesite",
        bg="black",
        fg="white",
    )
    label.pack()

    # Crear un frame para organizar el texto y los Entry
    frame = tk.Frame(modify_specific_turn_window)
    frame.pack(pady=20)

    # Crear entradas pre-rellenadas con los valores actuales del turno
    name_entry = create_entry(frame, "Nombre:", default_value=turn["name"])
    last_name_entry = create_entry(frame, "Apellido:", default_value=turn["last_name"])
    date_entry = create_entry(frame, "Fecha (YYYY-MM-DD):", default_value=turn["date"])
    hour_entry = create_entry(frame, "Hora (HH:MM):", default_value=turn["hour"])
    email_entry = create_entry(frame, "Email:", default_value=turn["email"])
    phone_entry = create_entry(frame, "Teléfono:", default_value=turn["phone"])

    # Función para actualizar el turno
    def submit_changes():
        # Recoger los nuevos valores de los Entry (si están vacíos, mantener los valores originales)
        name = name_entry.get() or turn["name"]
        last_name = last_name_entry.get() or turn["last_name"]
        date = date_entry.get() or turn["date"]
        hour = hour_entry.get() or turn["hour"]
        email = email_entry.get() or turn["email"]
        phone = phone_entry.get() or turn["phone"]

        # Crear un diccionario con los datos actualizados
        updated_data = {
            "name": name,
            "last_name": last_name,
            "date": date,
            "hour": hour,
            "email": email,
            "phone": phone,
        }

        # Llamar a la función para modificar el turno en la base de datos
        modify_turn_bd(updated_data, turn["id"])
        # Muestra mensaje de éxito
        messagebox.showinfo("Éxito", "Turno modificado correctamente.")
        modify_specific_turn_window.destroy() # Cerrar la ventana después de modificar
        modify_turn.destroy()

    # Crear un botón para enviar los cambios
    submit_button = tk.Button(
        modify_specific_turn_window,
        text="Modificar Turno",
        bg="blue",
        fg="white",
        command=submit_changes,
    )
    submit_button.pack(pady=10)
    



def cancel_turn():
    cancel_turn_window = tk.Toplevel(app)
    cancel_turn_window.configure(bg="black")
    cancel_turn_window.geometry("720x480")
    cancel_turn_window.title("Cancelar turno")
    label = tk.Label(cancel_turn_window, text="Cancelar turno", bg="black", fg="white")
    label.pack()

    # Crear un frame para organizar el texto y el Entry
    frame = tk.Frame(cancel_turn_window)
    frame.pack(pady=20)

    date_entry = create_entry(
        frame, "Fecha del turno que deseas modificar (YYYY-MM-DD):"
    )

    def search_turns():
        date_turn = date_entry.get()
        turns = show_turns()
        filtered_turns = [turn for turn in turns if turn["date"] == date_turn]

        # Limpiar la ventana de turnos anteriores
        for widget in cancel_turn_window.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        # Mostrar los turnos filtrados o un mensaje si no hay turnos para esa fecha
        if not filtered_turns:
            label = tk.Label(
                cancel_turn_window,
                text="No hay turnos para esa fecha.",
                bg="black",
                fg="white",
            )
            label.pack()
        else:
            label = tk.Label(
                cancel_turn_window, text="Turnos disponibles:", bg="black", fg="white"
            )
            label.pack()

            for turn in filtered_turns:
                # Usar lambda para pasar el turno específico a la función modify_specific_turn
                button = tk.Button(
                    cancel_turn_window,
                    text=f"{turn['name']} {turn['last_name']} - {turn['hour']}",
                    command=lambda turn_id=turn['id']: cancel_turn_db(turn_id),
                )
                button.pack(pady=10)
                
                cancel_turn_window.destroy()    
                # Muestra mensaje de éxito
                messagebox.showinfo("Éxito", "Turno eliminado correctamente.")

                
     # Botón para buscar turnos después de ingresar la fecha
    
    search_button = tk.Button(cancel_turn_window, text="Buscar Turnos", command=search_turns)
    search_button.pack(pady=10)


app = tk.Tk()
app.geometry("720x480")
app.configure(bg="black")

tk.Wm.wm_title(app, "Reservas de turnos")

button1 = tk.Button(
    app, text="Reservar turno", bg="blue", fg="white", command=open_reserve_turn
)
button1.pack(fill=tk.X)

button2 = tk.Button(
    app, text="Mostrar turnos", bg="blue", fg="white", command=show_turn
)
button2.pack(fill=tk.X)

button3 = tk.Button(
    app, text="Modificar turno", bg="blue", fg="white", command=modify_turn
)
button3.pack(fill=tk.X)

button4 = tk.Button(
    app, text="Cancelar turno", bg="blue", fg="white", command=cancel_turn
)
button4.pack(fill=tk.X)

app.mainloop()
