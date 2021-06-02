# Kaustubh Singh
# Python program for BMI calculation
# 02-06-2021

import json, os, logging, sys
from datetime import datetime

dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")

index = 0
bmi = []
category = []
risk = []
return_codes = {"Pass":0,"Fail":1}
logging.basicConfig(filename = 'log.txt', level=logging.DEBUG, format = '%(asctime)s :  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Function to read input JSON file
def read_ip():
    # Opening JSON file
    logging.debug('Opening input JSON file...')
    print('Opening input JSON file...')
    try:
        f = open('input.json')

        # returns JSON object as a dictionary
        logging.debug('Loading data from input JSON file...')
        print('Loading data from input JSON file...')
        data = json.load(f)
        # Closing file
        logging.debug('Closing input JSON file...')
        print('Closing input JSON file...')
        f.close()
    except:
        logging.debug('File error')
        print('File error')
        logging.debug('Exit Code: %s' %(str(return_codes["Fail"])))
        print('\nExit Code: %s' %(str(return_codes["Fail"])))
        sys.exit(return_codes["Fail"])
    return data

# Function to calculate BMI value from input weight and height values
def get_bmi(person):
    logging.debug('Computing BMI for %s...' %person)
    print('Computing BMI for %s...' %person)
    return float(person['WeightKg'])/pow(float(person['HeightCm'])/float(100), 2)

# Function to calculate BMI Category and Risk
def get_cat_rsk(bmi):
    if bmi <= 18.4:
        return ['Underweight', 'Malnutrition risk']
    elif (bmi >= 18.5) and (bmi <= 24.9):
        return ['Normal weight', 'Low risk']
    elif (bmi >= 25) and (bmi <= 29.9):
        return ['Overweight', 'Enhanced risk']
    elif (bmi >= 30) and (bmi <= 34.9):
        return ['Moderately obese', 'Medium risk']
    elif (bmi >= 35) and (bmi <= 39.9):
        return ['Severely obese', 'High risk']
    elif bmi >= 40:
        return ['Very severely obese', 'Very high risk']
    else:
        return None

# Function to count number of overweight people
def count_overwt(category):
    return category.count('Overweight')

# Function to check consistency of the count of overweight people
def check_overwt_count(overwt_count, ip_data):
    logging.debug('Checking consistency of the count of total number of overweight people...')
    print('Checking consistency of the count of total number of overweight people...')
    if (overwt_count >= 0) and (overwt_count <= len(ip_data)):
        logging.debug('Count %s found consistent with the total number of persons %s' %(overwt_count, len(ip_data)))
        print('Count %s found consistent with the total number of persons %s' %(overwt_count, len(ip_data)))
        return True
    logging.debug('Count %s found inconsistent with the total number of persons %s' %(overwt_count, len(ip_data)))
    print('Count %s found inconsistent with the total number of persons %s' %(overwt_count, len(ip_data)))
    return False

# Function to write output to a text file
def write_op(bool_val, count):
    index = 0
    logging.debug('Writing output to a text file...')
    print('Writing output to a text file...')
    try:
        if not os.path.exists('output.txt'):
            open('output.txt', 'a')
        op_file = open('output.txt', 'a')
        op_file.write('\n%s' %timestampStr)
        op_file.write('\nBMI\t|\tCategory\t|\tRisk')
        logging.debug('BMI\t|\tCategory\t|\tRisk')
        print('\nBMI\t|\tCategory\t|\tRisk')
        for value in bmi:
            op_file.write('\n%s\t|\t%s\t|\t%s' %(value, category[index], risk[index]))
            logging.debug('%s\t|\t%s\t|\t%s' %(value, category[index], risk[index]))
            print('\n%s\t|\t%s\t|\t%s' %(value, category[index], risk[index]))
            index += 1
        op_file.write('\nTotal number of overweight people: %s' %count)
        print('\nTotal number of overweight people: %s' %count)
        op_file.write('\nConsistency of count of overweight people: %s\n' %bool_val)
        print('\nConsistency of count of overweight people: %s\n' %bool_val)
        op_file.close()
    except:
        logging.debug('File error')
        print('File error')
        logging.debug('Exit Code: %s' %(str(return_codes["Fail"])))
        print('\nExit Code: %s' %(str(return_codes["Fail"])))
        sys.exit(return_codes["Fail"])

# Function to validate JSON input
def validate_ip(ip_data):
    if (ip_data == None) or (ip_data == []) or (ip_data == {}) or (ip_data == ""):
        logging.debug('Invalid input')
        print('Invalid input')
        logging.debug('Exit Code: %s' %(str(return_codes["Fail"])))
        print('\nExit Code: %s' %(str(return_codes["Fail"])))
        sys.exit(return_codes["Fail"])
    for person in ip_data:
        if (len(person) != 3) or not((isinstance(person['WeightKg'], int) or isinstance(person['WeightKg'], float)) and (isinstance(person['HeightCm'], int) or isinstance(person['HeightCm'], float))):
            logging.debug('Invalid input')
            print('Invalid input')
            logging.debug('Exit Code: %s' %(str(return_codes["Fail"])))
            print('\nExit Code: %s' %(str(return_codes["Fail"])))
            sys.exit(return_codes["Fail"])
        
ip_data = read_ip()
validate_ip(ip_data)
index = 0
for person in ip_data:
    bmi.append(get_bmi(person))
    logging.debug('Calculating BMI Category and Risk for BMI value %s...' %bmi[index])
    print('Calculating BMI Category and Risk for BMI value %s...' %bmi[index])
    category.append(get_cat_rsk(bmi[index])[0])
    risk.append(get_cat_rsk(bmi[index])[1])
    index += 1

logging.debug('Counting the total number of overweight people...')
print('Counting the total number of overweight people...')
write_op(check_overwt_count(count_overwt(category), ip_data), count_overwt(category))
logging.debug('Exit Code: %s' %(str(return_codes["Pass"])))
print('\nExit Code: %s' %(str(return_codes["Pass"])))
sys.exit(return_codes["Pass"])