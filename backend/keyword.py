import requests
import csv
import inspect
import pandas as pd
import numpy as np
import pgeocode
from dotenv import load_dotenv

import os

load_dotenv()

BING_API_KEY = os.environ.get("BING_API_KEY")
geo = pgeocode.Nominatim('us')

class KeywordSingleton:
	_instance = None
	

	def __init__():
		raise RuntimeError("Call instance() instead")

	@classmethod
	def instance(cls):
     
		if cls._instance is None:
			print('Creating new instance of KeywordSingleton')
			cls._instance = cls.__new__(cls)
	
		print("Returning instance of KeywordSingleton")
		return cls._instance

	def get_lat_long(self, zip_code):
		info = geo.query_postal_code(zip_code)
		lat = info["latitude"]
		lon = info["longitude"]
		return str(lat)+","+str(lon)
	
	
	def get_url_data(self, keyword, zip_code):
		query = """"{}" {}""".format(keyword, zip_code)
		latlon = self.get_lat_long(zip_code)
		url = "https://dev.virtualearth.net/REST/v1/LocalSearch/?query={}&userLocation={}&key={}".format(query, latlon, BING_API_KEY)
		
		while True:
			try:
				response = requests.get(url).json()
				data = response["resourceSets"][0]["resources"]
				results = []
				for i in data:
					name = i["name"]
					address = i["Address"]["formattedAddress"]
					phonenum = i["PhoneNumber"]
					website = i["Website"]
					if zip_code in address:
						results.append([zip_code,name,address,phonenum,website])
				return results
			except:
				print("stuck", keyword, zip_code)
				continue
	def get_data(self, zip_codes, keywords):
		results=[]
		for i in zip_codes:
			for j in keywords:
				results += self.get_url_data(j, i)
		new_df = pd.DataFrame(columns=["Zipcode","Name","Address","Phone","Website"], data=results)
		new_df = new_df.drop_duplicates(subset=["Zipcode","Name","Address","Phone","Website"])
		pivot = pd.pivot_table(new_df, values='Name', index='Zipcode', aggfunc='count')
		col_name = 'Total Number of Businesses ({})'.format(', '.join(keywords))
		pivot = pivot.rename(columns={'Name': col_name})
		pivot.loc['TOTAL']= pivot.sum(numeric_only=True, axis=0)
		return new_df, pivot