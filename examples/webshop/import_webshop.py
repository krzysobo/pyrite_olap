import sys
import os
from sqlalchemy.engine import create_engine
from sqlalchemy import text
import re
import datetime
import csv
import random


cache = {}
connection = None
file_csv = 'webshop-facts.csv'

def main():
    global connection
    global file_csv

    if len(sys.argv) > 1:
        file_csv = sys.argv[1]

    if not os.path.exists(file_csv):
        print(f"\nFILE with name {file_csv} does NOT exist. Quitting.\n")
        exit(-1)
    
    # Open source
    engine = create_engine("sqlite:///webshop.sqlite")
    connection = engine.connect()

    # re-installation of the whole database (total cleanup)
    with open("webshop-structure.sql",'rb') as sf:
        sqlite3_conn = connection.connection
        sql_script = sf.read().decode('utf-8')
        print("\n===== SQL SCRIPT: ", sql_script,"\n\n")
        sqlite3_conn.executescript(sql_script)

    # connection.execute("DELETE FROM dates");
    # connection.execute("DELETE FROM customers");
    # connection.execute("DELETE FROM countries");
    # connection.execute("DELETE FROM products");
    # connection.execute("DELETE FROM sales");
    # connection.execute("DELETE FROM webvisits")
    
    # Import facts and dimension data
    import_sales()
    # Generate all dates
    generate_dates()
    # Generate site visits
    generate_webvisits()

    # Add extra dimensions for left joins
    insert_product ("Books", "200 ways of slicing a cube")    

def save_object(table, row):
    
    if (table in cache):
        if (row["id"] in cache[table]):
            return row["id"]
    else:
        cache[table] = {}
    
    keys = row.keys();
    sql = "INSERT INTO " + table + " ("
    sql = sql + ", ".join(keys)
    sql = sql + ") VALUES ("
    sql = sql + ", ".join([ ("'" + str(row[key]) + "'") for key in keys])
    sql = sql + ")"
    
    print("Inserting - Table: %-14s Id: %s" % (table, row["id"]))
    #print sql
    
    connection.execute(sql);
    cache[table][row["id"]] = row      
                              
    return row["id"]

def sanitize(value):
    
    if (value == ""):
        value = "(BLANK)"
    elif (value == None):
        value = "(NULL)"
    else:
        value = re.sub('[^\w]', "_", value.strip())
    return value

def insert_country (continent, country):
    
    row = {
           "id": sanitize (continent + "/" + country),
           "continent_id": sanitize(continent),
           "continent_label": continent,
           "country_id": sanitize(country),
           "country_label": country,
    }
    return save_object ("countries", row)

def insert_product (category, product):
    
    row = {
           "id": sanitize (category + "/" + product),
           "category_id": sanitize(category),
           "category_label": category,
           "product_id": sanitize(product),
           "product_label": product,
    }
    return save_object ("products", row)

def insert_customer (customer_name):
    
    row = {
           "id": sanitize(customer_name),
           "name": customer_name
    }
    return save_object ("customers", row)

def insert_date (year, month, day):
    
    row = { }
    prefix = "date"

    date = datetime.date(int(year), int(month), int(day));

    if date != None:
        row["id"] = sanitize(datetime.datetime.strftime(date, "%d/%b/%Y"))
        row[prefix + "_year"] = date.year
        row[prefix + "_quarter"] = ((date.month - 1) / 3) + 1
        row[prefix + "_month"] = date.month
        row[prefix + "_day"] = date.day
        row[prefix + "_week"] = date.isocalendar()[1]

        if row[prefix + "_month"] == 12 and row[prefix + "_week"] <= 1:
            row[prefix + "_week"] = 52
        if row[prefix + "_month"] == 1 and row[prefix + "_week"] >= 52:
            row[prefix + "_week"] = 1

    return save_object ("dates", row)

def insert_sale(fact):
    return save_object ("sales", fact)

def insert_webvisit(fact):
    return save_object ("webvisits", fact)

def generate_dates():
    
    start_date =  datetime.datetime.strptime("2012-01-01", "%Y-%m-%d")
    end_date =  datetime.datetime.strptime("2013-12-31", "%Y-%m-%d")
    
    cur_date = start_date
    while (cur_date <= end_date):
        insert_date (cur_date.year, cur_date.month, cur_date.day)
        cur_date = cur_date + datetime.timedelta(days = +1)
    
def import_sales():
    count = 0
    incorrect_rows_count = 0
    header = None
    with open(file_csv, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            
            count = count + 1
            fact = { "id" : count }
            
            if (header == None):
                header = row
                continue
            
            arow = {}

            incorrect_row = False
            for header_index in range (0,  len(header)):
                arow[(header[header_index])] = row[header_index]
                if row[header_index] is None or str(row[header_index]) == "":
                    incorrect_row = True

            if incorrect_row:
                print(f"\n== incorrect ROW index: {count} - skipping\n")
                incorrect_rows_count += 1
                continue

            # Process row
            fact["date_id"] = insert_date(arow["date_created.year"], arow["date_created.month"], arow["date_created.day"])
            fact["country_id"] = insert_country(arow["country.region"], arow["country.country"])
            fact["customer_id"] = insert_customer(arow["customer.name"])
            fact["product_id"] = insert_product(arow["product.category"], arow["product.name"])
            
            # Import figures (quick hack for localization issues):
            if arow['quantity'] is None or arow['quantity'] == "" or arow['price_total'] is None or arow['price_total'] == "":
                continue

            fact["quantity"] = float(str(arow["quantity"]).replace(",", "."))
            fact["price_total"] = float(str(arow["price_total"]).replace(",", "."))
            
            print(f"\n======= Inserting sales row: {count}\n")
            insert_sale(fact)
            
    print(f"== Imported {count} facts. Incorrect rows no: {incorrect_rows_count}\n\n")

def generate_webvisits():
    
    for i in range (1, 1079):
        
        fact = { "id" : i }
        
        fact["country_id"] = random.choice (list(cache["countries"].keys()))
        fact["date_id"] = random.choice (list(cache["dates"].keys()))
        
        fact["browser"] = random.choice (list(["Lynx", "Firefox", "Firefox", "Chrome", "Chrome", "Chrome"]))
        fact["newsletter"] = random.choice (list(["Yes", "No", "No", "No"]))
        
        fact["source_label"] = random.choice(list(["Web search", "Web search", "Direct link", "Unknown"]))
        fact["source_id"] = sanitize(fact["source_label"])
        
        fact["pageviews"] = abs(int (random.gauss (7, 6))) + 1
        
        insert_webvisit(fact)

if __name__ == "__main__":
    main()

