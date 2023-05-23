from flask import Flask,render_template, request
from flask_celery import make_celery
from backend.demo import Demographics
from backend.email import Emailer
from backend.keyword import KeywordSingleton
import re
from dotenv import load_dotenv

import os

load_dotenv()

BROKER_URL = os.environ.get("REDIS_URL")


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = BROKER_URL
celery = make_celery(app)



@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
	zc = request.form['zipCodes']
	kee = request.form['keywords']
	email = request.form['email']
	zip_codes = zc.split('\n')
	for i in range(len(zip_codes)):
		zip_codes[i] = zip_codes[i].strip()
	keywords = kee.split('\n')
	for i in range(len(keywords)):
		keywords[i] = keywords[i].strip()
	get_all_data_send_email.delay(zip_codes, keywords, email)
	print(zip_codes, kee, email)
	return render_template('successful_parser.html')

@celery.task(name='get_all_data_send_email')
def get_all_data_send_email(zip_codes, keywords, email):
	print("hereeeeeee 0")
	demographics = Demographics(zip_codes)
	demographics_data = demographics.get_all_data()
	print("heeereeeeeee 1")
	k = KeywordSingleton.instance()
	k_data = k.get_data(zip_codes, keywords)
	k_data_simple = k_data[0]
	k_piv = k_data[1]
	print("hereeeeeee 2")
	emailer = Emailer.instance()
	print("hereeeeeee 3")
	emailer.send_email_2_df(email, "Your Franchise Data", k_data_simple, k_piv, demographics_data)
	print("hereeeeeee 4")
	del demographics
	del k_data_simple
	del k_piv
	del k_data
if __name__ == '__main__':
	app.run(debug=True, use_reloader=False)