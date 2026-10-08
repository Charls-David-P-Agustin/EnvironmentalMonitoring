from flask import Flask, request, render_template
import mariadb

app = Flask(__name__)

db = mariadb.connect(
    host="localhost",
    user="root",
    password="12345",
    database="environmental_monitoring"
)

cursor = db.cursor()


@app.route("/")
def home():

    cursor.execute("""
        SELECT temperature, humidity, air_quality, light_intensity, recorded_at
        FROM sensor_environment_full
        ORDER BY id DESC
        LIMIT 1
    """)

    latest_data = cursor.fetchone()

    if latest_data:

        temperature = latest_data[0]
        humidity = latest_data[1]
        air_quality = latest_data[2]
        light_intensity = latest_data[3]
        recorded_at = latest_data[4]

    else:

        temperature = "No data"
        humidity = "No data"
        air_quality = "No data"
        light_intensity = "No data"
        recorded_at = "No data"

    return render_template(
        "index.html",
        temperature=temperature,
        humidity=humidity,
        air_quality=air_quality,
        light_intensity=light_intensity,
        recorded_at=recorded_at
    )


@app.route("/data", methods=["POST"])
def receive_data():

    data = request.get_json()

    temperature = data["temperature"]
    humidity = data["humidity"]
    air_quality = data["air_quality"]
    light_intensity = data["light_intensity"]

    print("Temperature:", temperature, "°C")
    print("Humidity:", humidity, "%")
    print("Air Quality Raw:", air_quality)
    print("Light Intensity Raw:", light_intensity)

    cursor.execute(
        """
        INSERT INTO sensor_environment_full
        (temperature, humidity, air_quality, light_intensity)
        VALUES (?, ?, ?, ?)
        """,
        (temperature, humidity, air_quality, light_intensity)
    )

    db.commit()

    print("Data saved to MariaDB!")

    return "Data received and saved successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)