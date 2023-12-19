from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

from pycaret.regression import load_model
from pycaret.regression import predict_model

model = load_model('../../models/model_v1')

app = Flask(__name__)

@app.route('/saludo', methods=['GET'])
def saludo():
    strOut = 'Hola mundo'
    print(strOut)
    return jsonify({'mensaje': strOut})

@app.route('/sumar/', methods= ['GET'])
@app.route('/sumar/<int:a>/<int:b>', methods= ['GET'])
def sumar(a = None, b= None):
    if((a == None) and (b == None)):
        return jsonify({'resultado': 'No se enviaron parametros para operar'})
    else:
        resultado = a+b
        return jsonify({'resultado': resultado})

@app.route('/mul/', methods=['GET'])
def multiplicar():

    try:
        a=int(request.args.get('a',None))
        b=int(request.args.get('b',None))
        resultado = a * b
        return jsonify({'suma':resultado})
    except:
        return jsonify({'resultado':'No se enviaron los parametros para operar.'})  

@app.route('/div/', methods=['POST'])
def division():
    data = request.json
    print(data)
    return jsonify({'mensaje':'ok'})

@app.route('/predictOne/', methods=['POST'])
def predictOne():
    data = request.json
    data_to_predict = pd.json_normalize(data) #convertirmos a dataframe con los tipos de datos default
    try:
        prediction = predict_model(model, data=data_to_predict)
        valor_predicho = round(list(prediction['prediction_label'])[0], 4)

        with open('model_logs.log', 'a') as file_modificado:
            #esribir el contenido modificado en el file
            strLog= f'Predicted_Value: {valor_predicho} - Date: {datetime.now().strftime("%Y-%m-%d %H:%M%S")}\n'
            file_modificado.write(strLog)

        print(valor_predicho)
        return jsonify({'Prediction': valor_predicho})
    
    except:
        with open('model_logs.log', 'a') as file_modificado:
            #esribir el contenido modificado en el file
            strLog= f'Error, at Date: {datetime.now().strftime("%Y-%m-%d %H:%M%S")}\n'
            file_modificado.write(strLog)
        return jsonify({'mensaje': 'Se genero un error en la prediction'})