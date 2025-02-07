import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from turns import (
    delete_turn,
    show_turns,
    reserve_turn,
    modify_turn as modify_turn_bd,
)


def create_entry(frame, label_text, default_value=""):
    # Crear el label
    label = tk.Label(frame, text=label_text,background='black', foreground='white', font=("Arial", 12, "bold"))
    label.grid(pady=2)

    # Crear el Entry
    entry = ttk.Entry(frame)
    entry.grid(pady=15, padx=200)

    # Establecer valor por defecto
    entry.insert(0, default_value)
    
    # Aplicar el estilo si lo deseas
    style = ttk.Style()
    style.configure("Custom.TEntry",
                    foreground="black",
                    background="white",
                    font=("Arial", 12))

    entry.configure(style="Custom.TEntry")

    return entry

# Pantalla de reserva.
def open_reserve_turn():
    reserve_turn_window = tk.Toplevel(app)
    reserve_turn_window.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    reserve_turn_window.configure(bg="black")
    reserve_turn_window.title("Reservar turno",)
    label = tk.Label(reserve_turn_window, text="Reservar turno", bg="black", fg="white", font=("Arial", 20, "bold"))
    label.pack(pady=25)
    

    # Crear un frame para organizar el texto y el Entry
    frame = tk.Frame(reserve_turn_window, bg="black", bd=5, highlightbackground="#404040", highlightthickness=2)
    frame.pack(pady=20, padx=200)


    # Crear varios Entry con sus labels
    entry1 = create_entry(frame, "Nombre:")
    entry2 = create_entry(frame, "Apellido:")
    entry3 = create_entry(frame, "Fecha - YYYY-MM-DD:")
    entry4 = create_entry(frame, "Hora - HH:MM:")
    entry5 = create_entry(frame, "Email:")
    entry6 = create_entry(frame, "Teléfono:")
    
    # Label para mostrar los errores
    error_label = tk.Label(reserve_turn_window, text="", bg="black", fg="red")
    error_label.pack(pady=10)

    ttk.Button(
        reserve_turn_window,
        text="Reservar",
        style="Modern.TButton",
        command=lambda: handle_reserve(
            {
                "name": entry1.get(),
                "last_name": entry2.get(),
                "date": entry3.get(),
                "hour": entry4.get(),
                "email": entry5.get(),
                "phone": entry6.get(),
            }, reserve_turn_window, error_label
        ),
    ).pack(pady=10)
    
    # Maneja errores en Resrva.
    def handle_reserve(data, window, error_label):
        success = reserve_turn(data)
        if success.get("success"):
            error_label.config(text="")
            messagebox.showinfo("Éxito", "Turno guardado correctamente.")
            window.destroy()  # Cierra la ventana solo si la operación fue exitosa
        else:
            errores = success["errors"]
            error_text = "\n".join([f"{campo}: {mensaje}" for campo, mensaje in errores.items()])
            error_label.config(text=error_text)  # Muestra todos los errores en la etiqueta


# Pantalla para mostrar todos los turnos
def show_turn():
    show_turn_window = tk.Toplevel(app)
    show_turn_window.configure(bg="black")
    show_turn_window.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    show_turn_window.title("Reservar turno")
    
    label = tk.Label(show_turn_window, text="Todos los turnos", bg="black", fg="white", font=("Arial", 16, "bold"))
    label.pack(pady=20)

    turns = show_turns()

    # Frame principal para contener todos los turnos
    frame = tk.Frame(show_turn_window, bg="black", bd=5, highlightbackground="#404040", highlightthickness=2)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Canvas para permitir el desplazamiento si hay muchos turnos
    canvas = tk.Canvas(frame, bg="black")
    canvas.pack(side="left", fill="both", expand=True)
    
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    
    turn_frame = tk.Frame(canvas, bg="black")
    canvas.create_window((0, 0), window=turn_frame, anchor="nw")

    # Iterar sobre los turnos y mostrarlos en el frame
    for i, turn in enumerate(turns):
        turn_frame.grid_rowconfigure(i, weight=1)

        # Crear un Frame individual para cada turno
        turn_widget = tk.Frame(turn_frame, bg="#333333", bd=2, relief="solid", padx=10, pady=10)
        turn_widget.grid(row=i, column=0, sticky="w", padx=5, pady=5)

        # Etiquetas con la información del turno
        turn_label = tk.Label(
            turn_widget,
            text=f"{turn['name']} {turn['last_name']} - {turn['date']} {turn['hour']} - {turn['email']} - {turn['phone']}",
            bg="#333333",
            fg="white",
            font=("Arial", 12)
        )
        turn_label.pack()

    # Actualizar el scrollregion para el canvas
    turn_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Pantalla para buscar y seleccionar turnos a modificar
def modify_turn():
    modify_turn_window = tk.Toplevel(app)
    modify_turn_window.configure(bg="black")
    modify_turn_window.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    modify_turn_window.title("Modificar turno")

    label = tk.Label(modify_turn_window, text="Modificar turno", bg="black", fg="white",font=("Arial", 20, "bold") )
    label.pack(pady=25)

    # Crear un frame para organizar el texto y el Entry
    frame = tk.Frame(modify_turn_window, bg="black", bd=5, highlightbackground="#404040", highlightthickness=2)
    frame.pack(pady=20, padx=200)

    date_entry = create_entry(
        frame, "Nombre del paciente que tiene el turno:"
    )
    
    # Frame para contener los botones de los turnos
    turn_buttons_frame = tk.Frame(modify_turn_window, bg="black")
    turn_buttons_frame.pack(pady=20)


    # Función para actualizar los turnos
    def update_turns():
        for widget in turn_buttons_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.destroy()
            elif isinstance(widget, tk.Label):
                widget.destroy()
        
        # Obtener la fecha desde el Entry
        name_turn = date_entry.get()
        turns = show_turns()
        filtered_turns = [turn for turn in turns if turn["name"] == name_turn]

        # Mostrar los turnos filtrados o un mensaje si no hay turnos para esa fecha
        if not filtered_turns:
            label = tk.Label(
                turn_buttons_frame,
                text="No hay turnos para esa fecha.",
                bg="black",
                fg="white",
                font=("Arial", 15, "bold")
            )
            label.pack()
        else:
            label = tk.Label(
                turn_buttons_frame, text="Turnos disponibles:", bg="black", fg="white", font=("Arial", 15, "bold")
            )
            label.pack()

            for turn in filtered_turns:
                # Usar lambda para pasar el turno específico a la función modify_specific_turn
                button = ttk.Button(
                    turn_buttons_frame,
                    style="Modern.TButton",
                    text=f"{turn['name']} {turn['last_name']} - {turn['hour']}",
                    command=lambda t=turn: modify_specific_turn(t, modify_turn_window),
                )
                button.pack(pady=10)

    
    # Botón para actualizar la lista de turnos
    update_button = ttk.Button(
        modify_turn_window,
        text="Actualizar Turnos",
        style="Modern.TButton",
        command=update_turns,
    )
    update_button.pack(pady=10)
    
# Pantalla para modificar un turno específico
def modify_specific_turn(turn, modify_turn_window):
    modify_specific_turn_window = tk.Toplevel(app)
    modify_specific_turn_window.configure(bg="black")
    modify_specific_turn_window.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    modify_specific_turn_window.title("Modificar turno específico")

    label = tk.Label(
        modify_specific_turn_window,
        text="Modifique solamente los campos que necesite",
        bg="black",
        fg="white",
        font=("Arial", 20, "bold")
        
    )
    label.pack(pady=20)

    # Crear un frame para organizar el texto y los Entry
    frame = tk.Frame(modify_specific_turn_window, bg="black", bd=5, highlightbackground="#404040", highlightthickness=2)
    frame.pack(pady=20, padx=200)

    # Crear entradas pre-rellenadas con los valores actuales del turno
    name_entry = create_entry(frame, "Nombre:", default_value=turn["name"])
    last_name_entry = create_entry(frame, "Apellido:", default_value=turn["last_name"])
    date_entry = create_entry(frame, "Fecha (YYYY-MM-DD):", default_value=turn["date"])
    hour_entry = create_entry(frame, "Hora (HH:MM):", default_value=turn["hour"])
    email_entry = create_entry(frame, "Email:", default_value=turn["email"])
    phone_entry = create_entry(frame, "Teléfono:", default_value=turn["phone"])
    
    # Label para mostrar los errores
    error_label = tk.Label(modify_specific_turn_window, text="", bg="black", fg="red", font=("Arial", 15, "bold"))
    error_label.pack(pady=10)

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
        # Validar los datos
        if not name or not last_name or not date or not hour or not email or not phone:
            error_label.config(text="Todos los campos deben estar completos.")
            return  # No enviar los datos si hay campos vacíos

        # Llamar a la función para modificar el turno en la base de datos
        success = modify_turn_bd(updated_data, turn["id"])

        if success.get("success"):
            error_label.config(text="")
            messagebox.showinfo("Éxito", "Turno modificado correctamente.")
            modify_specific_turn_window.destroy()  # Cerrar la ventana después de modificar
            modify_turn_window.destroy()  # Cerrar la ventana de modificar turnos
        else:
            errores = success["errors"]
            error_text = "\n".join([f"{campo}: {mensaje}" for campo, mensaje in errores.items()])
            error_label.config(text=error_text)  # Muestra todos los errores en la etiqueta

    # Crear un botón para enviar los cambios
    submit_button = ttk.Button(
        modify_specific_turn_window,
        text="Modificar Turno",
        style="Modern.TButton",
        command=submit_changes,
    )
    submit_button.pack(pady=10)
    
# Pantalla para buscar un turno para cancelar
def cancel_turn():
    cancel_turn_window = tk.Toplevel(app)
    cancel_turn_window.configure(bg="black")
    cancel_turn_window.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    cancel_turn_window.title("Cancelar turno")
    label = tk.Label(cancel_turn_window, text="Cancelar turno", bg="black", fg="white", font=("Arial", 20, "bold"))
    label.pack(pady=20)

    # Crear un frame para organizar el texto y el Entry
    frame = tk.Frame(cancel_turn_window, bg="black", bd=5, highlightbackground="#404040", highlightthickness=2)
    frame.pack(pady=20)

    date_entry = create_entry(
        frame, "Nombre del paciente que quiere cancelar el turno:"
    )
    
    # Frame para contener los turnos
    turn_buttons_frame = tk.Frame(cancel_turn_window, bg="black")
    turn_buttons_frame.pack(pady=20)

    # Función de búsqueda de turnos según nombre
    def search_turns():
        name_turn = date_entry.get()
        turns = show_turns()
        filtered_turns = [turn for turn in turns if turn["name"] == name_turn]


        # Mostrar los turnos filtrados o un mensaje si no hay turnos para esa fecha
        if not filtered_turns:
            label = tk.Label(
                turn_buttons_frame,
                text="No hay turnos para esa fecha.",
                bg="black",
                fg="white",
                font=("Arial", 15, "bold")
            )
            label.pack()
        else:
            label = tk.Label(
                turn_buttons_frame, text="Turnos disponibles:", bg="black", fg="white", font=("Arial", 15, "bold"),           
            )
            label.pack()

            # Recorre y muestra los turnos filtrados por nombre
            for turn in filtered_turns:
                # Usar lambda para pasar el turno específico a la función modify_specific_turn
                button = ttk.Button(
                    turn_buttons_frame,
                    text=f"{turn['name']} {turn['last_name']} - {turn['hour']}",
                    style="Modern.TButton",
                    command=lambda turn_id=turn['id'], turn_name=turn['name'], turn_last_name=turn['last_name'], turn_email=turn['email']: handle_cancel(turn_id, turn_name, turn_last_name, turn_email, cancel_turn_window),
                )
                button.pack(pady=10)
                    

    
    
    # Función para manejar la cancelación y el cierre de la ventana
    def handle_cancel(turn_id, turn_name, turn_email, turn_last_name, window):
        success = delete_turn(turn_id, turn_name, turn_email, turn_last_name)
        if success:
            messagebox.showinfo("Éxito", "Turno eliminado correctamente.")
            window.destroy()  # 🔹 Cierra la ventana solo si la operación fue exitosa
        else:
            messagebox.showerror("Error", "No se pudo eliminar el turno.")
            
    # Botón para buscar turnos después de ingresar la fecha
    search_button = ttk.Button(cancel_turn_window, text="Buscar Turnos", command=search_turns, style="Modern.TButton")
    search_button.pack(pady=10)


# Creación de la interfaz en Tkinter
app = tk.Tk()
ancho_pantalla = app.winfo_screenwidth()
alto_pantalla = app.winfo_screenheight()

# Ajustar la ventana al tamaño del monitor
app.geometry(f"{ancho_pantalla}x{alto_pantalla}")
app.configure(bg="black")
imagen = tk.PhotoImage(file="calendar.png")

# Configurar estilo del botón
button_style = ttk.Style()
button_style.configure(
    "Modern.TButton",
    font=("Arial", 14, "bold"),  # Fuente moderna
    foreground="black",          # Color del texto
    background="#0078D7",        # Azul moderno (NO se aplica en ttk, pero lo usamos en map)
    padding=10,                  # Relleno interno
    borderwidth=2,
    relief="flat"                # Sin bordes elevados
)
button_style.map(
    "Modern.TButton",
    foreground=[("pressed", "black"), ("active", "black")],
    background=[("pressed", "#005A9E"), ("active", "#005A9E")],
)

# Titulo de la ventana
tk.Wm.wm_title(app, "Reservas de turnos")

# Label principal, titulo de la app
label = ttk.Label(app, text="Gestión de pacientes", background='black', foreground='white', font=("Arial", 20, "bold"))
label.pack(pady=20)  # Agrega espacio alrededor

# Label con la imagen de la pantalla principal
label_image = tk.Label(app, image=imagen, bg="black")
label_image.pack()

# Botones del menú
button1 = ttk.Button(
    app, text="Reservar turno", command=open_reserve_turn, style="Modern.TButton"
)
button1.pack(padx=20, pady=10)

button2 = ttk.Button(
    app, text="Mostrar turnos", command=show_turn, style="Modern.TButton"
)
button2.pack(padx=20, pady=10)

button3 = ttk.Button(
    app, text="Modificar turno", command=modify_turn, style="Modern.TButton"
)
button3.pack(padx=20, pady=10)  

button4 = ttk.Button(
    app, text="Cancelar turno", command=cancel_turn, style="Modern.TButton"
)
button4.pack(padx=20, pady=10)

button5 = ttk.Button(
    app, text="Salir", command=lambda: app.destroy() , style="Modern.TButton"
)
button5.pack(padx=20, pady=10)

# Función nativa de Tkinter que se encarga de empezar el bucle pincipal de eventos.
app.mainloop()
