import requests
import csv
import inspect
import pandas as pd
from dotenv import load_dotenv
import os
import sys
import pgeocode

# setting path
sys.path.append('../static_data')
# from static_data.demo_data import data
load_dotenv()

CENSUS_API_KEY = os.environ.get("CENSUS_API_KEY")
geo = pgeocode.Nominatim('us')

class DemographicsSingleton:
	_instance = None
 
	d = {
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

	def __init__():
		raise RuntimeError("Call instance() instead")

	@classmethod
	def instance(cls):
		if cls._instance is None:
			print('Creating new instance')
			cls._instance = cls.__new__(cls)
			
			cls.data_tbles={}
			for i in cls.d.keys():
				cls.data_tbles[i]=[]
			# results=[]
			for i in cls.d.keys():
				url = "https://api.census.gov/data/2021/acs/acs5?get=NAME,{}&for=zip%20code%20tabulation%20area:*&key={}".format(cls.d[i],CENSUS_API_KEY)
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
					# import pdb
					# pdb.set_trace()
					data[j[0][-5:]]=float(j[1])
				cls.data_tbles[i] = data
		print("Returning instance")
		return cls._instance

	@classmethod
	def get_data(cls, zipcode):
		i = zipcode
		z = geo.query_postal_code(i)
  
		while True:
			try:
				answer = {
					"Zip Code": i,
					"Population": cls.data_tbles["population"][i],
					"Children Age 0-5 Years": cls.data_tbles["under_5_male"][i]+cls.data_tbles["under_5_female"][i],
					"Children Age 5-9 Years": cls.data_tbles["male_5_9"][i]+cls.data_tbles["female_5_9"][i],
					"Percentage of children (%)": round(100*(cls.data_tbles["under_5_male"][i]+cls.data_tbles["under_5_female"][i]+cls.data_tbles["male_5_9"][i]+cls.data_tbles["female_5_9"][i])/cls.data_tbles["population"][i],2),
					"Total Households": cls.data_tbles["total_households"][i],
					"Median Household Income ($)": cls.data_tbles["median_income"][i],
					"Median Housing Value ($)": cls.data_tbles["median_housing_val"][i],
					"College Degree (%)": round(100*((cls.data_tbles["college_1"][i]+cls.data_tbles["college_2"][i]+cls.data_tbles["college_3"][i]+cls.data_tbles["college_4"][i]+cls.data_tbles["college_5"][i])/ cls.data_tbles["older_25_pop"][i]),2),
					"Median Age": cls.data_tbles["median_age"][i],
					"Renter Occupied (%)": round(100*(cls.data_tbles["renter_occupied"][i]/cls.data_tbles["total_occupied"][i]),2),
					"Unemployment Rate (%)": round(100*(cls.data_tbles["unemployment"][i]/cls.data_tbles["workforce"][i]),2),
					"White (%)": round(100*(cls.data_tbles["white"][i]/cls.data_tbles["population"][i]),2),
					"Black (%)": round(100*(cls.data_tbles["black"][i]/cls.data_tbles["population"][i]),2),
					"American Indian (%)": round(100*(cls.data_tbles["native"][i]/cls.data_tbles["population"][i]),2),
					"Asian (%)": round(100*(cls.data_tbles["asian"][i]/cls.data_tbles["population"][i]),2),
					"Islander (%)": round(100*(cls.data_tbles["islander"][i]/cls.data_tbles["population"][i]),2),
					"Other (%)": round(100*(cls.data_tbles["other"][i]/cls.data_tbles["population"][i]),2),
					"Two or More (%)": round(100*(cls.data_tbles["two_more"][i]/cls.data_tbles["population"][i]),2),
					"City": z.place_name,
					"County": z.county_name
					}
				return answer
			except:
				
				print("stuck in get_data")
				continue

	@classmethod
	def get_all_data(cls, zipcodes):
		results = []
		for i in zipcodes:
			results.append(cls.get_data(i))
		df = pd.DataFrame(results)
		return df
