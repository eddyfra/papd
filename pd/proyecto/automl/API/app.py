from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

from pycaret.regression import load_model
from pycaret.regression import predict_model

rf_model = load_model('../models/model_v1')
dt_model = load_model('../models/model_v2')
et_model = load_model('../models/model_v3')

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def saludo():
    try:
        a = request.args.get('a',None)
        strOut = "Hola mundo: {a}"
        return jsonify({'mensaje': strOut})
    except:
        return jsonify({'resultado':'No se enviaron los parametros para operar.'})

@app.route('/predict_rf/', methods=['POST'])
def predict_rf():
    data = request.json
    data_to_predict = pd.json_normalize(data) #convertirmos a dataframe con los tipos de datos default
    try:
        prediction = predict_model(rf_model, data=data_to_predict)
        valor_predicho = round(list(prediction['prediction_label'])[0], 4)

        with open('model_logs.log', 'a') as file_modificado:
            #esribir el contenido modificado en el file
            strLog= f'Modelo: {rf_model} - Predicted_Value: {valor_predicho} - Date: {datetime.now().strftime("%Y-%m-%d %H:%M%S")}\n'
            file_modificado.write(strLog)

        print(valor_predicho)
        return jsonify({'Prediction': valor_predicho})
    
    except:
        with open('model_logs.log', 'a') as file_modificado:
            #esribir el contenido modificado en el file
            strLog= f'Error, at Date: {datetime.now().strftime("%Y-%m-%d %H:%M%S")}, at model: {rf_model}\n'
            file_modificado.write(strLog)
        return jsonify({'mensaje': 'Se genero un error en la prediction'})