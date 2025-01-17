from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.pred_pipeline import CustomData, PredictPipline
from src.pipeline.training_pipeline import Training_pipeline

application = Flask(__name__)

app=application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_data', methods = ("GET", 'POST'))
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score')),
        )

        custom_df = data.get_data_as_dataframe()
        print(custom_df)
        
        predict_pipeline = PredictPipline()
        results = predict_pipeline.predict(custom_df)
        return render_template ('home.html', result = results[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0")