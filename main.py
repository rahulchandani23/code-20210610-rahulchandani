import pandas as pd
import json
import numpy as np
import os


# Function to clear null values
def clear_null(val):
    if pd.isnull(val):
        return 0
    else:
        return val
    
# function to clear divide by 0 - infinite values
def clear_inf(val):
    if np.isinf(val):
        return 0
    else:
        return val


#main function to calculate bmi of a person
def bmi_calculator(filename):
    
    #Handling both csv and json files
    name,ext = os.path.splitext(filename)
    if ext=='.json':
        df = pd.read_json(filename)
    elif ext=='.csv':
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame.columns["Gender","HeightCm","WeightKg"]
    
    # clearing na values if any
    df.dropna(axis=0)
    
    df['Heightm'] = df['HeightCm'] / 100
    df['BMI'] = df['WeightKg'] / (df['Heightm'] ** 2)
    
    df['BMI'].apply(clear_null)
    pd.set_option('use_inf_as_na', True)
    df['BMI'] = df['BMI'].fillna(100)
    # print(df)
    
    #creating bins according to the table 1
    bins = [0, 18.5, 25, 30, 35, 40, np.inf]
    
    bmi_category = ['Underweight', 'Normal weight', 'Overweight', 'Moderately Obese', 'Severely Obese',
                    'Very Severely Obese']
    health_risk = ['Malnutrition Risk', 'Low Risk', 'Enhanced Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
    
    df['BMI Category'] = pd.cut(df['BMI'], bins, labels=bmi_category, include_lowest=True)
    df['Health Risk'] = pd.cut(df.BMI, bins, labels=health_risk, include_lowest=True)
    
    df.drop(['Heightm'], axis=1)
    
    overweight_count = df['BMI Category'].value_counts()['Overweight']
    
    json_data = df.to_json(orient='records')
    
    
    #returning the required json output - can also be written into a file as required.
    return json_data,overweight_count
    
    
if __name__ == '__main__':
    filename = 'input.json'

    print(bmi_calculator(filename))
