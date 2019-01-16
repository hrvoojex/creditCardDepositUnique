#!/usr/bin/env python3
# -*- coding: utf-8

import pandas as pd
import datetime
import uuid

# Initialize input file
xlsxFile = "Bank and Credit card.xlsx"


# Calculate a day when deposit is seen in a bank account
def dayMoneyOnAccount(timespn):
    try:
        if timespn.time() < datetime.time(22):  # Before 22:00 h, goes into that day
            day = timespn.weekday()
        else:
            day = timespn.weekday()
            if day != 6:
                day = timespn.weekday() + 1     # Goes to next day
            else:
                day = 0   # If it's sunday (6), next day is monday (0)
    except:
        return 'NaT'      # If there is no date or can't be parsed to weekday
    if day in [5, 6, 0]:  # By bank rules, friday, 
        day = 2           # sathurday, sunday are visible on wednsday
    elif day == 1:
        day = 3
    elif day == 2:
        day = 4
    elif day == 3:
        day = 0
    else:
        day = 1
    return day


def main():
    xls = pd.ExcelFile(xlsxFile)  # Excel reader
    df1 = pd.read_excel(xls, 0)   # First sheet or df1 = pd.read_excel(xls, 'Sheet_name')
    df2 = pd.read_excel(xls, 1)   # Second sheet
    # Iterate over rows
    unqIDlst = []
    for index, row in df2.iterrows():
        if row['Date'] != 'NaT' and dayMoneyOnAccount(row['Date']) != 'NaT' :  # While there is datetime in column 'Date'
            if index != 0:
                dayAccount = dayMoneyOnAccount(row['Date'])
                unqID = str(uuid.uuid4().fields[-1])[:12]  # 12 character random num
                if dayAccount == prevDayAccount:
                    unqID = prevUnqID  # If on same day on account, add same ID
                unqIDlst.append(unqID)
                # Add current data to yesterdays data for next index
                prevDayAccount = dayAccount
                prevUnqID = unqID 
            else:
                dayAccount = dayMoneyOnAccount(row['Date'])
                unqID = str(uuid.uuid4().fields[-1])[:12]  # 12 character random num
                unqIDlst.append(unqID)
                # Add current data to yesterdays data for next index
                prevDayAccount = dayAccount
                prevUnqID = unqID

    rec = pd.Series(unqIDlst)  # Convert list to pandas Series obj
    df2['unique_identifier'] = rec  # Write Series obj to a new column  

    # unique_identifier = pd.Series([100, 200, 300, 400])  # Conver to pd.Series not to get errors with empty cells
    # df2['unique_identifier'] = unique_identifier  # Add new column

    # # Create a Pandas dataframe from some data.
    # # df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

    # Create a Pandas Excel writer using openpyxl as the engine.
    writer = pd.ExcelWriter('Bank and Credit card Unique deposit.xlsx', engine='openpyxl')

    # Convert the dataframe to an XlsxWriter Excel object.
    df1.to_excel(writer, sheet_name='Sheet1', index=False)  # Don't add index number at the beginning
    df2.to_excel(writer, sheet_name='Sheet2', index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


if __name__ == '__main__':
    main()



