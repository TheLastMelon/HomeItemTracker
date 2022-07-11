import os
import tkinter as tk
import uuid
from tkinter import filedialog
import sqlite3

TO_BE_PROCESS = "WAITING"
PROCESSED = "PROCESSED"
DATABASE = "HIC.db"

SQL_CREATE_TABLE_RECEIPT = 'CREATE TABLE IF NOT EXISTS RECEIPT(' \
                           'RECEIPT_ID INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                           'PURCHASE_DATE DATE,' \
                           'TOTAL REAL NOT NULL,' \
                           'STORAGE_LOCATION VARCHAR(255) NOT NULL,' \
                           'ITEM_ID INT NOT NULL,' \
                           'FOREIGN KEY (ITEM_ID) REFERENCES ITEMS(ITEM_ID));'

SQL_CREATE_TABLE_ITEMS = 'CREATE TABLE IF NOT EXISTS ITEMS(' \
                         'ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT,' \
                         'ITEM_DESCRIPTION VARCHAR(255) NOT NULL,' \
                         'ITEM_PRICE REAL NOT NULL,' \
                         'SERIAL_NUMBER VARCHAR(128),' \
                         'MODEL_NUMBER VARCHAR(128));'

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

        conn.execute(SQL_CREATE_TABLE_ITEMS)
        conn.execute(SQL_CREATE_TABLE_RECEIPT)
        conn.execute(SQL_CREATE_TABLE_PHOTOS)

        conn.commit()

        conn.close()
        print('Added the proper tables for the new database.')


def getModelSerialNumber():
    result = []

    userResponse = input('Is there a Model Number, (Y)es or (N)o? ')

    if userResponse == 'Y':
        result.append(input('Model Number: '))
    else:
        result.append('')

    userResponse = input('Is there a Serial Number, (Y)es or (N)o? ')
    if userResponse == 'Y':
        result.append(input('Serial Number: '))
    else:
        result.append('')

    return result


def getReceipt():
    root = tk.Tk()
    root.withdraw()
    selectedReceipt = filedialog.askopenfilename()
    return selectedReceipt


def getPhotos():
    root = tk.Tk()
    root.withdraw()
    selectedFiles = filedialog.askopenfilenames()
    return selectedFiles


def addItem():
    # Gather info about the item
    purchaseDate = input('What was the purchase date of the item mm/dd/yyyy: ')
    itemTotal = input("How much did the item cost: ")
    itemName = input('Describe the item: ')

    modelSerialNumber = getModelSerialNumber()
    modelNumber = modelSerialNumber[0]
    serialNumber = modelSerialNumber[1]

    photos = getPhotos()

    sqlAddItem = "INSERT INTO ITEMS( ITEM_DESCRIPTION, ITEM_PRICE, SERIAL_NUMBER, " \
                 "MODEL_NUMBER)" \
                 "VALUES('{}', {}, '{}', '{}');".format(itemName, itemTotal, serialNumber, modelNumber)

    conn = sqlite3.connect(DATABASE)
    print('Opening the database to add an item.')

    cursor = conn.cursor()
    cursor.execute(sqlAddItem)

    rowID = cursor.lastrowid

    cursor.close()
    conn.commit()
    conn.close()

    print(rowID)

    receiptExists = input('Is there a receipt that is associated with this item, (Y)es or (N)o: ')
    if receiptExists == 'Y':
        receipt = getReceipt()
        receiptID = uuid.uuid4()


def addReceipt():
    print('hello')


def addItemsOrReceipt():
    while True:
        userResponse = input('Add a single (I)tem or scan a (R)eceipt? ')

        if userResponse == 'I' or userResponse == 'R':
            break
        else:
            print("Invalid input")

    if userResponse == 'I':
        addItem()
    else:
        addReceipt()


def main():
    # Setting up the folder structure for storing files and ingesting
    createStructure()

    while True:
        addItemsOrReceipt()
        continueAsking = input('Continue adding items or receipts? (Y)es or (N): ')
        if continueAsking == 'N':
            break

    # Getting the

    # what


if __name__ == '__main__':
    main()
