import time
import logging

# ==============================================
# Logger OOP
# ==============================================
class TaximeterLogger:
    def __init__(self, logfile="taximeter.log"):
        self.logger = logging.getLogger("taximeter_logger")
        self.logger.setLevel(logging.DEBUG)

        # Handler
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
# Trip Model (representa un viaje)
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
# TripStorage (archivo)
# ==============================================
class TripStorage:
    def __init__(self, filename="trip_history.txt"):
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
# TaximeterApp (CLI y control)
# ==============================================
class TaximeterApp:
    def __init__(self):
        self.logger = TaximeterLogger()
        self.storage = TripStorage()
        self.current_trip = None

    def request_rates(self):
        try:
            stopped_rate = float(input("Ingrese precio por segundo detenido (€): "))
            moving_rate = float(input("Ingrese precio por segundo en movimiento (€): "))
        except ValueError:
            print("Entrada inválida. Usando precios por defecto (0.02/0.05).")
            stopped_rate = 0.02
            moving_rate = 0.05
        return stopped_rate, moving_rate

    def start_trip(self):
        if self.current_trip:
            print("Error: Un viaje ya está en curso.")
            self.logger.warning("Intento de iniciar un viaje cuando uno ya estaba activo.")
            return

        rates = self.request_rates()
        self.current_trip = Trip(*rates)

        print("Viaje iniciado. Estado inicial: 'stopped'.")
        self.logger.info("Viaje iniciado.")

    def change_state(self, state):
        if not self.current_trip:
            print("Error: No hay un viaje activo.")
            self.logger.warning(f"No se puede cambiar a {state}. No hay viaje activo.")
            return

        elapsed = self.current_trip.change_state(state)
        print(f"Estado cambiado a '{state}'.")
        self.logger.info(f"Estado cambiado a '{state}' después de {elapsed:.1f}s.")

    def finish_trip(self):
        if not self.current_trip:
            print("Error: No hay viaje para finalizar.")
            self.logger.warning("Intento de finalizar viaje sin viaje activo.")
            return

        total_fare = self.current_trip.finish()
        data = self.current_trip.to_dict()

        print("\n--- Resumen del viaje ---")
        print(f"Tiempo detenido: {data['stopped_time']:.1f} segundos")
        print(f"Tiempo en movimiento: {data['moving_time']:.1f} segundos")
        print(f"Tarifa total: €{data['total_fare']:.2f}")
        print("-------------------------\n")

        self.storage.save(self.current_trip)
        self.logger.info(f"Viaje finalizado. Tarifa: €{total_fare:.2f}")

        self.current_trip = None

    def run(self):
        print("Bienvenido al Taxímetro F5!")
        print("Comandos disponibles: start, stop, move, finish, exit")

        while True:
            cmd = input("> ").strip().lower()

            if cmd == "start":
                self.start_trip()
            elif cmd == "stop":
                self.change_state("stopped")
            elif cmd == "move":
                self.change_state("moving")
            elif cmd == "finish":
                self.finish_trip()
            elif cmd == "exit":
                print("Saliendo del programa. ¡Adiós!")
                self.logger.info("Programa terminado por usuario.")
                break
            else:
                print("Comando desconocido. Usa: start, stop, move, finish, exit.")
                self.logger.warning(f"Comando desconocido ingresado: '{cmd}'")


# ==============================================
# Autenticación
# ==============================================
def authenticate():
    """
    Solicita usuario y contraseña antes de permitir el acceso.
    """
    USER = "admin"       # Usuario autorizado
    PASSWORD = "1234"    # Contraseña autorizada

    print("=== Autenticación requerida ===")
    username = input("Usuario: ")
    password = input("Contraseña: ")

    if username == USER and password == PASSWORD:
        print("Acceso concedido.\n")
        return True
    else:
        print("Acceso denegado. Usuario o contraseña incorrectos.")
        return False


# ==============================================
# Main
# ==============================================
if __name__ == "__main__":
    if authenticate():       # Se autentica antes de iniciar la app
        app = TaximeterApp()
        app.run()
    else:
        exit()
