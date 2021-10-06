import pandas as pd
import json
import numpy as np
import os

def clear_null(val):
    if pd.isnull(val):
        return 0
    else:
        return val
    
def clear_inf(val):
    if np.isinf(val):
        return 0
    else:
        return val

def bmi_calculator(filename):
    name,ext = os.path.splitext(filename)
    if ext=='.json':
        df = pd.read_json(filename)
    elif ext=='.csv':
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame.columns["Gender","HeightCm","WeightKg"]
    
    
    df.dropna(axis=0)
    
    df['Heightm'] = df['HeightCm'] / 100
    df['BMI'] = df['WeightKg'] / (df['Heightm'] ** 2)
    
    df['BMI'].apply(clear_null)
    pd.set_option('use_inf_as_na', True)
    df['BMI'] = df['BMI'].fillna(100)
    print(df)
    
    
    bins = [0, 18.5, 25, 30, 35, 40, np.inf]
    
    bmi_category = ['Underweight', 'Normal weight', 'Overweight', 'Moderately Obese', 'Severely Obese',
                    'Very Severely Obese']
    health_risk = ['Malnutrition Risk', 'Low Risk', 'Enhanced Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
    
    df['BMI Category'] = pd.cut(df['BMI'], bins, labels=bmi_category, include_lowest=True)
    df['Health Risk'] = pd.cut(df.BMI, bins, labels=health_risk, include_lowest=True)
    
    df.drop(['Heightm'], axis=1)
    
    overweight_count = df['BMI Category'].value_counts()['Overweight']
    
    json_data = df.to_json(orient='records')
    
    return json_data,overweight_count
    
    
    

filename = 'weight-height.csv'

print(bmi_calculator(filename))