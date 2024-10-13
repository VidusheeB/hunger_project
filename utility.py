from datetime import datetime

def snake_case(s):
    # # Creating problems downstream, remove late
    return s

def most_current_file(current_dir_region):
    max_date = None
    max_file_path = None
    
    # Iterate over files in the directory
    for file_path in current_dir_region.glob('*.csv'):
        # Extract the date from the file name
        file_date_str = file_path.stem
        try:
            file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
        except ValueError:
            continue  # Skip files with invalid date format
        
        # Update max_date and max_file_path if the current file date is higher
        if max_date is None or file_date > max_date:
            max_date = file_date
            max_file_path = file_path
    
    return max_file_path

def make_date(dateString, ft = '%Y-%m-%d'):
    # convert string to date
    return datetime.strptime(dateString, ft)

def four_year_daterange(start_year, end_year):
    # given a start and end year, generate a range in 4 year periods 
    # 4 year period is chosen because google trends beyond 4 years, doesn't give back weekly data points
    # after 4 years, google trends gives yearly trends
    # this is the make sure we always get the same duration between data points to compare
    starting_year = start_year
    for year in range(start_year+1, end_year):
        if year - starting_year >=4:
            starting_year +=1
        yield(datetime(starting_year,1,1), datetime(year, 1,1))

