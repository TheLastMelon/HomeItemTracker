import os
import shutil
import tkinter as tk
import uuid
from tkinter import filedialog
import sqlite3

RECEIPT_SAVE_LOC = "RECEIPT"
PHOTOS_SAVE_LOC = "PHOTOS"
DATABASE = "HIC.db"

SQL_CREATE_TABLE_RECEIPT = 'CREATE TABLE IF NOT EXISTS RECEIPT(' \
                           'RECEIPT_ID INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                           'PHOTO_LOC TEXT NOT NULL,' \
                           'ITEM_ID INT NOT NULL,' \
                           'FOREIGN KEY (ITEM_ID) REFERENCES ITEMS(ITEM_ID));'

SQL_CREATE_TABLE_ITEMS = 'CREATE TABLE IF NOT EXISTS ITEMS(' \
                         'ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT,' \
                         'ITEM_NAME TEXT NOT NULL,' \
                         'ITEM_DESCRIPTION TEXT NOT NULL,' \
                         'ITEM_PRICE REAL NOT NULL,' \
                         'ITEM_LINK TEXT' \
                         'SERIAL_NUMBER TEXT,' \
                         'MODEL_NUMBER TEXT, ' \
                         'SERIAL_NUMBER TEXT);'

SQL_CREATE_TABLE_PHOTOS = 'CREATE TABLE IF NOT EXISTS PHOTOS(' \
                          'ITEM_ID INT NOT NULL,' \
                          'PHOTO_LOC TEXT NOT NULL,' \
                          'FOREIGN KEY (ITEM_ID) REFERENCES ITEMS(ITEM_ID));'


def createStructure():
    if not os.path.exists(RECEIPT_SAVE_LOC):
        os.mkdir(RECEIPT_SAVE_LOC)
        print("The waiting folder did not exists, creating it now")

    if not os.path.exists(PHOTOS_SAVE_LOC):
        os.mkdir(PHOTOS_SAVE_LOC)
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

    if userResponse.lower() == 'Y'.lower():
        result.append(input('Model Number: '))
    else:
        result.append(None)

    userResponse = input('Is there a Serial Number, (Y)es or (N)o? ')
    if userResponse.lower() == 'Y'.lower():
        result.append(input('Serial Number: '))
    else:
        result.append(None)

    return result


def selectFiles():
    root = tk.Tk()
    root.withdraw()
    selectedFiles = filedialog.askopenfilenames()
    return selectedFiles


def addAttachment(rowID, photos, table_name):
    print(photos)
    saveDir = os.path.join(table_name, str(rowID))
    os.mkdir(saveDir)
    for x in photos:
        fileName = str(uuid.uuid4()) + '.' + x.split(".")[1]
        saveLoc = os.path.join(saveDir, fileName)
        shutil.move(x, os.path.join(os.getcwd(), saveLoc))

        conn = sqlite3.connect(DATABASE)
        print('Opening the database to add an item.')

        sqlAddPhoto = "INSERT INTO " + table_name + "( ITEM_ID, PHOTO_LOC)" \
                                                    "VALUES('{}', '{}');".format(rowID, saveLoc)

        cursor = conn.cursor()
        cursor.execute(sqlAddPhoto)

        cursor.close()
        conn.commit()
        conn.close()


def addItem():
    while True:

        print("")
        print("======================Data Entry======================")
        itemName = input('What is the Item Name: ')
        itemDesc = input('A description of the item: ')
        itemPrice = input('Replacement Item Cost: ')
        itemLink = input('A link to the item:  ')

        if itemLink == "":
            itemLink = None

        modelSerialNumber = getModelSerialNumber()
        modelNumber = modelSerialNumber[0]
        serialNumber = modelSerialNumber[1]

        print("======================End Data Entry======================")
        print("")

        print("")
        print("======================Review Data Entry======================")
        print("Item Name: " + itemName)
        print("Item Description: " + itemDesc)
        print("Item Price: " + itemPrice)

        if itemLink is not None:
            print("Item Link: " + itemLink)

        if serialNumber is not None:
            print("Serial Number: " + serialNumber)

        if modelNumber is not None:
            print("Model Number: " + modelNumber)

        print("======================End Review Data Entry======================")
        answer = input('Does this information look correct? ')
        print("")
        if answer.lower() == 'y':
            break

    sqlAddItem = "INSERT INTO ITEMS(ITEM_LINK, ITEM_PRICE, ITEM_NAME, ITEM_DESCRIPTION, SERIAL_NUMBER, " \
                 "MODEL_NUMBER)" \
                 "VALUES('{}',{},'{}','{}', '{}', '{}');".format(itemLink, itemPrice, itemName, itemDesc, serialNumber,
                                                                 modelNumber)

    conn = sqlite3.connect(DATABASE)
    print('Opening the database to add an item.')

    cursor = conn.cursor()
    cursor.execute(sqlAddItem)

    rowID = cursor.lastrowid

    cursor.close()
    conn.commit()
    conn.close()

    print(rowID)

    possiblePhotos = input("Do you Have any photos you would like to add? (Y)es or (N)o: ")
    if possiblePhotos.lower() == 'Y'.lower():
        photos = selectFiles()
        addAttachment(rowID, photos, PHOTOS_SAVE_LOC)

    receiptExists = input('Is there a receipt that is associated with this item, (Y)es or (N)o: ')
    if receiptExists.lower() == 'Y'.lower():
        receipt = selectFiles()
        addAttachment(rowID, receipt, RECEIPT_SAVE_LOC)


def main():
    # Setting up the folder structure for storing files and ingesting
    createStructure()

    while True:
        print("")
        print('======================Selection Menu======================')
        print("1) Add Item")
        print("2) Add Receipt")
        print("3) Add Photos")
        print('======================Selection End======================')
        answer = input("What Did you want to do? ")
        print("")
        if answer == "1":
            addItem()
        elif answer == "2":
            addAttachment(input('Enter the associated Item ID: '), selectFiles(), RECEIPT_SAVE_LOC)
        elif answer == "3":
            addAttachment(input('Enter the associated Item ID: '), selectFiles(), PHOTOS_SAVE_LOC)

        continueAsking = input('Continue adding items? (Y)es or (N): ')
        if continueAsking.lower() == 'n':
            break


if __name__ == '__main__':
    main()
