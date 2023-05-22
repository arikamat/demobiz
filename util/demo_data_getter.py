import requests
import csv
from uszipcode import SearchEngine
search = SearchEngine()
from dotenv import load_dotenv

import os

load_dotenv()

CENSUS_API_KEY = os.environ.get("CENSUS_API_KEY")

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
data_tbles={}
for i in d.keys():
    data_tbles[i]=[]
results=[]
for i in d.keys():
	url = "https://api.census.gov/data/2021/acs/acs5?get=NAME,{}&for=zip%20code%20tabulation%20area:*&key={}".format(d[i],CENSUS_API_KEY)
	response = requests.get(url)
	lst = response.json()
	data = {}
	for j in lst[1:]:
		# import pdb
		# pdb.set_trace()
		data[j[0][-5:]]=float(j[1])
	data_tbles[i] = data
f = open("../static_data/demo_data.py", "w")
print("data = ", data_tbles, file=f)
f.close()