import pyodbc
import os 
from pathlib import Path
import csv
from dotenv import load_dotenv
import pandas as pd

# .env file-аас орчны хувьсагчийг унших
load_dotenv()

# MSSQL серверийн холболтын мэдээлэл
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
database_distribution = os.getenv('DB_DIST_NAME')
password = os.getenv('DB_PASSWORD')

# MSSQL сервертэй холбогдох
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

conn = pyodbc.connect(connection_string)

connection_string_distribution = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database_distribution};UID={username};PWD={password}'

conn_distribution = pyodbc.connect(connection_string_distribution)
cursor = conn.cursor()
cursor_distribution = conn_distribution.cursor()

# төслийн үндсэн хавтас
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# CSV файлуудыг хадгалах хавтас
DATA_DIR = os.path.join(BASE_DIR, 'static', 'data', 'csv_files')

print(f'BASE_DIR: {BASE_DIR}')
print(f'DATA_DIR: {DATA_DIR}')
# Хэрэв DATA_DIR хавтас байхгүй бол үүсгэх
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f'Created directory: {DATA_DIR}')
else:
    print(f'Directory already exists: {DATA_DIR}')

# бүх хүснэгтүүдийг авах
def get_views():
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS")
    return [row[0] for row in cursor.fetchall()]

# distribution сангийн views хүснэгтүүдийг авах
def get_views_distribution():
    cursor_distribution.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS")
    return [row[0] for row in cursor_distribution.fetchall()]

# Views хүснэгтүүдээс өгөгдлийг татаж авах
def get_views_data(view_name):
    cursor.execute(f"SELECT * FROM {view_name}")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    return columns, rows

# distribution сангийн Views хүснэгтүүдээс өгөгдлийг татаж авах
def get_views_data_distribution(view_name):
    cursor_distribution.execute(f"SELECT * FROM {view_name}")
    columns = [column[0] for column in cursor_distribution.description]
    rows = cursor_distribution.fetchall()
    return columns, rows

# өгөгдлийг CSV файлд хадгалах
def save_to_csv(view_name, columns, rows):
    file_path = os.path.join(DATA_DIR, f"{view_name}.csv")
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # баганын нэрсийг бичих
        writer.writerows(rows)    # өгөгдлийг бичих
    print(f"Account-н дата view '{view_name}' хадгалла. - {file_path}")
    
    
def save_to_csv_distribution(view_name, columns, rows):
    file_path = os.path.join(DATA_DIR, f"{view_name}.csv")
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # баганын нэрсийг бичих
        writer.writerows(rows)    # өгөгдлийг бичих
    print(f"Dist-н view '{view_name}' хадгаллаа. - {file_path}")
    
    
def export_all_views_to_csv():
    views = get_views()
    if not views:
        print("Ямар ч view олдсонгүй.")
        return
    for view in views:
        columns, rows = get_views_data(view)
        save_to_csv(view, columns, rows)
        
def export_all_views_to_csv_distribution():
    views = get_views_distribution()
    if not views:
        print("Ямар ч view олдсонгүй.")
        return
    for view in views:
        columns, rows = get_views_data_distribution(view)
        save_to_csv_distribution(view, columns, rows)
        
        
        
excel_path = r"C:\Users\Dell\OneDrive\attendance\хоолны тооцоо.xlsx"
output_csv_path = os.path.join(DATA_DIR, 'food_calculation.csv')
def convert_excel_to_csv():
    try:
        df= pd.read_excel(excel_path, sheet_name='food registration')
        df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
        print(f"Excel файлыг CSV файлд амжилттай хөрвүүллээ: {output_csv_path}")
    except Exception as e:
        print(f"Алдаа гарлаа: {e}")
        
export_all_views_to_csv()
export_all_views_to_csv_distribution()
convert_excel_to_csv()

# Холболтыг хаах
cursor.close()
conn.close()
cursor_distribution.close()
conn_distribution.close()


print("Data fetching completed.")