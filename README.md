# Florida ABT FLAT Spec

This library aims to provide a simple to use interface for creating Florida's Alcoholic Beverages and Tobacco Products Annual Report FLAT file. The complete specification can be found [here](http://floridarevenue.com/taxes/Documents/flAbtImportFileSpecs.pdf). While the Florida Department of Revenue provides an Excel template for formatting everything, it's somewhat fickle and requires manual data entry into the spreadsheet.

Use
----
The library has no external dependencies and can be imported as simply as:
```python
import FlABTSpec as ABT
```
The user will need to match retailer info to their monthly categorized sales totals through some means. In the provided example the only product sold is Cigars and the Retailers and Sales Totals are read in from two seperate .csv spreadsheets. From that point the data can be formatted to make the FLAT file like so:
```python
with open("ABT.txt", "w") as abtfile:
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
```
Note that the ABT FLAT file is a newline delimited list of "Records" so a newline character is appended to each write call.

License
----

MIT