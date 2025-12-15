import logging
import os

# ==========================
# Carpeta donde se guardarán los logs
# ==========================
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# ==========================
# Configuración del logger principal
# ==========================
logger = logging.getLogger("taximeter_logger")
logger.setLevel(logging.INFO)  # Nivel mínimo de logs


formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Handler para archivo
log_file = os.path.join(LOG_DIR, "app.log")
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


