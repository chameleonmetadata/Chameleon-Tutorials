#### 
####----- Python Routine Initiation
#### 

import datetime

print ('<-<-<-<-<-<-<-<-<-<---------- P Y T H O N   S C R I P T ---------->->->->->->->->->->')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>   Chameleon Tutorial DSB-3-LAB-1-A: Download Documents from SEC Edgar     <<<<<')
print ('>>>>> ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ <<<<<')
print ('>>>>>  Extract Filings URLs directly from SEC Edgar  (10-K, 10-Q, 13-F, etc.)   <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('-----                                                                           -----')
start_time = datetime.datetime.now()
print ('----- Start Time: ', start_time, '                                  -----')
print ('-----                                                                           -----')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>--------------------  E X E C U T I O N   B E G I N S  --------------------<<<<< \n')

#### 
####----- Python Environment Division
#### 

import os
import pprint
import urllib.request
from bs4 import BeautifulSoup

#### 
####----- Working Storage Section (WSS)
#### 

####----- DISCLAIMER
#-------- 
#-------- Don't read anything into the fact that Wave Life Sciences is used in this student lab.
#-------- They were only selected as the target company because they were at the top of Edgar's 
#-------- most recent filings list the day I wrote this student lab - Selecting Wave Life Sciences was completely random.
#-------- 
#-------- Change the sec_company_cik, sec_company_name and sec_company_sic below to retrieve any other company's SEC filings.
#-------- 

####
##----------------- WSS Static Values Variables
#### 

#~~~ Set the prefix value I will use to build the name of the output directory to which files will be written when this routine executes.
doc_buttons_write_dir_perfix = 'c:/DMZ_FTP-Receiving/sec-edgar'

#~~~ Set the prefix value I will use to build the URL and request to send to the SEC Edgar system
sec_url_prefix               = 'https://www.sec.gov'

#~~~ Initialize other variables used to build directory and file names based on request sent to Edgar
local_DMZ_sec_cik_dir        = ''
local_DMZ_sec_cik_secNum_dir = ''
local_DMZ_write_location     = ''

doc_buttons_write_dir        = ''
doc_buttons_write_location   = ''

##------------------------ WSS SEC Edgar Manditory
#~~~ 
sec_company_cik              = '0001631574'      #-- &CIK URL variable - Make sure to include leading zeros

##------------------------ WSS SEC Edgar Optional

filing_type                  = '10-K'            #-- &type URL variable
#--- until_data                   = '20181231'   #-- &dateb URL variable
#--- filing_count                 = '15'         #-- &count URL variable

####
##----------------- WSS Dynamic Values Variables
#### 

datetime_dir_suffix        = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
 
sec_edgar_request_url      = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + sec_company_cik + '&type=' + filing_type 

doc_buttons_write_dir      = doc_buttons_write_dir_perfix + '/' + sec_company_cik + '/'

####
##----------------- Dictionaries, Data Frames, Files Etc.
#### 

sec_edgar_request_metadata = []
sec_edgar_doc_buttons_list = []


#~~~ SEND REQUEST to and RECEIVE PAYLOAD from SEC Edgar
with urllib.request.urlopen(sec_edgar_request_url) as edgar_request_url:
    edgar_request_url_read = edgar_request_url.read() 
    
#~~~ Parse the PAYLOAD from SEC Edgar using BeautifulSoup's HTML parser    
    edgar_request_soup = BeautifulSoup(edgar_request_url_read, "html.parser")
    
#~~~ Find all tables in the HTML reply PAYLOAD
    edgar_request_soup_tables = edgar_request_soup.find_all('table')
    
#~~~ Although only one table is expected in the HTML reply PAYLOAD, it's always good practice to use a loop
    for soup_table in edgar_request_soup_tables:
#~~~ Find all the 'documentsbutton' tags (which have the target URL as a sub-tag) in the HTML reply PAYLOAD
        href_list = edgar_request_soup.find_all('a', id='documentsbutton')
#~~~ Loop through all the 'documentsbutton' tags found in the HTML reply PAYLOAD - This will vary with each request
        for href in href_list:
#~~~ Extract the URL from all the 'documentsbutton' tags found
            doc_button_href = href['href']
#~~~ Build a complete URL by adding the 'documentsbutton' tags (which only have the last part of the URL) to the 'sec_url_prefix' variable set above.            
            sec_edgar_url = (sec_url_prefix + doc_button_href)
#~~~ If the full URL is not already in the dictionary (we don't want duplicates), add it to the dictionary
            if sec_edgar_url not in sec_edgar_doc_buttons_list:
                sec_edgar_doc_buttons_list.append(sec_edgar_url)
#~~~ Print the REQUEST and REPLY to and from Edgar to the console so the operator can review the execution statistics                         
    print('Request-1 Message Sent to SEC Edgar:', sec_edgar_request_url, '\n')
    print('Request-1 Reply Received from SEC Edgar:')
    pprint.pprint(sec_edgar_doc_buttons_list)
    print('_____________________________________________________________________ \n')

#~~~ Set the names for the Directory, Request File and Reply File Names
doc_buttons_write_dir            = doc_buttons_write_dir_perfix + '/' + sec_company_cik 
doc_buttons_write_reply_file     = doc_buttons_write_dir_perfix + '/' + sec_company_cik + '/' + 'edgar-reply-' + datetime_dir_suffix + '.txt' 
doc_buttons_write_request_file   = doc_buttons_write_dir_perfix + '/' + sec_company_cik + '/' + 'edgar-request-' + datetime_dir_suffix + '.txt' 

#~~~ Create a sub-folder in the DMZ with the name equal to the variable used for 'sec_company_cik' if it doesn't exist
if not os.path.exists(doc_buttons_write_dir):
    print('PATH Not Found:     ', doc_buttons_write_dir)
    try:
        os.makedirs(doc_buttons_write_dir)
        print('Directory Created:  ', doc_buttons_write_dir)
    except:
        print('ERROR: Creating Directory')
else:
    print('Directory Already Exists')

#~~~ Populate the dictionary 'sec_edgar_request_metadata' to be used when writing the doc_buttons_write_request_file
sec_edgar_request_metadata.append('Chameleon Tutorial DSB-3-LAB-1-A')
sec_edgar_request_metadata.append(str(start_time))
sec_edgar_request_metadata.append(sec_company_cik)
sec_edgar_request_metadata.append(sec_edgar_request_url)
sec_edgar_request_metadata.append(doc_buttons_write_dir)
sec_edgar_request_metadata.append(doc_buttons_write_request_file)
sec_edgar_request_metadata.append(doc_buttons_write_reply_file)

#~~~ Print items in dictionary 'sec_edgar_request_metadata' to the console so the operator can review the request details
print('sec_edgar_request_metadata:')
pprint.pprint(sec_edgar_request_metadata)

#~~~ Write dictionary 'sec_edgar_request_metadata' items to the doc_buttons_write_request_file
with open(doc_buttons_write_request_file, 'w') as f_request:
    for request_metadata_item in sec_edgar_request_metadata:
        f_request.write(request_metadata_item)
        f_request.write(' \n')
    
f_request.close()

#~~~ Write URL's collected above to the doc_buttons_write_reply_file
with open(doc_buttons_write_reply_file, 'w') as f_reply:
    for sec_edgar_doc_buttons_url in sec_edgar_doc_buttons_list:
        f_reply.write(sec_edgar_doc_buttons_url)
        f_reply.write(' \n')
        
f_reply.close()

#### 
####----- Python Routine Termination
#### 

print (' \n')
print ('<-<-<-<-<-<-<-<-<-<----  E X E C U T I O N   C O M P L E T E  ---->->->->->->->->->->')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>   Chameleon Tutorial DSB-3-LAB-1-A: Download Documents from SEC Edgar     <<<<<')
print ('>>>>> ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('-----                                                                           -----')
end_time = datetime.datetime.now()
print ('----- End Time:   ', end_time, '                                  -----')
print ('----- Start Time: ', start_time, '                                  -----')
execution_time = end_time - start_time
print ('----- ---------------------------------------', '                                  -----')
print ('----- Execution Time:         ', execution_time, '                                  -----')
print ('-----                                                                           -----')
print ('>>>>>                                                                           <<<<<')
print ('<-<-<-<-<-<-<-<-<-<----  E X E C U T I O N   C O M P L E T E  ---->->->->->->->->->->')
# 
#############################################################################################################################
#---------------------------------------------   MIT Creative Commons License   ---------------------------------------------
#---------------------------------------------      Chameleon-DSB-3-LAB-1-A     ---------------------------------------------
#---------------------   Copyright © 2018 Dynamic Database Support Systems and ChameleonMetadata.com    --------------------- 
#----------------------------------------------------------------------------------------------------------------------------
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated  
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
#  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
#  to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#  1) The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#  2) The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to 
#     the warranties of merchantability, fitness for a particular purpose and noninfringement. 
#     In no event shall the authors or copyright holders be liable for any claim, damages or other liability, 
#     whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software 
#     or the use or other dealings in the Software.
#############################################################################################################################