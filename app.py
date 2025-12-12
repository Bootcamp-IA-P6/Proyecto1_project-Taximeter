from flask import Flask, render_template, request, redirect, url_for, session
from tax import Taximeter  # tu clase Taximeter en tax.py


app = Flask(__name__)
app.secret_key = "supersecretkey"  # necesario para sesiones

# Usuarios en memoria
USERS = {
    "admin": "1234",
    "user1": "abcd"
}

# Instancia global del taxímetro
taximeter = Taximeter()

# ======================
# Ruta de login
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if username in USERS and USERS[username] == password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            # Error se muestra en login.html
            return render_template("login.html", error="Usuario o contraseña incorrectos")
            
    return render_template("login.html")


# ======================
# Página principal / control del taxímetro
# ======================
@app.route("/index", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        action = request.form["action"]
        if action == "start":
            taximeter.start_trip()
        elif action == "stop":
            taximeter.change_state("stopped")
        elif action == "move":
            taximeter.change_state("moving")
        elif action == "finish":
            taximeter.finish_trip()
    
    # Pasa información opcional del taxímetro a la plantilla
    return render_template("index.html", username=session["username"])


# ======================
# Ver todos los viajes
# ======================
@app.route("/trips")
def trips():
    if "username" not in session:
        return redirect(url_for("login"))

    trips_list = taximeter.db.get_all_trips()  # lista de tuplas
    return render_template("trips.html", trips=trips_list)


# ======================
# Cerrar sesión
# ======================
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


# ======================
# Ejecutar Flask
# ======================
if __name__ == "__main__":
    app.run(debug=True)
