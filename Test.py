from random import randint

from randomtimestamp import randomtimestamp

invoiceID = 1

while invoiceID <= 10:
    random_date = randomtimestamp(start_year=2015,end_year=2022,text=False).strftime("%d/%m/%Y")
    count = 0
    used = []
    while count < randint(4,10):
        procID = randint(1,10)
        while procID in used:
            procID = randint(1,10)

        used.append(procID)
        unitCount = randint(1, 5)
        print('insert into PROC_TO_INV values({}, {}, {}, "{}");'.format(procID,invoiceID, unitCount, random_date))
        count += 1
    used.clear()

    invoiceID += 1