from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model
model_ann = load_model('predictor.h5')

def temperatur_to_cond(temp):
    if temp < 30:
        return 0
    elif 30 <= temp <= 33:
        return 1
    elif 34 <= temp <= 35:
        return 2
    else:
        return 3

def kelembaban_to_cond(humidity):
    if humidity > 80:
        return 0
    elif 61 <= humidity <= 80:
        return 1
    elif 41 <= humidity <= 60:
        return 2
    else:
        return 3

def water_level_to_cond(water_level):
    if water_level < 30:
        return 0
    elif 31 <= water_level <= 39:
        return 1
    elif 41 <= water_level <= 49:
        return 2
    else:
        return 3

def predict_condition(temperatur, kelembaban, ketinggian_air):
    # Mengubah input menjadi kondisi sesuai dengan batasan yang ditetapkan
    temperatur_cond = temperatur_to_cond(temperatur)
    kelembaban_cond = kelembaban_to_cond(kelembaban)
    water_level_cond = water_level_to_cond(ketinggian_air)

    # Membuat array dari input
    input_data = np.array([[temperatur_cond, kelembaban_cond, water_level_cond]])

    # Prediksi menggunakan model ANN
    pred_ann = np.argmax(model_ann.predict(input_data), axis=-1)[0]

    # Mengonversi prediksi menjadi tipe data int
    pred_ann = int(pred_ann)

    return pred_ann

@app.route('/predict', methods=['POST'])
def predict():
    # Ambil data input dari POST request
    input_data = request.get_json()

    # Lakukan prediksi berdasarkan input yang diberikan
    temperatur = input_data['temperatur']
    kelembaban = input_data['kelembaban']
    ketinggian_air = input_data['ketinggian_air']
    prediction = predict_condition(temperatur, kelembaban, ketinggian_air)

    # Mengembalikan hasil prediksi dalam bentuk JSON
    response = jsonify({'prediksi': prediction})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')  
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')  
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
