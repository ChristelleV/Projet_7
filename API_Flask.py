from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pandas as pd
import pickle as p
import json


app = Flask(__name__)


@app.route('/api/', methods=['POST'])
def makecalc():
    data = request.get_json()
    print(data)
    print(type(data))
    data_df = pd.read_json(data, orient='split')
    prediction = np.array2string(model.predict(data_df.to_numpy().reshape(1, -1)))
    return jsonify(prediction)


if __name__ == '__main__':
    modelfile = 'final_prediction.pickle'
    model = p.load(open(modelfile, 'rb'))
    app.run(host='127.0.0.1', port=5000)
