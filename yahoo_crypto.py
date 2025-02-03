import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import sqlite3

def scrape_crypto_data(url):
    
    response = requests.get(url)

 
    if response.status_code == 200:
       
        soup = BeautifulSoup(response.content, 'html.parser')

        
        table = soup.find('table', {'class': 'W(100%)'})

        if table:
           
            headers = []
            data = []

            
            header_row = table.find('thead').find('tr')
            for th in header_row.find_all('th'):
                headers.append(th.text.strip())

            
            for row in table.find('tbody').find_all('tr'):
                row_data = []
                for cell in row.find_all(['th', 'td']):
                    row_data.append(cell.text.strip())
                data.append(row_data)

           
            crypto_data = {'headers': headers, 'data': data}
            return crypto_data
        else:
            print("Table not found on the webpage.")
    else:
        print("Failed to retrieve data from the webpage.")

def save_as_xml(data, filename):
    root = ET.Element("crypto_data")
    headers = ET.SubElement(root, "headers")
    for header in data['headers']:
        ET.SubElement(headers, "header").text = header
    rows = ET.SubElement(root, "rows")
    for row in data['data']:
        xml_row = ET.SubElement(rows, "row")
        for i, cell in enumerate(row):
            ET.SubElement(xml_row, f"col_{i+1}").text = cell
    tree = ET.ElementTree(root)
    tree.write(filename)

def save_as_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def save_to_database(data, db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS CryptoData 
                   (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        {} 
                    )'''.format(" TEXT, ".join([f"{header} TEXT" for header in data['headers']])))

    for row in data['data']:
        placeholders = ", ".join(["?" for _ in data['headers']])
        cursor.execute(f'''INSERT INTO CryptoData ({", ".join(data['headers'])})
                          VALUES ({placeholders})''', row)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    url = "https://finance.yahoo.com/crypto"
    crypto_data = scrape_crypto_data(url)
    if crypto_data:
        print("Crypto Data:")
        print(crypto_data)
        
 
        xml_filename = "crypto_data.xml"
        save_as_xml(crypto_data, xml_filename)
        print(f"Data saved as {xml_filename}")

        json_filename = "crypto_data.json"
        save_as_json(crypto_data, json_filename)
        print(f"Data saved as {json_filename}")


        db_filename = "crypto_data.db"
        save_to_database(crypto_data, db_filename)
        print(f"Data saved to database {db_filename}")
