from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)


# =========================================================
# ANALYZE LIVE SENSOR READINGS
# =========================================================

def calculate_deviation(values):

    values = np.array(values, dtype=float)

    median = np.median(values)

    if median == 0:
        return np.abs(values - median)

    deviation = (
        np.abs(values - median)
        / abs(median)
    ) * 100

    return deviation


def analyze_sensors(sensor_data):

    data = pd.DataFrame(sensor_data)

    data["temperature"] = pd.to_numeric(
        data["temperature"],
        errors="coerce"
    )

    data["humidity"] = pd.to_numeric(
        data["humidity"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["temperature", "humidity"]
    )

    if len(data) == 0:
        return {
            "total": 0,
            "healthy": 0,
            "warning": 0,
            "critical": 0,
            "anomalies": 0,
            "maintenance": 0,
            "sensors": []
        }


    # =====================================================
    # SAME LOGIC AS YOUR PYTHON PROGRAM
    # =====================================================

    temperature_deviation = calculate_deviation(
        data["temperature"].values
    )

    humidity_deviation = calculate_deviation(
        data["humidity"].values
    )


    temperature_tolerance = 25
    humidity_tolerance = 25


    results = []


    for i in range(len(data)):

        temp_abnormal = (
            temperature_deviation[i]
            > temperature_tolerance
        )

        humidity_abnormal = (
            humidity_deviation[i]
            > humidity_tolerance
        )


        # =================================================
        # STATUS
        # =================================================

        if temp_abnormal and humidity_abnormal:

            # Your original program only has
            # NORMAL / ABNORMAL.
            # For the dashboard we classify a sensor
            # abnormal in BOTH parameters as CRITICAL.

            status = "Critical"

        elif temp_abnormal or humidity_abnormal:

            status = "Warning"

        else:

            status = "Normal"


        abnormal_parameters = []

        if temp_abnormal:
            abnormal_parameters.append("Temperature")

        if humidity_abnormal:
            abnormal_parameters.append("Humidity")


        results.append({

            "id": str(data.iloc[i]["machine_id"]),

            "temperature": float(
                data.iloc[i]["temperature"]
            ),

            "humidity": float(
                data.iloc[i]["humidity"]
            ),

            "temperature_deviation": round(
                float(temperature_deviation[i]),
                2
            ),

            "humidity_deviation": round(
                float(humidity_deviation[i]),
                2
            ),

            "status": status,

            "abnormal_parameter":
                ", ".join(abnormal_parameters)
                if abnormal_parameters
                else "-",

            "maintenance":
                status != "Normal"

        })


    # =====================================================
    # DASHBOARD COUNTS
    # =====================================================

    total = len(results)

    healthy = sum(
        1 for r in results
        if r["status"] == "Normal"
    )

    warning = sum(
        1 for r in results
        if r["status"] == "Warning"
    )

    critical = sum(
        1 for r in results
        if r["status"] == "Critical"
    )

    anomalies = sum(
        1 for r in results
        if r["status"] != "Normal"
    )

    maintenance = sum(
        1 for r in results
        if r["maintenance"]
    )


    return {

        "total": total,

        "healthy": healthy,

        "warning": warning,

        "critical": critical,

        "anomalies": anomalies,

        "maintenance": maintenance,

        "sensors": results

    }


# =========================================================
# API
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        body = request.get_json()

        readings = body.get("readings", [])

        result = analyze_sensors(readings)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/", methods=["GET"])
def home():

    return "SmartPredict Live Analysis API is running."


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )