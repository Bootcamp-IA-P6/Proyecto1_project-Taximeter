import time
import logging

# --------------------------
# Configuración del logger
# --------------------------
logger = logging.getLogger("taximeter_logger")
logger.setLevel(logging.DEBUG)  # Captura todos los niveles de log

# FileHandler para guardar logs en taximeter.log
fh = logging.FileHandler("taximeter.log")
fh.setLevel(logging.DEBUG)

# Formato del log: fecha;nivel;mensaje
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
fh.setFormatter(formatter)

# Evitar duplicación de handlers
if not logger.hasHandlers():
    logger.addHandler(fh)

# --------------------------
# Funciones del taxímetro
# --------------------------
def calculate_fare(seconds_stopped, seconds_moving, stopped_rate=0.02, moving_rate=0.05):
    """
    Calcular la tarifa total en euros con precios configurables.
    """
    fare = seconds_stopped * stopped_rate + seconds_moving * moving_rate
    logger.info(f"Fare calculated: €{fare:.2f} (Stopped: {seconds_stopped:.1f}s, Moving: {seconds_moving:.1f}s, Rates: {stopped_rate}/{moving_rate})")
    print(f"Este es el total: {fare:.2f}")
    return fare

def save_trip_record(start_time_str, stopped_time, moving_time, total_fare):
    """
    Guarda un registro del viaje en 'trip_history.txt' en modo append.
    """
    with open("trip_history.txt", "a") as file:
        file.write(f"--- Trip {start_time_str} ---\n")
        file.write(f"Stopped time: {stopped_time:.1f} seconds\n")
        file.write(f"Moving time: {moving_time:.1f} seconds\n")
        file.write(f"Total fare: €{total_fare:.2f}\n")
        file.write("-------------------------------\n\n")

def taximeter():
    """
    Función para manejar y mostrar las opciones del taxímetro.
    """
    print("Welcome to the F5 Taximeter!")
    print("Available commands: 'start', 'stop', 'move', 'finish', 'exit'\n")

    # --------------------------
    # Configuración dinámica de precios
    # --------------------------
    try:
        stopped_rate = float(input("Ingrese precio por segundo detenido (€): "))
        moving_rate = float(input("Ingrese precio por segundo en movimiento (€): "))
    except ValueError:
        print("Entrada inválida. Usando precios por defecto (0.02/0.05).")
        stopped_rate = 0.02
        moving_rate = 0.05

    trip_active = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None  # 'stopped' o 'moving'
    state_start_time = 0

    while True:
        command = input("> ").strip().lower()

        if command == "start":
            if trip_active:
                print("Error: A trip is already in progress.")
                logger.warning("Tried to start a trip, but one is already active.")
                continue
            trip_active = True
            start_time = time.time()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'
            state_start_time = time.time()
            print("Trip started. Initial state: 'stopped'.")
            logger.info("Trip started. Initial state: 'stopped'.")

        elif command in ("stop", "move"):
            if not trip_active:
                print("Error: No active trip. Please start first.")
                logger.warning(f"Tried to change state to '{command}', but no trip is active.")
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration
            state = 'stopped' if command == "stop" else 'moving'
            state_start_time = time.time()
            print(f"State changed to '{state}'.")
            logger.info(f"State changed to '{state}' after {duration:.1f} seconds in previous state.")

        elif command == "finish":
            if not trip_active:
                print("Error: No active trip to finish.")
                logger.warning("Tried to finish a trip, but no trip is active.")
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration

            total_fare = calculate_fare(stopped_time, moving_time, stopped_rate, moving_rate)

            start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
            save_trip_record(start_time_str, stopped_time, moving_time, total_fare)

            print(f"\n--- Trip Summary ---")
            print(f"Stopped time: {stopped_time:.1f} seconds")
            print(f"Moving time: {moving_time:.1f} seconds")
            print(f"Total fare: €{total_fare:.2f}")
            print("---------------------\n")
            logger.info(f"Trip finished. Stopped: {stopped_time:.1f}s, Moving: {moving_time:.1f}s, Total fare: €{total_fare:.2f}")

            trip_active = False
            state = None

        elif command == "exit":
            print("Exiting the program. Goodbye!")
            logger.info("Program exited by user.")
            break

        else:
            print("Unknown command. Use: start, stop, move, finish, or exit.")
            logger.warning(f"Unknown command entered: '{command}'")

# --------------------------
# Ejecución principal
# --------------------------
if __name__ == "__main__":
    taximeter()