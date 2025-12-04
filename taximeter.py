import time

def calculate_fare(seconds_stopped, seconds_moving):
    """
    Calcular la tarifa total en euros.
    - Stopped: 0.02 €/s
    - Moving: 0.05 €/s
    """
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    print(f"Este es el total: {fare}")
    return fare

def taximeter():
    """
    Función para manejar y mostrar las opciones del taxímetro.
    """
    print("Welcome to the F5 Taximeter!")
    print("Available commands: 'start', 'stop', 'move', 'finish', 'exit'\n")

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
                continue
            trip_active = True
            start_time = time.time()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'  # Iniciamos en estado 'stopped'
            state_start_time = time.time()
            print("Trip started. Initial state: 'stopped'.")