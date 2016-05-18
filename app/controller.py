from app import app
from flask import render_template, flash, redirect, session, url_for, request, g , Response, Flask
from werkzeug import secure_filename
import os

from models.SentimentalModel import *

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/') #Mejor redirigir que mantener todo bajo una sola funcion
def home():
	return redirect(url_for('index'))

@app.route('/index',methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/train', methods=['GET'])
def train():
	modelo = SentimentalModel()
	return Response(status = 200)
	
@app.route('/upload',methods=['POST'])
def upload_data():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)

			modelo = SentimentalModel()

			file.save(os.path.join(app.config['DATA_FOLDER'], filename))

			modelo.setFileData(filename)

			return redirect(url_for('study'))

@app.route('/exploratory',methods=['GET'])
def exploratory():
	modelo = SentimentalModel()
	res = modelo.getExploratory()
	return Response(res,status=200)

@app.route('/preprocessing',methods=['GET'])
def preprocessing():
	modelo = SentimentalModel()
	res = modelo.getPreprocessing()
	return Response(res,status=200)

@app.route('/results',methods=['GET'])
def results():
	modelo = SentimentalModel()
	res = modelo.getResults()
	return Response(res,status=200)

@app.route('/test_file', methods=['GET'])
def test_file():
	modelo = SentimentalModel()
	if modelo.testFileData() == True:
		return Response(status = 200)

@app.route('/test_review', methods=['POST'])
def test_review():
	modelo = SentimentalModel()
	if request.method == 'POST':
		review = request.form['review']
		
		if modelo.testReview(review)  == True:
			return Response(status = 200)

@app.route('/study', methods=['GET'])
def study():
	return render_template('case.html')

