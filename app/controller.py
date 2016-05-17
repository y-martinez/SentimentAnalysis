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
	#modelo = SentimentalModel()
	return Response(status = 202)
	
@app.route('/upload',methods=['POST'])
def upload_data():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['DATA_FOLDER'], filename))
			return redirect(url_for('study_case'))
	

@app.route('/study_case', methods=['GET'])
def classify():
	return render_template('case.html')

