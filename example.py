from operator import itemgetter
import csv
import FlABTSpec as ABT

abt_lines = []

with open("ABT Retailers.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"', dialect="excel")
    for row in csvreader:
        if "".join(row) != "":
            abt_lines.append(row[0:7])

for line in abt_lines:
    #strip white space
    for i in range(0, 7):
        line[i] = line[i].strip()
    #expand WD to Winn Dixie
    if line[1].startswith("WD: "):
        line[1] = "Winn Dixie " + line[1][line[1].find("#"):]
    if line[1].startswith("Winn Dixies"):
        line[1] = line[1][0:10] + line[1][11:]
    #make zip codes 5 digits
    line[5] = line[5][:5]

#sort and remove duplicates
abt_lines = sorted(abt_lines[1:], key=itemgetter(1))
abt_lines = [abt_lines[i] for i in range(len(abt_lines)) if i == 0 or abt_lines[i] != abt_lines[i-1]]

#report duplicate names
for i in range(1, len(abt_lines)):
    if abt_lines[i][1] == abt_lines[i-1][1]:
        print(abt_lines[i - 1])
        print(abt_lines[i])

doWrite = False

with open("Retailers.csv", "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, dialect="excel")
    for line in abt_lines:
        csvwriter.writerow(line)

lines = []

prefix = ""

ignore = {
    "Cigar Rollers" : 1,
    "Walk In Customers" : 1,
}

with open("Monthly Sales.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"', dialect="excel")
    for row in csvreader:
        #prefixes may expand name of following sub-companies
        elif row[3] == "":
            if row[1] == "WD":
                prefix = "Winn Dixie #"
        #sub company so add the prefix
        elif row[1] == "":
            row[1] = prefix + row[2]
            row[2] = ""
            lines.append(row[1:])
        #remove any remaining Totals, they don't count
        elif not row[1].startswith("Total") and not row[1] == "" and row[1] not in ignore:
            lines.append(row[1:])

#lines are seperated by empty columns, remove those
lines = [line[::2] for line in lines[1:-1]]

for row in lines:
    #strip name white space
    row[0] = row[0].strip()
    postfix = ""
    #Keep (Grocery) postfix and take city name out of Winn Dixie
    if row[0].endswith("(Grocery)"):
        postfix = " (Grocery)"
    if row[0].startswith("Winn Dixie #"):
        row[0] = row[0][:row[0].find(" ", 12)] + postfix

num_missing = 0

print("No match for the following companies:\n")

#check for missing companies between the two files
for row in lines:
    found = False
    for line in abt_lines:
        if row[0] == line[1]:
            found = True
    if not found:
        print(row)
        num_missing += 1

#remove commas and periods to get int with decimal
def getIntFromExcel(string):
    string = string.replace(",", "").replace(".", "")
    return int(string)

sums = [0] * 13

#sum the sales to make sure everything is correct
for line in lines:
    for i in range(1,14):
        sums[i-1] += getIntFromExcel(line[i])

print()
print(sums)

assert num_missing == 0

sellerFEIN = "123456789"
sellerLicenseNum = "WDE1100000"
startDate = "20170701"
endDate = "20180630"
totalSales = { "Cigars" : sums[12] }
retailSUTNum = " " * 13
retailFEIN = " " * 9
months = {
    0 : "0717",
    1 : "0817",
    2 : "0917",
    3 : "1017",
    4 : "1117",
    5 : "1217",
    6 : "0118",
    7 : "0218",
    8 : "0318",
    9 : "0418",
    10 : "0518",
    11 : "0618",
}
num81 = 0
num82 = 0

#Write out to the ABT file using all of the info
with open("CABT.txt", "w") as abtfile:
    abtfile.write(ABT.header(sellerFEIN, sellerLicenseNum) + "\n")
    abtfile.write(ABT.sellerReport(sellerLicenseNum, startDate, endDate, totalSales) + "\n")
    for company in lines:
        num81 += 1
        retailName = company[0]
        #Find matching retailer and get info
        for row in abt_lines:
            if retailName == row[1]:
                retailLicenseNum = row[0]
                if retailLicenseNum == "":
                    retailLicenseNum = ABT.nextLicenseNum()
                retailAddress = row[2]
                retailCity = row[3]
                retailState = row[4]
                retailZipcode = row[5]
        abtfile.write(ABT.retailerInfo(retailName, retailAddress, retailCity, retailState, retailZipcode, retailLicenseNum, retailSUTNum, retailFEIN, sellerLicenseNum) + "\n")
        for i in range(0, 12):
            num82 += 1
            abtfile.write(ABT.retailerMonth(months[i], retailLicenseNum, sellerLicenseNum, { "Cigars" : getIntFromExcel(company[i+1]) }) + "\n")
    abtfile.write(ABT.trailer(sellerFEIN, sellerLicenseNum, num81, num82) + "\n")



        
