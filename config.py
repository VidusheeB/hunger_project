
from pathlib import Path

# main directory to save data
home = Path.home()
main_directory = home / 'github/hunger_trends/trends_data'

# Subdirectories
raw_historic_dir = main_directory / 'raw_historic'
scaled_historic_dir = main_directory / 'scaled_historic'
current_dir = main_directory / 'current'
latest_dir = main_directory / 'latest'
monthly_dir = main_directory / 'monthly'

# if adding new directory above, add it below so it can create accordingly
# to make above directories if they don't exist
main_directory.mkdir(parents=True, exist_ok=True)
raw_historic_dir.mkdir(parents=True, exist_ok=True)
scaled_historic_dir.mkdir(parents=True, exist_ok=True)
current_dir.mkdir(parents=True, exist_ok=True)
latest_dir.mkdir(parents=True, exist_ok=True)
monthly_dir.mkdir(parents=True, exist_ok=True)

all_subdirectories = [raw_historic_dir, scaled_historic_dir, current_dir, latest_dir]

#Topics found so far
topics = {
	"Supplemntal Nutrition Assistance Program": "/m/030gj7",
	"CalFresh": "/m/0ngtw90" ,
	"Food Stamps": "/g/1tdb024s",
	"food assistance": "/g/11bc69n54b",
	"Food bank": "/m/059plx",
	"Electronic Benefit Transfer": "/m/030g_2",
	"Soup kitchen": "/m/02p1bc"
}

# creates topic directories in each subdirectory
for subdirectories in all_subdirectories:
	for topic_name in topics:
		(subdirectories / topic_name).mkdir(parents=True, exist_ok=True)


# This is the output of the above cell
region_dict = {
    'Abilene-Sweetwater TX': 'US-TX-662',
    'Amarillo TX': 'US-TX-634',
    'Austin TX': 'US-TX-635',
    'Bakersfield CA': 'US-CA-800',
    'Beaumont-Port Arthur TX': 'US-TX-692',
    'Chico-Redding CA': 'US-CA-868',
    'Corpus Christi TX': 'US-TX-600',
    'Dallas-Ft. Worth TX': 'US-TX-623',
    'El Paso TX': 'US-TX-765',
    'Eureka CA': 'US-CA-802',
    'Fresno-Visalia CA': 'US-CA-866',
    'Harlingen-Weslaco-Brownsville-McAllen TX': 'US-TX-636',
    'Houston TX': 'US-TX-618',
    'Laredo TX': 'US-TX-749',
    'Los Angeles CA': 'US-CA-803',
    'Lubbock TX': 'US-TX-651',
    'Monterey-Salinas CA': 'US-CA-828',
    'Odessa-Midland TX': 'US-TX-633',
    'Palm Springs CA': 'US-CA-804',
    'Sacramento-Stockton-Modesto CA': 'US-CA-862',
    'San Angelo TX': 'US-TX-661',
    'San Antonio TX': 'US-TX-641',
    'San Diego CA': 'US-CA-825',
    'San Francisco-Oakland-San Jose CA': 'US-CA-807',
    'Santa Barbara-Santa Maria-San Luis Obispo CA': 'US-CA-855',
    'Tyler-Longview(Lufkin & Nacogdoches) TX': 'US-TX-709',
    'Victoria TX': 'US-TX-626',
    'Waco-Temple-Bryan TX': 'US-TX-625',
    'Yuma AZ-El Centro CA': 'US-CA-771'
}