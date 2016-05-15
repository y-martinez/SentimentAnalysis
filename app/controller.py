from app import app
from flask import render_template, flash, redirect, session, url_for, request, g ,Flask


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/') #Mejor redirigir que mantener todo bajo una sola funcion
def home():
	return redirect(url_for('index'))

@app.route('/index',methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/upload',methods=['GET', 'POST'])
def upload_data():
	if request.method == 'POST':
		print "hey"