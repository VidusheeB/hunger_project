# hunger_trends
Using pytrends to fetch latest data on hunger keywords. Also includes a scaling function since numbers are always normalized to 100.

Currently the script is all in one monolith. It can be run in python as follows:

```python
from main import *

start_year = 2018
end_year = 2024 #ends 2023
for keyword in topics:
    print("*"*10)
    print(keyword)
    print("*"*10)
    # Run build historic only once
    build_historical_data(keyword, start_year, end_year)
    # get latest, gets today's data and scales it to historic
    get_latest_data(keyword,datetime.today())
    
    # TODO: get monthly and put into latest
```

The script on import will create folders by default in `~/Desktop/trends_data` and that can be changed in the script.

## Data

I've attached the data here in this repo under `trends_data/`
Each folder will have a subfolder for each topic.
Here's the folder definition:

* raw_historic: This includes the raw extract for the first time this code runs. Currently it includes data from 2018 to 2023.
* scaled_historic: This takes the raw_historic data and scales it across different years.
* latest: This is the latest data we get from a single run. A single run will include 4 years worth of data in a single pull.
* current: This is what we'll be using. Per topic, there are subfolders per territory. Each territory, we will use the highest date's data to power our regression/dashboard. For example: `trends_data/current/CalFresh/austin_tx/2024-02-16` is the final output data for Feb 16th including all historic data and scaled at a weekly cadence.

## TODO:
- [ ] Add monthly aggregation. Currently in weekly state. 
- [ ] Modularize code
- [ ] Add more documentation
