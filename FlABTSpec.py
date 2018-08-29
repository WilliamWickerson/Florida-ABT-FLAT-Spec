_types = {
    1 : "Beer",
    2 : "Wine",
    3 : "Spirits/Liquor",
    4 : "Cigars",
    5 : "Cigarette",
    6 : "Other Tobacco",
    7 : "Other",
    8 : "Total",
}

#Pads integer with 0s right justified
def _zeroPad(x, size):
    string = str(x)
    if len(string) < size:
        padding = "0" * (size - len(string))
        string = padding + string
    return string

#Pads string with spaces left justified
def _spacePadLeft(string, size):
    if len(string) > size:
        string = string[0:size]
    elif len(string) < size:
        string += " " * (size - len(string))
    return string

#Pads string with spaces right justified
def _spacePadRight(string, size):
    if len(string) > size:
        string = string[0:size]
    elif len(string) < size:
        string = (" " * (size - len(string))) + string
    return string

#Gets the string for a single type's sales
def _salesBlock(itemType, amount):
    block = _zeroPad(itemType, 2) + "0000"
    block += _zeroPad(abs(amount), 11)
    block += "+" if amount >= 0 else "-"
    return block

#Wrapes _salesBlock to provide type from dictionary
def _typeBlock(itemType, typeDic):
    return _salesBlock(itemType, typeDic.get(_types[itemType], 0))

#Returns a string for all 8 types
def _fullSales(typeDic):
    line = ""
    for i in range(1, 9):
        line += _typeBlock(i, typeDic)
    return line

#Starts at BEV1100001 and returns next free BEV number
#Use this for any companies missing a license number
currLicenseNum = 1100001
def nextLicenseNum():
    global currLicenseNum
    string = "BEV" + _zeroPad(currLicenseNum, 7)
    currLicenseNum += 1
    return string

#Returns a 29 byte string header
def header(FEIN, licenseNum):
    assert len(FEIN) == 9 and len(licenseNum) == 10
    return "01" + "0000" + FEIN + "0000" + licenseNum

#Returns a 188 byte string of the Type 80 record
#startDate and endDate are of the form MMDDYYYY
#typeDic is a dictionary like: { "Cigars" : 1234 }
#which would mean $12.34 in annual Cigar sales
#See the above _types dictionary
def sellerReport(licenseNum, startDate, endDate, typeDic):
    assert len(licenseNum) == 10 and len(startDate) == 8 and len(endDate) == 8
    line = "80" + "0000"
    line += licenseNum
    line += "0000"
    line += startDate
    line += "0000"
    line += endDate
    line += "0000"
    line += _fullSales(typeDic)
    return line

#Returns a 182 byte string of the Type 81 record
#The retail SUT and FEIN are optional, in which case
#Just replace them with the appropriate number of space characters
def retailerInfo(name, address, city, state, zipcode, retailLicenseNum, retailSUTNum, retailFEIN, sellerLicenseNum):
    zipcode = _zeroPad(int(zipcode), 5)
    assert len(state) == 2 and len(zipcode) == 5 and len(retailSUTNum) == 13 and len(retailFEIN) == 9 and len(sellerLicenseNum) == 10
    line = "81" + "0000"
    line += _spacePadLeft(name, 40)
    line += "0000"
    line += _spacePadLeft(address, 40)
    line += _spacePadLeft(city, 26)
    line += state
    line += zipcode
    line += "0000"
    line += _spacePadRight(retailLicenseNum, 11)
    line += "0000"
    line += retailSUTNum
    line += "0000"
    line += retailFEIN
    line += "0000"
    line += sellerLicenseNum
    return line

#Returns a 183 byte string of the Type 82 record
#monthDate is of the form MMYY
#typeDic is of the same format as Type 80 record
def retailerMonth(monthDate, retailLicenseNum, sellerLicenseNum, typeDic):
    assert len(monthDate) == 4 and len(sellerLicenseNum) == 10
    line = "82" + "0000"
    line += monthDate
    line += "0000"
    line += _fullSales(typeDic)
    line += _spacePadRight(retailLicenseNum, 11)
    line += "0000"
    line += sellerLicenseNum
    return line

#Returns a 59 byte string of the Type 99 trailer
#num81 and num82 are the number of Type 81 and
#Type 82 records respectively, the latter being
#twelve times the former if months aren't left out
def trailer(FEIN, licenseNum, num81, num82):
    assert len(FEIN) == 9 and len(licenseNum) == 10
    line = "99" + "0000"
    line += FEIN
    line += "0000"
    line += licenseNum
    line += "0000"
    line += _zeroPad(num81, 11)
    line += "0000"
    line += _zeroPad(num82, 11)
    return line
