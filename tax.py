import time
import sqlite3
from datetime import datetime
import os
from dataclasses import dataclass, asdict


# ==============================================
# SQLite DB
# ==============================================
class TripDB:
    def __init__(self, db_name="trips.db"):
        db_path = os.path.join(os.getcwd(), db_name)
        print(f"[TripDB] Base de datos SQLite en: {db_path}")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()


    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT,
                stopped_time REAL,
                moving_time REAL,
                total_fare REAL
            )
        """)
        self.conn.commit()


    def save_trip(self, trip):
        try:
            data = trip.to_dict()
            self.cursor.execute("""
                INSERT INTO trips (start_time, stopped_time, moving_time, total_fare)
                VALUES (?, ?, ?, ?)
            """, (
                data['start_time'],
                data['stopped_time'],
                data['moving_time'],
                data['total_fare']
            ))
            self.conn.commit()
            print("[TripDB] Viaje guardado correctamente:", data)
        except Exception as e:
            print("[TripDB] Error guardando viaje:", e)


    def get_all_trips(self):
        self.cursor.execute("""
            SELECT id, start_time, stopped_time, moving_time, total_fare
            FROM trips ORDER BY id DESC
        """)
        return self.cursor.fetchall()


    def close(self):
        self.conn.close()




# ==============================================
# Modelo Trip
# ==============================================
@dataclass
class Trip:
    start_time: str
    stopped_time: float
    moving_time: float
    total_fare: float


    def to_dict(self):
        return asdict(self)




# ==============================================
# Taximeter – SOLO LÓGICA
# ==============================================
class Taximeter:
    def __init__(self):
        self.trip_active = False
        self.stopped_time = 0.0
        self.moving_time = 0.0
        self.state = None
        self.state_start_time = 0.0
        self.start_time = None
        self.db = TripDB("trips.db")


    def calculate_fare(self):
        return self.stopped_time * 0.02 + self.moving_time * 0.05


    def start_trip(self):
        if self.trip_active:
            print("Error: Ya hay un viaje en curso.")
            return


        self.trip_active = True
        self.stopped_time = 0.0
        self.moving_time = 0.0
        self.state = "stopped"
        self.state_start_time = time.time()
        self.start_time = datetime.now().isoformat()


        print("Viaje iniciado.")


    def change_state(self, new_state):
        if not self.trip_active:
            print("Error: No hay viaje activo.")
            return


        duration = time.time() - self.state_start_time


        if self.state == "stopped":
            self.stopped_time += duration
        elif self.state == "moving":
            self.moving_time += duration


        self.state = new_state
        self.state_start_time = time.time()


        print(f"Estado cambiado a '{new_state}'.")


    def finish_trip(self):
        if not self.trip_active:
            print("Error: No hay viaje activo.")
            return


        duration = time.time() - self.state_start_time


        if self.state == "stopped":
            self.stopped_time += duration
        elif self.state == "moving":
            self.moving_time += duration


        total_fare = self.calculate_fare()


        trip = Trip(
            start_time=self.start_time,
            stopped_time=self.stopped_time,
            moving_time=self.moving_time,
            total_fare=total_fare
        )


        self.db.save_trip(trip)


        # Reset
        self.trip_active = False
        self.state = None
        self.state_start_time = 0.0
        self.start_time = None




# FIN DEL ARCHIVO



