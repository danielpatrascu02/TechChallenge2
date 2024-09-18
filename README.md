# TechChallenge2

Pre-Interview Coding Challenge
Challenge 2: Backend – Predict next 3 values of Stock price (timeseries data)

## About

This application was developed with the following objective:
For each stock exchange, select the specified number of files, and for each file provided, predict the next 3 values of stock price for that specific file.

The requirements for this application did not mention the use of a specific programming language. The job application that is part of this challenge also did not mention the use of a specific programming language. That being said, I made the decision to solve the challenge using Python. The reason for this was the quick prototyping nature of Python and also the easy support for working with CSV files.

The application was developed using Python 3.12. No backward compatibility was tested.
Python packages used:

os
csv
datetime
random

No other additional packages were used.

## Application structure

The application consist of three functions:

function_one()  - for each file provided, returns 10 consecutive data points starting from a random
timestamp
function_two()  - gets the output from 1st one and predicts the next 3 values in the timeseries data
main()          - main function where calls to the prior functions are made



## Running the application

To run the application, the user must have Python 3.12 (or prior versions !?! ) installed.
The source folder should contain the main.py file, along with two folders.
Folder Input - stores exchanges/stock data, as provided for the challenge.
Folder Output - should be empty. Here the CSV files containing the prediction data will be stored.

CLI Usage: main.py

No additional optional arguments.

## Optional Enhancements to be made

1. Both functions can be extracted into standalone python files and imported in different projects with minimal modifications
2. Some formatting checks should be added for data read from the CSV. Currently, no check is being made on the data. Some check that can be implemented:
    - check if price data does not contain invalid numbers (negative price, zero price)
    - check if timestamp data is in correct formatting and discard data point if false
    - check if timestamp data is valid - dates that are from the future, dates that don't exist e.g 32-03-2025
    - check if the CSV file has the correct delimiter (, or ;)
3. Some logic check must be added for the prediction algorithm. 
    In a very specific case where the n-data point is also the 2nd highest value, the n+1 data point will be equal to the n-data point. This in turn will make the n+2 data and n+3 data also equal, because the difference will be zero.
4. For the moment, only 1 and 2 are valid user inputs for the number of files that will be processed. This can be added as a parameter to the application.
5. The prediction algorithm used was the one provided in the requirements, for simplicity. Additional algorithms should be implemented.

## Logical assumptions

1. n+2 data point has half the difference between n and n +1
    In this case, the wording of the requirement was not very clear and I made the following assumption: 
    - if the price between n and n+1 has increased, the price between n+1 and n+2 will also increase with the specified amount.
    - if the price between n and n+1 has decreased , the price between n+1 and n+2 will also decrease with the specified amount.
2. n+3 data point has 1/4th the difference between n+1 and n+2
    In this case, the wording of the requirement was not very clear and I made the following assumption: 
    - if the price between n+1 and n+2 has increased, the price between n+2 and n+3 will also increase with the specified amount.
    - if the price between n+1 and n+2 has decreased , the price between n+2 and n+3 will also decrease with the specified amount.