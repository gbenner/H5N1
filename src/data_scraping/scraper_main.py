#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Greg
#
# Created:     20/03/2011
# Copyright:   (c) Greg 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import re
import datetime

import myutil


class OutbreakData:
    def __init__(self):
        self.report_date = None
        self.country     = None
        self.latitude    = None
        self.longitude   = None
        self.cases       = None
        self.deaths      = None
        self.uri         = None

    @staticmethod
    def HeaderString():
            return "report_date\tcountry\tlatitude\tlongitude\tcases\tdeaths\turi\n"

    def ToTsvString(self):
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n"  % (self.report_date, self.country, self.latitude, self.longitude, self.cases, self.deaths, self.uri)




gLineNumber = -1


def main():

    RunFull("2011")
    RunFull("2010")
    RunFull("2009")
    RunFull("2008")
    RunFull("2007")
    #RunUnitTest()
    pass



def RunFull(year):

    errors = []
    errFile = open("../data/" + year + "_errors.txt","w")
    outFile = open("../data/" + year + "_out.tsv","w")
    outFile.write(OutbreakData.HeaderString())


    dataSrc = "D:\\School\\171\\fp\\data\\text\\" + year
    files = myutil.findFiles(dataSrc)

    for file in files:
        print "Extract file: " , file

        name = (file.split('/')[-1])[:-4]
        uri = "http://web.oie.int/wahis/reports/" +  name  +  ".pdf"

        data = ProccessTextFile(file, uri, errors)
        print "Found %d items" % (len(data))

        for d in data:
            outFile.write( d.ToTsvString() )

        FLushErrors(errFile, file, errors)

    outFile.close()
    errFile.close()


def RunUnitTest():

    print "Running unit Test"

    errors = []

    outFile = open("../data/unittest.tsv","w")
    outFile.write(OutbreakData.HeaderString())

    #file = "D:\\School\\171\\fp\\data\\sample\\en_fup_0000010121_20110102_154206.txt"
    file = "D:\\School\\171\\fp\\data\\text\\2010\\en_fup_0000009208_20100501_143249.txt"

    print "Open file : ", file

    uri = file.split('/')[-1]
    data = ProccessTextFile(file, uri, errors)

    for d in data:
        outFile.write( d.ToTsvString() )

    outFile.close()

    errFile = open("../data/errors.txt","w")
    FLushErrors(errFile, file, errors)
    errFile.close()




def FLushErrors(errFile, filename, errors):

    errFile.write(filename)
    errFile.write("\n")

    for err in errors:
        errFile.write(err)
        errFile.write("\n")

    errFile.write("\n\n")
    del errors[:]
    ##errors.clear()



def SeekToString(f, str):
    global gLineNumber
    while 1:
        line = f.readline()
        gLineNumber +=1
        if not line:
            return None
        if line.find(str) > -1:
            return line



def SeekToStringTup(f, tup ):
    global gLineNumber
    while 1:
        line = f.readline()
        gLineNumber += 1
        if not line:
            return None
        for s in tup:
            if line.startswith(s) is True:
                return line

def SeekNextNonEmptyLine(f):
    global gLineNumber
    while 1:
        line = f.readline()
        gLineNumber +=1
        if not line:
            return None
        if len(line) > 2:
            return line

# "Report reference: , OIE Ref: 10146, Report Date: 10/01/2011, Country: Bangladesh"
def ExtractCountryReportDate( line ):

    tmp = line.split(',')

    d = str( tmp[2].split(':')[1] ).strip()
    t = datetime.datetime.strptime(d, "%d/%m/%Y")
    d = t.strftime("%Y-%m-%d")

    c = str( tmp[3].split(':')[1] ).strip().replace('\t', ' ')  # no TAB chars please!

    return [d,c]




# Extract Outbreak Data from this format
#
# Outbreak (other report - submitted)
# Division                     District                        Sub-district                     Unit Type                      Location                                   Latitude                  Longitude                            Start date                   End Date
# DHAKA                        Jamalpur                        Sharishabari                     Farm                           Naz poultry farm                               24,333                    88,91 05/02/2007                               26/03/2007
# Species                                   Measuring units                                                         Susceptible                           Cases                          Deaths                               Destroyed                             Slaughtered
# Birds                                     Animals                                                                         1000                             13                                13                                        987                                 0

def ProccessTextFile(filename, uri, errors):

    data = []

    f = open(filename, "r")

    global gLineNumber
    gLineNumber = 0

    # Find Report Date &&  Country  => "Report reference: , OIE Ref: 10146, Report Date: 10/01/2011, Country: Bangladesh"
    result = SeekToString(f, "Report reference" )
    if(result is None):
        print "Error in text cant find (Report reference) "
        return data # return empty data set.

    tmp = ExtractCountryReportDate(result)
    report_date = tmp[0]
    country     = tmp[1]



    # Find each section "Outbreak (other report - submitted)"

    while( SeekToString(f, "Outbreak (") is not None ):

        outbreakData = ExtractOutBreakData(f, errors)
        if( outbreakData is not None ):
            outbreakData.country        = country
            outbreakData.report_date    = report_date
            outbreakData.uri            = uri
            data.append(outbreakData)

            ##print outbreakData.ToTsvString()

    f.close()

    ##for er in errors:
       ## print er

    return data



def ExtractOutBreakData(f, errors):
    global gLineNumber


    outbreakData = OutbreakData()

    # move to the next header # Skip first header line
    ##if( SeekToStringTup(f, ("State","Province","Division", "Zone") ) is None ):

    if( SeekNextNonEmptyLine(f) is None ):
        msg = "Error in text line %s  cant find (State,Province,Division, Zone) " % str(gLineNumber)
        errors.append(msg)
        print msg
        return None

    firstDataLine = f.readline()  # first data line
    gLineNumber += 1


    # Pull out the Lat and Long values.
    lat_long_pattern  = "\d*,\d*"  # re.findall
    result = re.findall(lat_long_pattern, firstDataLine)

    if(len(result) < 2):
        msg  = "Error in text line %d finding lat long:\n%s"  % ( gLineNumber , firstDataLine)
        errors.append(msg)
        print msg
        return None

    outbreakData.latitude   = result[0]
    outbreakData.longitude  = result[1]



    # Skip to 2nd header line
    if( SeekToStringTup(f,  ("Species")) is None ):
        msg = "Error in text line %d Can not seek to 'Species' header : " %  gLineNumber
        errors.append(msg)
        print msg
        return None

    secoundDataLine = f.readline()  # reas 2nd data line
    gLineNumber += 1

    result = secoundDataLine.split()

    try:
        outbreakData.cases  = ConvertToNan(result[3])
        outbreakData.deaths = ConvertToNan(result[4])
    except:
        msg = "Error in text line %d could not parse cases & death' :\n%s " %  (gLineNumber, secoundDataLine)
        errors.append(msg)
        print msg
        return None

##    result = re.findall("\d+", secoundDataLine)

##    if(len(result) < 2):
##        print "Error in text line %s finding cases and deaths: " % str(lineNumber) , secoundDataLine
##        return None
##    elif( len(result) == 2):
##        print "Guessing text line %d cases(%s) and deaths(%s): " % ( lineNumber ,  result[0],  result[1]), secoundDataLine
##        outbreakData.cases  = result[0]
##        outbreakData.deaths = result[1]
##    else:
##        outbreakData.cases  = result[1]
##        outbreakData.deaths = result[2]

    # We made it found all the field values.
    return outbreakData


# we may missing numbers as ...
# ['Birds', 'Animals', '...', '...', '1', '...', '...']
def ConvertToNan(s):
    if s == '...': return "NaN"
    return s



if __name__ == '__main__':
    main()
