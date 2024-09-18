# LSEG Task - Engineer - TechChallenge2
# Daniel Patrascu

# For each stock exchange, select the specified number of files, 
# and for each file provided, predict the next 3 values of stock price for that specific file.

import csv
import os
import random
from datetime import datetime, timedelta

INPUT_FOLDER    = "./Input"
OUTPUT_FOLDER   = "./Output"

NAME_INDEX      = 0
TIMESTAMP_INDEX = 1
PRICE_INDEX     = 2


def function_one(csv_file: str, sample_size: int = 10) ->list[str]:
    '''
    1st API/Function that, for each file provided, returns 10 consecutive data points 
    starting from a random timestamp.

    Parameters:
                csv_file    (str)       :   Name of the CSV File that containt the necessary data
                sample_size (int)       :   Number of data points (rows) that are pulled from the input file
                                            Default = 10

    Returns:
                data_points (list[str]) :   List of strings that contains the sampled data
    '''

    data_points = []
    
    try:
        with open(csv_file) as file:
            csv_reader = csv.reader(file)
            csv_data = list(csv_reader)

            # Get the total number of data points
            data_size: int = len(csv_data)

            try:
                if (data_size < sample_size):
                    raise ValueError("Not enough data")
            
                # Generate a random number for selecting a data point
                # Substract the target number to make sure we don't get less data points than required in the next step
                # Substract one (1) to account for index zero (0)
                random_timestamp = random.randint(0, data_size - sample_size - 1)

                # Get the data for the next target number of data points
                for counter in range(random_timestamp, random_timestamp + sample_size):
                    data_points.append(csv_data[counter])

            except ValueError:
                    print(f"Data size is less than the sample size required for task {csv_file}")

    except FileNotFoundError:
        print(f"The file '{csv_file}' was not found.")

    return data_points


def function_two(csv_file: str, data_points: list[str]):
    '''
    2nd API/function that gets the output from 1st one and 
    predicts the next 3 values in the timeseries data.

    Parameters:
                csv_file (str)          :   Name of the CSV File that will containt the output data
                data_points (list[str]) :   List of strings that contains the sampled data

    Return:
                None
    '''

    max_price_one: float = 0.0
    max_price_two: float = 0.0

    try:
        if not data_points:
            raise ValueError("List is empty")
    

        predicted_data: list[str] = data_points
    
        # Get index of last data point recorded
        # Substract one (1) to account for index zero (0)
        index_n: int = len(data_points) - 1


        # Find the 2nd highes value for price
        for data in data_points:

            current_price = float(data[PRICE_INDEX])
            
            if (current_price > max_price_one):
                max_price_two = max_price_one
                max_price_one = current_price
            else:
                if (current_price > max_price_two):                         
                    max_price_two = current_price
                else:
                    # Do nothing
                    pass
        
        # Read last recorded timestamp
        data_n  = data_points[index_n]
        data_n_timestamp = datetime.strptime(data_n[TIMESTAMP_INDEX], '%d-%m-%Y')

        # Create data_point for n+1
        
        data_n1_name: str = data_n[NAME_INDEX]

        # Increment by timedelta one (1) day
        # Some string formatting is implemented to maintain CSV formatting
        data_n1_timestamp: str = (data_n_timestamp + timedelta(days = 1)).strftime('%d-%m-%Y')

        # first predicted (n+1) data point is same as the 2nd highest value present in the 10 data points
        data_n1_price: float = max_price_two

        data_n1 = [data_n1_name, data_n1_timestamp, "%.2f" % data_n1_price]
        predicted_data.append(data_n1)


        # Create data_point for n+2

        data_n2_name: str = data_n[NAME_INDEX]

        # Increment by timedelta two (2) days
        data_n2_timestamp: str = (data_n_timestamp + timedelta(days = 2)).strftime('%d-%m-%Y')

        # n+2 data point has half the difference between n and n+1
        price_delta: float = (float(data_n[PRICE_INDEX]) - data_n1_price) / 2
        # Here I have made the assumption that if the price delta is positive (price going down)
        # I should substract the difference for the next timestamp
        # And the opposite applies if the price is going up
        data_n2_price: float = (data_n1_price - price_delta)

        data_n2 = [data_n2_name, data_n2_timestamp, "%.2f" % data_n2_price]

        predicted_data.append(data_n2)


        # Create data_point for n+3
        data_n3_name: str = data_n[NAME_INDEX]

        # Increment by timedelta three (3) days
        data_n3_timestamp: str = (data_n_timestamp + timedelta(days = 3)).strftime('%d-%m-%Y')

        # n+3 data point has 1/4th the difference between n+1 and n+2
        price_delta = (data_n1_price - data_n2_price) / 4
        # Here I have made the assumption that if the price delta is positive (price going down)
        # I should substract the difference for the next timestamp
        # And the opposite applies if the price is going up
        data_n3_price: float = (data_n2_price - price_delta)

        data_n3 = [data_n3_name, data_n3_timestamp, "%.2f" % data_n3_price]

        predicted_data.append(data_n3)

        # Output to CSV files
        with open(csv_file , 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(predicted_data)

    except ValueError:
        print(f"Data invalid or empty for task {csv_file}.")


def main():
    # Create a list of available input folders (Exchanges)
    # This should be checked if it is empty and act accordingly
    exchanges = os.listdir("./Input")

    number_of_files = int(input('Please enter the number [1 / 2] of files to process: '))

    if (int(number_of_files) in range(1,3)):
        # Input is valid
        pass
    else:
        number_of_files = 1
        print("Input was invalid. Default value of 1 is selected.")

    for exchange in exchanges:
        try:
            # Create output folders for each exchange
            os.mkdir(OUTPUT_FOLDER + "/" + exchange)
        except FileExistsError as e:
            print(f"Folder already exists: {exchange}")

        # Create a list of available input csv files (Stocks)
        stocks = os.listdir("./Input/" + exchange)

        
        stock_counter: int = 1

        for stock in stocks:
            # Only process the required number of files
            if (number_of_files < stock_counter):
                pass
            else:
                csv_input_file = INPUT_FOLDER + "/" + exchange + "/" + stock
                data = function_one(csv_input_file)
                
                csv_output_file = OUTPUT_FOLDER + "/" + exchange + "/" + stock
                function_two(csv_output_file, data)
                stock_counter += 1


if __name__ == "__main__":
    main()