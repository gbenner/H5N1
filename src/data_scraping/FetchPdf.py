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


import datetime
import os
import re, util
import BeautifulSoup
from urllib2 import Request, urlopen, URLError, HTTPError


def main():


    ##<ul class="oe_pressReleasesList">
    ##		<table id="ai_official_reports">
    ##            <tr>
    ##                <td><a href="http://web.oie.int/wahis/reports/en_fup_0000010121_20110102_154206.pdf" target="_top" title="Follow-up report No. 2">Follow-up report No. 2</a>&nbsp;&nbsp;<a style="color:#FAF9F8" name="c27054">27054</a></td>

    base= "http://www.oie.int/animal-health-in-the-world/update-on-avian-influenza/"    # 2011 - 2004
    # variation http://www.oie.int/animal-health-in-the-world/update-on-avian-influenza/2011
    ## http://web.oie.int/wahis/reports/en_fup_0000010289_20110304_170141.pdf


    # Make a new directory for this run with date as name.
    tm = datetime.datetime.now()
    datadir = "../data/" + tm.strftime("%Y-%m-%d_t%H_%M_%S")
    #datadir = "D:\\School\\171\\fp\\data\\" + str(tm)

    EnsureDirectory(datadir)



    # keep going until we find a page that doesn't have any job postings
    # -- Loop on pages.
    for yr in range(4,8):
        print "Year : ", yr

        if( yr < 10):
            yearPostFix = "200" + str(yr)
        else:
            yearPostFix = "20" + str(yr)

        url = base + yearPostFix
        print "PAGE -----------------------", url

        # Find the pdf file links
        soup = util.mysoupopen(url)

        # find table with the pdf links <table id="ai_official_reports">
        linkTable = soup.findAll("table", {"id":"ai_official_reports"})

        if(len(linkTable) == 0):
            print "Did not find any links!"
            break;


        anchorList = soup.findAll("a", {"target":"_top"})

        # Break out of page loop when there are no job details links.
        if(len(anchorList) == 0):
            print "No pdf links found???"
            break

        # create a directory for this year.
        yearDir = datadir + "/" + yearPostFix + "/" ;
        EnsureDirectory(yearDir)
        # -- Loop on Details links. <a id="" class="detailsLink" ..>
        for anchor in anchorList:
            href =  anchor['href']
            print href
            download(href, yearDir)


        pass


##def download(url, dir):
##	"""Copy the contents of a file from a given URL
##	to a local file.
##	"""
##	import urllib
##	webFile = urllib.urlopen(url, mode='rb')
##	localFile = open(dir + url.split('/')[-1], 'wb')
##	localFile.write(webFile.read())
##	webFile.close()
##	localFile.close()

def download(url, dir):
    #create the url and the request
    req = Request(url)

    # Open the url
    try:
        localname = dir + url.split('/')[-1]

        f = urlopen(req)
        print "downloading " + url

         # Open our local file for writing
        local_file = open(localname, "wb")  # Important PDF must use binary read write!!!

        #Write to our local file
        local_file.write(f.read())
        local_file.close()
        f.close()
    #handle errors
    except HTTPError, e:
        print "HTTP Error:",e.code , url
    except URLError, e:
        print "URL Error:",e.reason , url



def EnsureDirectory(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        if os.path.exists(dirname):
            # We are nearly safe
            pass
        else:
            # There was an error on creation, so make sure we know about it
            raise

if __name__ == '__main__':
    main()
