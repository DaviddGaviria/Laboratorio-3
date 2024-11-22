import trivia_client as client
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button
from PIL import Image, ImageDraw, ImageTk
import time
import math

def pseudo_random_integer(minimo, maximo):
    seed = int(time.time() * 1000) % (2**32 - 1)
    return minimo + seed % (maximo - minimo + 1)

# Función para cargar los datos de usuarios
def load_users(filename="users.txt"):
    users = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    password = parts[1].strip()
                    status = parts[2].strip() if len(parts) > 2 else 'desconectado'
                    users[name] = {'password': password, 'status': status}
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo {filename}")
    return users

# Función para guardar los datos de usuarios
def save_users(users, filename="users.txt"):
    with open(filename, 'w', encoding='utf-8') as file:
        for name, data in users.items():
            file.write(f"{name},{data['password']},{data['status']}\n")

# Función para leer los datos de puntajes
def load_scores(filename="scores.txt"):
    scores = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                name, score = line.strip().split(',')
                scores[name.strip()] = int(score.strip())
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo {filename}")
    return scores

# Función para leer las preguntas
def load_questions(filename="questions.txt"):
    questions = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) >= 6:
                    category, question, *options, answer = parts
                    questions.append({
                        'category': category,
                        'question': question,
                        'options': options,
                        'answer': answer
                    })
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo {filename}")
    return questions
# Función para crear las imágenes con la flecha rotada
def create_arrow_images(image_path, arrow_length=100):
    base_image = Image.open(image_path).convert("RGBA")
    centro_x = base_image.size[0] // 2
    centro_y = base_image.size[1] // 2
    
    images = []
    for angle in range(0, 360, 10):
        new_image = base_image.copy()
        draw = ImageDraw.Draw(new_image)
        end_x = centro_x + arrow_length * -1 * math.sin(math.radians(angle))
        end_y = centro_y + arrow_length * -1 * math.cos(math.radians(angle))
        draw.line((centro_x, centro_y, end_x, end_y), fill="red", width=5)
        images.append(ImageTk.PhotoImage(new_image))
    
    return images

# Clase principal de la aplicación
class TriviaClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Client")

        # Aplicar tema con ttkbootstrap
        style = Style(theme="cosmo")

        # Variables
        self.url = "http://localhost:80"
        self.name = tk.StringVar()
        self.password = tk.StringVar()
        self.score = tk.IntVar()

        # Cargar datos
        self.users = load_users()
        self.scores = load_scores()
        self.questions = load_questions("questions.txt")

        # Configuración de estilos
        style.configure('TFrame', background='#1f2847')
        style.configure('TLabel', background='#1f2847', foreground='white', font=("Poppins", 12))
        style.configure('TEntry', font=("Poppins", 12))
        style.configure('TButton', background='#334d93', foreground='white', font=("Poppins", 12))
        style.map("TButton", background=[('active', '#263b73')])

        # Marco principal
        frame = tk.Frame(root, padx=20, pady=20, bg="#1f2847")
        frame.pack()
        # Etiquetas y entradas
        tk.Label(frame, text="Usuario:", font=("Poppins", 12), bg="#1f2847", fg="white").grid(row=0, column=0, sticky="e", pady=5)
        tk.Entry(frame, textvariable=self.name, font=("Poppins", 12), bg="white", fg="black").grid(row=0, column=1, pady=5)
        tk.Label(frame, text="Contraseña:", font=("Poppins", 12), bg="#1f2847", fg="white").grid(row=1, column=0, sticky="e", pady=5)
        tk.Entry(frame, textvariable=self.password, show="*", font=("Poppins", 12), bg="white", fg="black").grid(row=1, column=1, pady=5)

        # Botones
        buttons = [
            ("Registrar Usuario", self.register_user),
            ("Iniciar Sesión", self.open_session),
            ("Cerrar Sesión", self.close_session),
            ("Lista Conectados", self.show_user_status),
            ("Ranked", self.show_ranked)
        ]

        for i, (text, command) in enumerate(buttons):
            Button(frame, text=text, command=command, bootstyle="primary").grid(row=2 + i // 2, column=i % 2, pady=10, padx=10)

    def register_user(self):
        username = self.name.get().strip()
        password = self.password.get().strip()
        if not username or not password:
            messagebox.showerror("Registro", "El nombre de usuario y la contraseña no deben estar vacíos.")
            return
        if username in self.users:
            messagebox.showerror("Registro", "El usuario ya existe.")
        else:
            response = client.registerUser(self.url, username, password)
            if response:
                self.users[username] = {'password': password, 'status': 'desconectado'}
                save_users(self.users)
                messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
            else:
                messagebox.showerror("Registro", "Error al registrar el usuario.")

    def open_session(self):
        username = self.name.get().strip()
        password = self.password.get().strip()
        if not username or not password:
            messagebox.showerror("Iniciar Sesión", "El nombre de usuario y la contraseña no deben estar vacíos.")
            return
        if username in self.users and self.users[username]['password'] == password:
            self.users[username]['status'] = 'conectado'
            save_users(self.users)
            self.score.set(self.scores.get(username, 0))  # Cargar puntaje al iniciar sesión
            messagebox.showinfo("Iniciar Sesión", "Sesión correctamente iniciada.")
            self.open_wheel_window()
        else:
            messagebox.showerror("Iniciar Sesión", "Usuario o contraseña incorrectos.")

    def open_wheel_window(self):
        wheel_window = tk.Toplevel(self.root)
        wheel_window.title("Ruleta")
        wheel_window.configure(background="#1f2847")

        # Crear imágenes con la flecha rotada
        try:
            images = create_arrow_images("ruleta.png")
            image_label = tk.Label(wheel_window, image=images[0], background="#1f2847")
            image_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cargar la imagen: {e}")

        button_frame = tk.Frame(wheel_window, background="#1f2847")
        button_frame.pack(pady=10)

        Button(button_frame, text="Girar Ruleta", bootstyle="primary", command=lambda: self.start_spin(image_label, images)).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Puntaje", bootstyle="primary", command=self.show_score).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Salir", bootstyle="danger", command=wheel_window.destroy).grid(row=0, column=2, padx=5)

    def start_spin(self, image_label, images):
        stop_angle = self.animate_wheel(image_label, images)
        category = self.get_category_by_angle(stop_angle)
        messagebox.showinfo("Categoría Seleccionada", f"La categoría seleccionada es: {category}")
        self.show_random_question(category)

    def animate_wheel(self, image_label, images, angle=0, stop_angle=None):
        def update_image(angle):
            rotated_image = images[angle // 10 % len(images)]
            image_label.configure(image=rotated_image)
            image_label.image = rotated_image

        if stop_angle is None:
            stop_angle = pseudo_random_integer(0, 359) // 10 * 10  # Ajustar el ángulo al múltiplo de 10
        
        # Velocidad inicial
        speed = 10

        while angle != stop_angle:
            self.root.update()
            time.sleep(0.01)  # Ajusta este valor para controlar la velocidad del giro
            angle = (angle + speed) % 360
            update_image(angle)
            speed = max(1, speed - 1)  # Reducir velocidad gradualmente
            
        return stop_angle

    def get_category_by_angle(self, angle):
        if 0 <= angle < 90:
            return "Deportes"
        elif 90 <= angle < 180:
            return "Ciencia"
        elif 180 <= angle < 270:
            return "Historia"
        else:
            return "Arte"

    def show_score(self):
        username = self.name.get().strip()
        score = self.scores.get(username, 0)
        messagebox.showinfo("Puntaje", f"El puntaje de {username} es: {score}")

    def show_random_question(self, category=None):
        try:
            if category:
                questions_in_category = [q for q in self.questions if q['category'] == category]
                question = questions_in_category[pseudo_random_integer(0, len(questions_in_category) - 1)]
            else:
                question = self.questions[pseudo_random_integer(0, len(self.questions) - 1)]

            category = question['category']
            question_text = question['question']
            options = question['options']
            correct_answer = question['answer']

            question_window = tk.Toplevel(self.root)
            question_window.title("Pregunta de Trivia")
            question_window.configure(background="#1f2847")

            tk.Label(question_window, text=f"Categoría: {category}", font=("Poppins", 12), background="#1f2847", foreground="white").pack(pady=10)
            tk.Label(question_window, text=question_text, font=("Poppins", 12), background="#1f2847", foreground="white").pack(pady=10)

            selected_answer = tk.StringVar()
            for idx, option in enumerate(options):
                tk.Radiobutton(question_window, text=f"{chr(97 + idx)}: {option}", variable=selected_answer, value=chr(97 + idx), font=("Poppins", 12), background="#1f2847", foreground="white").pack(anchor="w")

            Button(question_window, text="Enviar Respuesta", command=lambda: self.check_answer(selected_answer.get(), correct_answer, options, question_window), bootstyle="primary").pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cargar la pregunta: {e}")

    def check_answer(self, selected_answer, correct_answer, options, question_window):
        if selected_answer == correct_answer:
            messagebox.showinfo("Respuesta Correcta", "¡Correcto!")
            self.score.set(self.score.get() + 1)
            self.scores[self.name.get().strip()] = self.score.get()
            self.update_score_file()
        else:
            correct_option = options[ord(correct_answer) - 97]
            messagebox.showerror("Respuesta Incorrecta", f"Incorrecto. La respuesta correcta era: {correct_answer}: {correct_option}")
        question_window.destroy()

    def close_session(self):
        username = self.name.get().strip()
        if username in self.users:
            self.users[username]['status'] = 'desconectado'
            save_users(self.users)
            messagebox.showinfo("Cerrar Sesión", "Sesión cerrada exitosamente. Adiós.")
            response = client.closeSession(self.url, username, self.password.get())
            self.root.quit()
        else:
            messagebox.showerror("Cerrar Sesión", "El usuario no está registrado.")

    def show_user_status(self):
        user_status_list = "\n".join([f"{user}: {data['status']}" for user, data in self.users.items()])
        messagebox.showinfo("Lista de Conectados", user_status_list)

    def show_ranked(self):
        ranked_users = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
        ranked_list = "\n".join([f"{user}: {score}" for user, score in ranked_users])
        messagebox.showinfo("Tabla de Clasificación", ranked_list)

    def update_score_file(self):
        with open("scores.txt", 'w', encoding='utf-8') as file:
            for name, score in self.scores.items():
                file.write(f"{name},{score}\n")

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaClientApp(root)
    root.mainloop()
