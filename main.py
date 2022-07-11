import os
import tkinter as tk
from tkinter import filedialog
import sqlite3

TO_BE_PROCESS = "WAITING"
PROCESSED = "PROCESSED"
DATABASE = "HIC.db"

SQL_CREATE_TABLE_RECEIPT = 'CREATE TABLE IF NOT EXISTS RECEIPT(' \
                           'RECEIPT_ID IDENTITY(1,1) NOT NULL, ' \
                           'PURCHASE_DATE DATE NOT NULL,' \
                           'TOTAL REAL NOT NULL,' \
                           'STORAGE_LOCATION VARCHAR(255) NOT NULL,' \
                           'PRIMARY KEY(RECEIPT_ID));'

SQL_CREATE_TABLE_ITEMS = 'CREATE TABLE IF NOT EXISTS ITEMS(' \
                         'ITEM_ID IDENTITY(1,1) NOT NULL,' \
                         'RECEIPT_ID INT NOT NULL,' \
                         'ITEM_CODE VARCHAR(15) NOT NULL,' \
                         'ITEM_DESCRIPTION VARCHAR(255) NOT NULL,' \
                         'ITEM_PRICE_EA REAL NOT NULL,' \
                         'ITEM_PRICE REAL NOT NULL,' \
                         'ITEM_QUANTITY INT NOT NULL DEFAULT 1,' \
                         'PRIMARY KEY(ITEM_ID),' \
                         'FOREIGN KEY (RECEIPT_ID) REFERENCES RECEIPT(RECEIPT_ID));'

SQL_CREATE_TABLE_PHOTOS = 'CREATE TABLE IF NOT EXISTS PHOTOS(' \
                          'ITEM_ID INT NOT NULL,' \
                          'PHOTO_LOC VARCHAR(255) NOT NULL,' \
                          'FOREIGN KEY (ITEM_ID) REFERENCES ITEMS(ITEM_ID));'


def createStructure():
    if not os.path.exists(TO_BE_PROCESS):
        os.mkdir(TO_BE_PROCESS)
        print("The waiting folder did not exists, creating it now")

    if not os.path.exists(PROCESSED):
        os.mkdir(PROCESSED)
        print("The processed folder did not exists, creating it now")

    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        print("Database was mot found, creating it and the tables.")

        conn.execute(SQL_CREATE_TABLE_RECEIPT)
        conn.execute(SQL_CREATE_TABLE_ITEMS)
        conn.execute(SQL_CREATE_TABLE_PHOTOS)

        conn.commit()

        conn.close()
        print('Added the proper tables for the new database.')


def main():
    createStructure()
    # Getting the
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilenames()
    print(file_path)
    #what


if __name__ == '__main__':
    main()
