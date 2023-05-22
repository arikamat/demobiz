import requests
import csv
import inspect
from uszipcode import SearchEngine
import pandas as pd
import numpy as np
import pgeocode
from dotenv import load_dotenv

import os

load_dotenv()

BING_API_KEY = os.environ.get("BING_API_KEY")
geo = pgeocode.Nominatim('fr')

class KeywordSingleton:
	_instance = None
	

	def __init__():
		raise RuntimeError("Call instance() instead")

	@classmethod
	def instance(cls):
		print("hereeeeeeeeeeeeeeeeeeee")
		curframe = inspect.currentframe()
		calframe = inspect.getouterframes(curframe, 2)
		print('caller name:', calframe[1][3])
		if cls._instance is None:
			print('Creating new instance')
			cls._instance = cls.__new__(cls)
			# Put any initialization here.
	
		print("Returning instance")
		return cls._instance

	def get_lat_long(self, zip_code):
		
	
	
	def get_url_data(self, keyword, zip_code):
		query = """"{}" {}""".format(keyword, zip_code)
		latlon = self.get_lat_long(zip_code)
		url = "https://dev.virtualearth.net/REST/v1/LocalSearch/?query={}&userLocation={}&key={}".format(query, latlon, BING_API_KEY)
		status = False
		while not status:
			try:
				response = requests.get(url).json()
				status = True
			except:
				print("stuck", keyword, zip_code)
				continue
		try:
			data = response["resourceSets"][0]["resources"]
			results = []
			for i in data:
				name = i["name"]
				address = i["Address"]["formattedAddress"]
				phonenum = i["PhoneNumber"]
				website = i["Website"]
				if zip_code in address:
					results.append([zip_code,name,address,phonenum,website,keyword,query])
		except:
			print("stuck in url_data")
		return results
	def get_data(self, zip_codes, keywords):
		results=[]
		for i in zip_codes:
			for j in keywords:
				results += self.get_url_data(j, i)
		new_df = pd.DataFrame(columns=["Zipcode","Name","Address","Phone","Website","Keyword","Query"], data=results)
		new_df = new_df.drop_duplicates(subset=["Zipcode","Name","Address","Phone","Website"])
		pivot = pd.pivot_table(new_df, values='Name', index='Zipcode', aggfunc='count')
		pivot = pivot.rename(columns={'Name': 'Number of Businesses'})
		return new_df, pivot