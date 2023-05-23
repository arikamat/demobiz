import requests
import csv
import inspect
import pandas as pd
from dotenv import load_dotenv
import os
import sys
import pgeocode

load_dotenv()

CENSUS_API_KEY = os.environ.get("CENSUS_API_KEY")
geo = pgeocode.Nominatim('us')

class Demographics:	

	def __init__(self, zipcodes):
		self.d = {
		"population": "B01001_001E",
		"under_5_male": "B01001_003E",
		"under_5_female": "B01001_027E",
		"male_5_9": "B01001_004E",
		"female_5_9": "B01001_028E",
		"total_households": "B11016_001E",
		"median_income": "B19013_001E",
		"median_housing_val": "B25077_001E",
		"college_1": "B15003_021E",
		"college_2": "B15003_022E",
		"college_3": "B15003_023E",
		"college_4": "B15003_024E",
		"college_5": "B15003_025E",
		"older_25_pop": "B15003_001E",
		"median_age": "B01002_001E",
		"renter_occupied": "B25003_003E",
		"total_occupied": "B25003_001E",
		"unemployment": "B23025_005E",
		"workforce": "B23025_002E",
		"white": "B02001_002E",
		"black": "B02001_003E",
		"native": "B02001_004E",
		"asian": "B02001_005E",
		"islander": "B02001_006E",
		"other": "B02001_007E",
		"two_more": "B02001_008E",
	}
		zipcode_query = ','.join(zipcodes)
		self.data_tbles={}
		self.zip_codes=[]
		for i in self.d.keys():
			self.data_tbles[i]=[]
		for i in self.d.keys():
			url = "https://api.census.gov/data/2021/acs/acs5?get=NAME,{}&for=zip%20code%20tabulation%20area:{}&key={}".format(self.d[i],zipcode_query,CENSUS_API_KEY)
			print(url)
			while True:
				try:
					response = requests.get(url)
					lst = response.json()
					break
				except:
					continue
			data = {}
			for j in lst[1:]:
				zc = j[0][-5:]
				data[zc]=float(j[1])
				self.zip_codes.append(zc)
			self.data_tbles[i] = data

	def get_data(self, zipcode):
		i = zipcode
		z = geo.query_postal_code(i)
  
		while True:
			try:
				answer = {
					"Zip Code": i,
					"Population": self.data_tbles["population"][i],
					"Children Age 0-5 Years": self.data_tbles["under_5_male"][i]+self.data_tbles["under_5_female"][i],
					"Children Age 5-9 Years": self.data_tbles["male_5_9"][i]+self.data_tbles["female_5_9"][i],
					"Percentage of children (%)": round(100*(self.data_tbles["under_5_male"][i]+self.data_tbles["under_5_female"][i]+self.data_tbles["male_5_9"][i]+self.data_tbles["female_5_9"][i])/self.data_tbles["population"][i],2),
					"Total Households": self.data_tbles["total_households"][i],
					"Median Household Income ($)": self.data_tbles["median_income"][i],
					"Median Housing Value ($)": self.data_tbles["median_housing_val"][i],
					"College Degree (%)": round(100*((self.data_tbles["college_1"][i]+self.data_tbles["college_2"][i]+self.data_tbles["college_3"][i]+self.data_tbles["college_4"][i]+self.data_tbles["college_5"][i])/ self.data_tbles["older_25_pop"][i]),2),
					"Median Age": self.data_tbles["median_age"][i],
					"Renter Occupied (%)": round(100*(self.data_tbles["renter_occupied"][i]/self.data_tbles["total_occupied"][i]),2),
					"Unemployment Rate (%)": round(100*(self.data_tbles["unemployment"][i]/self.data_tbles["workforce"][i]),2),
					"White (%)": round(100*(self.data_tbles["white"][i]/self.data_tbles["population"][i]),2),
					"Black (%)": round(100*(self.data_tbles["black"][i]/self.data_tbles["population"][i]),2),
					"American Indian (%)": round(100*(self.data_tbles["native"][i]/self.data_tbles["population"][i]),2),
					"Asian (%)": round(100*(self.data_tbles["asian"][i]/self.data_tbles["population"][i]),2),
					"Islander (%)": round(100*(self.data_tbles["islander"][i]/self.data_tbles["population"][i]),2),
					"Other (%)": round(100*(self.data_tbles["other"][i]/self.data_tbles["population"][i]),2),
					"Two or More (%)": round(100*(self.data_tbles["two_more"][i]/self.data_tbles["population"][i]),2),
					"City": z.place_name,
					"County": z.county_name
					}
				return answer
			except:
				# import pdb
				# pdb.set_trace()
				print("stuck in get_data")
				continue

	
	def get_all_data(self):
		results = []
		for i in self.zip_codes:
			results.append(self.get_data(i))
		df = pd.DataFrame(results)
		return df

	def __del__(self):
		del self.data_tbles
		del self.zip_codes
		del self.d
