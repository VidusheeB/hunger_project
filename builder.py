import sys
import argparse
import numpy as np
import pandas as pd
from pytrends.dailydata import convert_dates_to_timeframe
from datetime import datetime
import warnings

# Global options settings
# warnings.filterwarnings("ignore")
pd.set_option('future.no_silent_downcasting', True)

# auxiliary.py
from auxiliary import refresh_pytrends, get_user_agent, get_interest_over_time

# utility.py
from utility import most_current_file, make_date, four_year_daterange, snake_case

# config.py
from config import *

##########
# main.py
##########

def scale_trends(df: pd.DataFrame, previous_column, current_column):
	# Init: Default to 1
	scaling_factor = 1
	print(previous_column, current_column)
	max_value_previous_year = df[previous_column].max()
	date_of_max_value_previous_year = df.loc[df[previous_column].idxmax(), 'date']
	print(f"* Previous Year High: {date_of_max_value_previous_year}")
	
	# then in the following year Y, find the previous year's high and see if there's a scale factor
	max_value_current_year = df[current_column].max()
	date_of_max_value_current_year = df.loc[df[current_column].idxmax(), 'date']
	print(f"* Current Year High: {date_of_max_value_current_year}")
	
	# if the date of the current max value is later than the previous 
	if max_value_previous_year != 0 and date_of_max_value_previous_year < date_of_max_value_current_year:
		scaled_value_of_previous_max_value = (
			df.loc[df['date'] == date_of_max_value_previous_year, previous_column].values[0]
		)
		# Find the previous values in the current year
		current_value_of_previous_max_value = (
			df.loc[df['date'] == date_of_max_value_previous_year, current_column].values[0]
		)
		
		# if the current trend does not have the max value in it - adjust with first value available.
		if np.isnan(current_value_of_previous_max_value):
			print(f"* Previous high not in current trend, using earliest date to scale")
			# Get the first non nan/non 0 date and value
			# first_available_value_date_current_year = df.loc[df[current_column].notna(), 'date'].iloc[0]
			first_available_value_date_current_year = df.loc[(df[current_column] != 0) & (df[current_column].notna()), 'date'].iloc[0]
			first_available_value_current_year = df.loc[df['date'] == first_available_value_date_current_year, current_column].values[0]
			
			# Get the corresponding value using the date in the previous column
			corresponding_value_previous_year = df.loc[df['date'] == first_available_value_date_current_year, previous_column].values[0]
			
			print(first_available_value_date_current_year, first_available_value_current_year, corresponding_value_previous_year)
			scaling_factor = corresponding_value_previous_year / first_available_value_current_year
			print(f"* Scale change: {corresponding_value_previous_year}/{first_available_value_current_year} = {scaling_factor}")
		else:
			scaling_factor = scaled_value_of_previous_max_value / current_value_of_previous_max_value
			print(f"* Scale change: {scaled_value_of_previous_max_value}/{current_value_of_previous_max_value} = {scaling_factor}")
	
	df[current_column] = df[current_column] * scaling_factor
	df[current_column] = df[previous_column].combine_first(df[current_column])
	return df
	

def build_historical_data(keyword: str, start_year: int, end_year: int):
	# Return: for each region, a pandas dataframe with each year as a column
	region_interest = dict()

	# init
	global region_dict
	global topics
	
	# Iterate through the regions
	print("Initial Fetch for ")
	# for region_name, region_code in islice(region_dict.items(), None, 4): #test
	for region_name, region_code in region_dict.items():
		print(f"* {region_name}")
		
		# initialize per region
		interest_over_time = pd.DataFrame()
		interest_by_region = pd.DataFrame()
		got_first = False

		for start_date, end_date in four_year_daterange(start_year, end_year):
			# make the timeframe
			current_timeframe = convert_dates_to_timeframe(start=start_date, stop=end_date)
			current_interest_over_time = get_interest_over_time(keyword, region_code, current_timeframe)
			# Remove partial data
			try:
				if not current_interest_over_time.empty:
					current_interest_over_time = (
						current_interest_over_time[~current_interest_over_time.isPartial]
						.drop(columns=['isPartial'])
						.rename(columns={topics[keyword]: end_date.date()})
					)
				else:
					print(f"No Data for {region_name} in {current_timeframe}")
					continue
			except Exception as e:
				print(current_interest_over_time)
				raise e
			# Add data to dataframe
			if current_interest_over_time.shape[0]>0: # if there's any data
				try:
					if not got_first: # First iteration
						interest_over_time = current_interest_over_time
						got_first = True
					else: # for the rest of the years
						interest_over_time = pd.merge(interest_over_time, current_interest_over_time, on='date', how='outer')
				except Exception as e:
					print('--current--')
					print(current_interest_over_time)
					print('--iot--')
					print(interest_over_time)
					raise e
		region_interest[region_name] = interest_over_time.copy(deep=False)
		# Save the data for reference
		interest_over_time.to_csv(f"{raw_historic_dir / keyword / snake_case(region_name)}.csv", index=False)
		
	# Now we've got the historic data, lets scale it
	for region_name, region_df in region_interest.items():
		print(f"Scaling {region_name}")
		if 'date' not in region_df.columns:
			print(f'No date column in df for {region_name}, {region_df.columns}')
			continue
		df_columns = region_df.set_index('date').columns.tolist()
		df_columns.sort()
		
		for idx in range(0, len(df_columns)-1):
			previous_column = df_columns[idx]
			current_column = df_columns[idx+1]
			region_df = scale_trends(region_df, previous_column, current_column)
		region_df.to_csv(f"{scaled_historic_dir / keyword / snake_case(region_name)}.csv", index=False)
		
		# Get the latest data and save it in current
		current_dir_region = (current_dir / keyword / snake_case(region_name))
		current_dir_region.mkdir(parents=True, exist_ok=True)
		latest_date =  max(list(region_df.set_index('date').columns))
		(region_df[['date', latest_date]]
		 .to_csv(f"{current_dir_region}/{latest_date}.csv", index=False))
	return region_interest


def convert_to_monthly(weekly_df, col):
	weekly_df['date'] = pd.to_datetime(weekly_df['date'])
	# Get current minimum and start it from start of year
	min_date = pd.Timestamp(
		year = weekly_df['date'].min().year, 
		month = 1,
		day = 1
	)
	start_of_year = pd.DataFrame([[min_date, np.nan]], columns=['date', col])
	weekly_df = pd.concat([weekly_df, start_of_year], ignore_index=True)
	weekly_df = weekly_df.set_index('date')
	weekly_df = (
		weekly_df.resample('D').bfill() # make daily and backfill
		.bfill() #twice so that it fills the first NaN we created with start_of_year
	)
	monthly_df = weekly_df.resample('MS').median()
	return monthly_df


def get_latest_data(keyword: str, end_date: datetime):
	# Return: for each region, a pandas dataframe with each year as a column
	region_interest = dict()

	# init
	global region_dict
	global topics
	
	# Iterate through the regions
	print("Fetching Latest for ")
	for region_name, region_code in region_dict.items():
		print(f"* {region_name}")
		
		# initialize per region
		interest_over_time = pd.DataFrame()
		interest_by_region = pd.DataFrame()
		
		# Create a 4 year timeframe
		start_date = datetime(end_date.year - 4, end_date.month, end_date.day)
		current_timeframe = convert_dates_to_timeframe(start=start_date, stop=end_date)
		current_interest_over_time = get_interest_over_time(keyword, region_code, current_timeframe)


		# Remove partial data
		try:
			current_interest_over_time = (
				current_interest_over_time[~current_interest_over_time.isPartial]
				.drop(columns=['isPartial'])
				.rename(columns={topics[keyword]: end_date.date()})
			)
		except Exception as e:
			print(current_interest_over_time)
			raise e
		# Add data to dataframe
		if current_interest_over_time.shape[0]>0: # if there's any data
			region_interest[region_name] = current_interest_over_time.copy(deep=False)
			# Save the data for reference
			current_interest_over_time.to_csv(f"{latest_dir / keyword / snake_case(region_name)}.csv", index=False)
		
	# Now we've got the latest data, lets scale it
	print("Scaling Latest:")
	for region_name, latest_df in region_interest.items():
		print(f"* {region_name}")
		current_dir_region = current_dir/keyword/snake_case(region_name)
		current_df = pd.read_csv(most_current_file(current_dir_region))
		# Adjust types in imported csv
		current_df['date'] = pd.to_datetime(current_df['date'])
		current_df.columns = [make_date(col).date() if col != 'date' else col for col in current_df.columns]

		# if its the already the latest - exit/skip
		if [col for col in current_df.columns if col!='date'][0] == end_date.date():
			print("Already latest")
			continue

		latest_df = pd.merge(current_df, latest_df, on='date', how='outer')
		

		print(f"Scaling {region_name}")
		df_columns = latest_df.set_index('date').columns.tolist()
		df_columns.sort()
		
		for idx in range(0, len(df_columns)-1):
			previous_column = df_columns[idx]
			current_column = df_columns[idx+1]
			scaled_latest_df = scale_trends(latest_df, previous_column, current_column)

		latest_date = max(list(scaled_latest_df.set_index('date').columns))
		print(f"{current_dir_region}/{latest_date}.csv")
		(
			scaled_latest_df[['date', latest_date]]
			.to_csv(f"{current_dir_region}/{latest_date}.csv", index=False, mode='w')
		)

		# monthly_df.to_csv(f"{monthly_dir}/{snake_case(region_name)}.csv", index=False, mode='w')

	return "Complete"


def convert_to_monthly(weekly_df, col):
    weekly_df['date'] = pd.to_datetime(weekly_df['date'])
    # Get current minimum and start it from start of year
    min_date = pd.Timestamp(
        year = weekly_df['date'].min().year, 
        month = 1,
        day = 1
    )
    start_of_year = pd.DataFrame([[min_date, np.nan]], columns=['date', col])
    weekly_df = pd.concat([weekly_df, start_of_year], ignore_index=True)
    weekly_df = weekly_df.set_index('date')
    weekly_df = (
        weekly_df.resample('D').bfill() # make daily and backfill
        .bfill() #twice so that it fills the first NaN we created with start_of_year
    )
    monthly_df = weekly_df.resample('MS').median()
    return monthly_df

def create_metro_county_monthly_data():
    county_df = {}
    keywords = [file for file in current_dir.glob('*') if file and not file.name.startswith('.')]
    for keyword in keywords:
        keyword_path = current_dir/keyword
        counties = [file for file in keyword_path.glob('*') if file and not file.name.startswith('.')]
        log = False
        for county in counties:
            max_filepath = max([file for file in county.glob('*') if file and not file.name.startswith('.')])
            col = max_filepath.name.strip('.csv')
            df = pd.read_csv(max_filepath)
            monthly_df = convert_to_monthly(df, col)
            monthly_df = monthly_df.rename(columns={col: keyword.stem})
            if county.stem not in county_df:
                county_df[county.stem] = monthly_df.copy()
            else:
                county_df[county.stem] = pd.merge(
                    county_df[county.stem], monthly_df, 
                    left_index=True, right_index=True, how='outer', 
                )

    dfs = []
    for county, df in county_df.items():
        df.columns = [f'gTrend_{col}' for col in df.columns]
        df['month'] = df.index.month
        df['year'] = df.index.year
        df['CountyName'] = county
        df['State'] = county.split(' ')[-1].upper()
        dfs.append(df)
        # df.round(2).to_csv(f'{monthly_dir}/{county}.csv')

    # Concatenate all DataFrames into a single DataFrame
    final_df = pd.concat(dfs, ignore_index=True)
    return final_df


if __name__ == "__main__":
	
	current_year = datetime.now().year
	parser = argparse.ArgumentParser()
	parser.add_argument("--historical", action='store_true', help="Flag for historical data")
	parser.add_argument("--monthly", action='store_true', help="Flag for monthly data")
	parser.add_argument("--start_year", type=int, help="Start year for historical data")
	parser.add_argument("--end_year", type=int, default=current_year - 1 , help="End year for historical data")
	
	# Adding an optional string argument "keyword"
	parser.add_argument("--keyword", type=str, help="Keyword for filtering data (optional)")

	args = parser.parse_args()

	if args.historical:
		if args.start_year and args.end_year:

			if args.keyword:
				print(f"Building Historical dataset for {args.keyword}")
				build_historical_data(keyword= args.keyword, start_year=args.start_year, end_year=args.end_year)

			else:

				print("All topics")
				if input("Buidlding for all topics since keyword not specified. Continue? Y/N: ").strip().upper() == 'Y':
					for topic in topics.keys():
						print(f"Building Historical dataset for {topic}")
						build_historical_data(keyword= topic, start_year=args.start_year, end_year=args.end_year)
				else:
					print("Operation canceled by the user.")
					sys.exit() 

		else:
			print("Please specify both start_year and end_year for historical data.")
	elif args.monthly:
		print("Creating monthly")
		create_metro_county_monthly_data()
	else:
		print("No Arguments passed. Use --help to learn more.")
