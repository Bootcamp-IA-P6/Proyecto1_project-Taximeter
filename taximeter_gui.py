import tkinter as tk
from tkinter import messagebox
import time
import logging
from refactorizar_taximeter_oop import Trip, TripStorage, TaximeterLogger

# ==============================================
# Logger OOP
# ==============================================
class TaximeterLogger:
    def __init__(self, logfile="taximeter_gui.log"):
        self.logger = logging.getLogger("taximeter_logger")
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
        fh.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(fh)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)


# ==============================================
# Trip Model
# ==============================================
class Trip:
    def __init__(self, stopped_rate=0.02, moving_rate=0.05):
        self.stopped_rate = stopped_rate
        self.moving_rate = moving_rate
        self.start_time = time.time()
        self.stopped_time = 0.0
        self.moving_time = 0.0
        self.state = "stopped"
        self.state_start_time = time.time()

    def change_state(self, new_state):
        now = time.time()
        elapsed = now - self.state_start_time
        if self.state == "stopped":
            self.stopped_time += elapsed
        else:
            self.moving_time += elapsed
        self.state = new_state
        self.state_start_time = now
        return elapsed

    def finish(self):
        now = time.time()
        elapsed = now - self.state_start_time
        if self.state == "stopped":
            self.stopped_time += elapsed
        else:
            self.moving_time += elapsed
        return self.calculate_fare()

    def calculate_fare(self):
        return self.stopped_time * self.stopped_rate + self.moving_time * self.moving_rate

    def to_dict(self):
        return {
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time)),
            "stopped_time": self.stopped_time,
            "moving_time": self.moving_time,
            "total_fare": self.calculate_fare()
        }


# ==============================================
# TripStorage
# ==============================================
class TripStorage:
    def __init__(self, filename="trip_history_gui.txt"):
        self.filename = filename

    def save(self, trip: Trip):
        data = trip.to_dict()
        with open(self.filename, "a") as f:
            f.write(f"--- Trip {data['start_time']} ---\n")
            f.write(f"Stopped time: {data['stopped_time']:.1f} seconds\n")
            f.write(f"Moving time: {data['moving_time']:.1f} seconds\n")
            f.write(f"Total fare: €{data['total_fare']:.2f}\n")
            f.write("-------------------------------\n\n")


# ==============================================
# Ventana de Login
# ==============================================
class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login - Taxímetro F5")
        self.master.geometry("450x300")
        self.master.configure(bg="lightblue")  # <- aquí se pone el color

        tk.Label(master, text="Bienvenido al Taxímetro F5", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(master, text="Usuario:").pack()
        self.user_entry = tk.Entry(master)
        self.user_entry.pack(pady=5)

        tk.Label(master, text="Contraseña:").pack()
        self.pass_entry = tk.Entry(master, show="*")
        self.pass_entry.pack(pady=5)

        self.login_button = tk.Button(master, text="Iniciar sesión", command=self.authenticate)
        self.login_button.pack(pady=10)

        self.master.bind('<Return>', lambda event: self.authenticate())  # Enter key

    def authenticate(self):
        USER = "admin"
        PASSWORD = "1234"

        username = self.user_entry.get()
        password = self.pass_entry.get()

        if username == USER and password == PASSWORD:
            messagebox.showinfo("Acceso concedido", f"Bienvenido {username} al Taxímetro F5!")
            self.master.destroy()  # cerrar ventana de login
            open_taximeter_window()  # abrir ventana principal
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")


# ==============================================
# GUI Principal del Taxímetro
# ==============================================
class TaximeterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Taxímetro F5 - GUI")
        self.root.geometry("400x450")

        # --- Objetos reales ---
        self.trip = None
        self.logger = TaximeterLogger()
        self.storage = TripStorage()

        # --- Widgets GUI ---
        self.title_label = tk.Label(root, text="Taxímetro F5", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        self.state_label = tk.Label(root, text="Estado: (sin viaje)", font=("Arial", 14))
        self.state_label.pack(pady=10)

        self.fare_label = tk.Label(root, text="Tarifa total: €0.00", font=("Arial", 14))
        self.fare_label.pack(pady=10)

        self.time_label = tk.Label(root, text="Tiempo detenido: 0s | Movimiento: 0s", font=("Arial", 12))
        self.time_label.pack(pady=10)

        # Botones
        self.start_button = tk.Button(root, text="Start Trip", width=12, command=self.start_trip)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop", width=12, state="disabled", command=self.set_stopped)
        self.stop_button.pack(pady=5)

        self.move_button = tk.Button(root, text="Move", width=12, state="disabled", command=self.set_moving)
        self.move_button.pack(pady=5)

        self.finish_button = tk.Button(root, text="Finish Trip", width=12, state="disabled", command=self.finish_trip)
        self.finish_button.pack(pady=5)

        # Activar actualización automática
        self.update_loop()

    # ------------------------------------------------------
    # Funciones del taxímetro
    # ------------------------------------------------------
    def start_trip(self):
        if self.trip is not None:
            messagebox.showerror("Error", "Ya hay un viaje en curso.")
            return

        self.trip = Trip(stopped_rate=0.02, moving_rate=0.05)
        self.logger.info("Viaje iniciado (GUI).")

        self.state_label.config(text="Estado: detenido")
        self.stop_button.config(state="normal")
        self.move_button.config(state="normal")
        self.finish_button.config(state="normal")

    def set_stopped(self):
        if self.trip:
            self.trip.change_state("stopped")
            self.state_label.config(text="Estado: detenido")
            self.logger.info("Estado cambiado a detenido (GUI)")

    def set_moving(self):
        if self.trip:
            self.trip.change_state("moving")
            self.state_label.config(text="Estado: en movimiento")
            self.logger.info("Estado cambiado a movimiento (GUI)")

    def finish_trip(self):
        if not self.trip:
            return

        total_fare = self.trip.finish()
        data = self.trip.to_dict()
        self.storage.save(self.trip)
        self.logger.info(f"Viaje finalizado (GUI). Total: €{total_fare:.2f}")

        messagebox.showinfo("Viaje finalizado", f"Tarifa total: €{total_fare:.2f}")

        # Reset GUI
        self.trip = None
        self.state_label.config(text="Estado: (sin viaje)")
        self.fare_label.config(text="Tarifa total: €0.00")
        self.time_label.config(text="Tiempo detenido: 0s | Movimiento: 0s")
        self.stop_button.config(state="disabled")
        self.move_button.config(state="disabled")
        self.finish_button.config(state="disabled")

    # ------------------------------------------------------
    # Actualización automática de pantalla
    # ------------------------------------------------------
    def update_loop(self):
        if self.trip:
            fare = self.trip.calculate_fare()
            self.fare_label.config(text=f"Tarifa total: €{fare:.2f}")
            self.time_label.config(
                text=f"Tiempo detenido: {int(self.trip.stopped_time)}s | "
                     f"Movimiento: {int(self.trip.moving_time)}s"
            )
        self.root.after(1000, self.update_loop)


# ==============================================
# Función para abrir la ventana del taxímetro
# ==============================================
def open_taximeter_window():
    root = tk.Tk()
    app = TaximeterGUI(root)
    root.mainloop()


# ==============================================
# Main
# ==============================================
if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()
