from database.db_connect import drop_db, create_db, add_user_and_passw, get_user_and_passw 
from flask import Flask, render_template, request, jsonify, current_app, g
from flask.cli import with_appcontext
import sqlite3
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import KNeighborsClassifier
from collections import Counter
from sklearn.metrics import accuracy_score
import pickle
import glob
import csv
import numpy as np
import pandas as pd
import os

BIOMETRIA_PATH = '../sdk_lib/sdk/biometrias/' # Pasta onde será salvo os dados .csv
create_db() # Cria o banco de dados SQLite

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('login.html')

@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
	if request.method == 'GET':
		return render_template('./cadastro/cadastro.html')
	elif request.method == 'POST':
		response = dict(request.get_json())
		username  = response['username']
		password = response['password']
		id, result = add_user_and_passw(username, password)

		if result:
			return jsonify({'cadastro_cod': 'UserRegistrySuccess', 'id_usuario': id})
		else:
			return jsonify({'cadastro_cod': 'UsernameAlreadyExist'})


@app.route('/cadastro/biometria', methods = ['POST'])
def biometria():
	if request.method == 'POST':
		response = dict(request.get_json())
		user_id  = response['user_id']
		data = response['data']
		dataframe = pd.DataFrame(data)
		path = BIOMETRIA_PATH + str(user_id) + ".csv"
		try: 
			dataframe.to_csv(path, header=False, index=False)
			return jsonify({'biometric_cod': 'Success'})
		except:
			print("Não foi possivel gerar o arquivo .csv")



# Server Start
if __name__ == '__main__':
	app.run(host='127.0.0.1', debug=True, port=3000)
