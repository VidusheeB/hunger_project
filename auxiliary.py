import time
import pandas as pd
from pytrends.request import TrendReq
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from config import *

def get_user_agent():
	# Since Google keeps timing us out, we generate fake user_agents to avoid 429 TooManyRequestsError
	software_names = [SoftwareName.CHROME.value]
	operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
	user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
	
	# Get Random User Agent String.
	return user_agent_rotator.get_random_user_agent()


def refresh_pytrends():
	# Recreate a pytrends object with the new user agent 
	requests_args = {
		'headers': {
			#'User-Agent': get_user_agent()
		},
		'verify':False
	}
	# pytrends = TrendReq(
	# 	hl='en-US', 
	# 	tz=360, 
	# 	timeout=(10,25),
	# 	retries=2, 
	# 	backoff_factor=0.1, 
	# 	requests_args=requests_args
	# )
	# Set global object value with new user agent
	pytrends = TrendReq(hl='en-US', tz=360, requests_args=requests_args)
	return pytrends

def get_interest_over_time(keyword, region_code, current_timeframe):
	current_interest_over_time = pd.DataFrame()
	got_data = False
	retries = 0
	while not got_data and retries < 5:
		# Build the payload - this applies to all requests being sent!
		pytrends = refresh_pytrends()
		pytrends.build_payload(
			kw_list=[topics[keyword]],
			cat = 0, #Default Category type - do we want to change this? Check with this: pytrends.categories()
			geo=region_code, #this changes to each region, etc.
			timeframe=current_timeframe
		)

		# Send Requests
		current_interest_over_time = pytrends.interest_over_time().reset_index()
		if not current_interest_over_time.empty:
			got_data = True
		else: 
			print("Retrying")
		retries += 1
	return current_interest_over_time
