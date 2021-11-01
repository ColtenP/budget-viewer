import os
import csv
import sqlite3
from datetime import datetime

db = sqlite3.connect('./transactions.db')


def main():
    for (dirpath, dirnames, filenames) in os.walk('./transactions'):
        for filename in filenames:
            with open(os.path.join(dirpath, filename)) as f:
                reader = csv.DictReader(f)

                if 'capital' in filename:
                    for row in reader:
                        date = datetime.strptime(row['Transaction Date'], '%m/%d/%y').strftime('%Y-%m-%d')
                        amount = -1 * float(row['Transaction Amount'])
                        description = row['Transaction Description']
                        insert_row(date, None, amount, description, 'Capital One')

                elif 'discover' in filename:
                    for row in reader:
                        date = datetime.strptime(row['Post Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                        amount = float(row['Amount'])
                        description = row['Description']
                        insert_row(date, None, amount, description, 'Discover')

                elif 'verizon' in filename:
                    for row in reader:
                        date = datetime.strptime(row['Posting Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                        ref = row['Reference Number']
                        amount = -1 * float(row['Amount'])
                        description = row['Description']
                        insert_row(date, ref, amount, description, 'Verizon')


def insert_row(date: str, ref: str, amount: float, description: str, source: str):
    db.execute('''
        INSERT INTO TRANSACTIONS (date, ref, amount, description, source)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, ref, amount, description, source))
    db.commit()


if __name__ == '__main__':
    main()
