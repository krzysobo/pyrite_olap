#
#

import sys
from sqlalchemy.engine import create_engine
from sqlalchemy import text
import re
import datetime
import csv
import random
import calendar
import math 
import datetime as dt 
import sys 

cache = {}
connection = None

DAILY_CARDINALITY_EXTRA_LOW = 2
DAILY_CARDINALITY_LOW = 5
DAILY_CARDINALITY_MEDIUM = 20
DAILY_CARDINALITY_EXTRA_MEDIUM = 28
DAILY_CARDINALITY_LARGE = 50
DAILY_CARDINALITY_EXTRA_LARGE = 75
DAILY_CARDINALITY_TOTAL = 100


year_start = 2011
year_end = 2024

def main():
    global year_start, year_end

    if len(sys.argv) > 1:
        crd_test = sys.argv[1]
        if crd_test.isnumeric() and 0 < int(crd_test) <= 100:
            sel_daily_cardinality = int(crd_test)
        else:
            print("\n=== incorrect cardinality. Number between 1 and 100 expected.")
            exit(-1)

        if len(sys.argv) == 4:
            year_start_tmp = sys.argv[2]
            year_end_tmp = sys.argv[3]

            if year_start_tmp.isnumeric() and year_end_tmp.isnumeric() and \
                    int(year_end_tmp) >= int(year_start_tmp):
                year_start = int(year_start_tmp)
                year_end = int(year_end_tmp)
    else:
        sel_daily_cardinality = DAILY_CARDINALITY_LOW


    print(f"\n cardinality: {sel_daily_cardinality}\n")

    rows_in = import_template()
    len_rows_in = len(rows_in)
    
    daily_crd_max = math.ceil((sel_daily_cardinality/100.00) * len_rows_in )


    total_days = 0
    total_rows = 0

    fieldnames = [
        "price_total","quantity","date_created.year","date_created.month",
        "date_created.day","customer.name","country.region","country.country",
        "product.category","product.name"
    ]

    dt_str = dt.datetime.now().strftime('%Y_%m_%d_%H_%M')
    filename_out = f'webshop-facts-daily-crd-{sel_daily_cardinality}--{dt_str}.csv'
    with open(filename_out, 'w', newline='') as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        for year in range(year_start, year_end + 1):
            for month in range(1, 13):
                last_day = get_last_day_of_month(year, month)
                for day in range(1, last_day+1):
                    daily_crd_out = random.randint(1, daily_crd_max)
                    total_days += 1
                    total_rows += daily_crd_out

                    product_rows = random.sample(rows_in, daily_crd_out)
                    for pr_row in product_rows:
                        row_out = pr_row.copy()
                        del row_out['base_price']
                        row_out['price_total'] = pr_row['base_price']
                        row_out['quantity'] = random.randint(1, 500)
                        row_out["date_created.year"] = year 
                        row_out["date_created.month"] = month
                        row_out["date_created.day"] = day
                        writer.writerow(row_out)
                    print(f"year {year} month {month} day {day} DAILY CRD MAX: {daily_crd_max} CRD OUT: {daily_crd_out} \n")

    daily_crd_avg = total_rows / total_days                
    print(f"\nTOTAL DAYS : {total_days} TOTAL ROWS: {total_rows} AVG: {daily_crd_avg}\n\n")


def get_last_day_of_month(year: int, month: int):
    return calendar.monthrange(year, month)[1]
    
def import_template():
    count = 0
    header = None

    rows_in = []
    cnt_rows_in = 0

    with open('webshop-products-customers-only.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            
            count = count + 1
            fact = { "id" : count }
            
            if (header == None):
                header = row
                continue
            
            arow = {}
            for header_index in range (0,  len(header)):
                arow[(header[header_index])] = row[header_index]
            rows_in.append(arow)
    cnt_rows_in = len(rows_in)
    print("number of rows in ", cnt_rows_in)

    return rows_in
            

if __name__ == "__main__":
    main()

