#
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

import os
import pprint
import urllib.request
from bs4 import BeautifulSoup

doc_buttons_write_dir_perfix = 'c:/DMZ_FTP-Receiving/sec-edgar'

sec_url_prefix               = 'https://www.sec.gov'

local_DMZ_sec_cik_dir        = ''
local_DMZ_sec_cik_secNum_dir = ''
local_DMZ_write_location     = ''

doc_buttons_write_dir        = ''
doc_buttons_write_location   = ''

sec_company_cik              = '0001631574'

filing_type                  = '10-K'

datetime_dir_suffix        = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
 
sec_edgar_request_url      = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + sec_company_cik + '&type=' + filing_type 

doc_buttons_write_dir      = doc_buttons_write_dir_perfix + '/' + sec_company_cik + '/'

sec_edgar_request_metadata = []
sec_edgar_doc_buttons_list = []

with urllib.request.urlopen(sec_edgar_request_url) as edgar_request_url:
    edgar_request_url_read = edgar_request_url.read() 
    
    edgar_request_soup = BeautifulSoup(edgar_request_url_read, "html.parser")
    
    edgar_request_soup_tables = edgar_request_soup.find_all('table')
    
    for soup_table in edgar_request_soup_tables:
        href_list = edgar_request_soup.find_all('a', id='documentsbutton')
        for href in href_list:
            doc_button_href = href['href']
            sec_edgar_url = (sec_url_prefix + doc_button_href)
            if sec_edgar_url not in sec_edgar_doc_buttons_list:
                sec_edgar_doc_buttons_list.append(sec_edgar_url)
    print('Request-1 Message Sent to SEC Edgar:', sec_edgar_request_url, '\n')
    print('Request-1 Reply Received from SEC Edgar:')
    pprint.pprint(sec_edgar_doc_buttons_list)
    print('_____________________________________________________________________ \n')

doc_buttons_write_dir            = doc_buttons_write_dir_perfix + '/' + sec_company_cik 
doc_buttons_write_reply_file     = doc_buttons_write_dir_perfix + '/' + sec_company_cik + '/' + 'edgar-reply-' + datetime_dir_suffix + '.txt' 
doc_buttons_write_request_file   = doc_buttons_write_dir_perfix + '/' + sec_company_cik + '/' + 'edgar-request-' + datetime_dir_suffix + '.txt' 

if not os.path.exists(doc_buttons_write_dir):
    print('PATH Not Found:     ', doc_buttons_write_dir)
    try:
        os.makedirs(doc_buttons_write_dir)
        print('Directory Created:  ', doc_buttons_write_dir)
    except:
        print('ERROR: Creating Directory')
else:
    print('Directory Already Exists')

sec_edgar_request_metadata.append('Chameleon Tutorial DSB-3-LAB-1-A')
sec_edgar_request_metadata.append(str(start_time))
sec_edgar_request_metadata.append(sec_company_cik)
sec_edgar_request_metadata.append(sec_edgar_request_url)
sec_edgar_request_metadata.append(doc_buttons_write_dir)
sec_edgar_request_metadata.append(doc_buttons_write_request_file)
sec_edgar_request_metadata.append(doc_buttons_write_reply_file)

print('sec_edgar_request_metadata:')
pprint.pprint(sec_edgar_request_metadata)

with open(doc_buttons_write_request_file, 'w') as f_request:
    for request_metadata_item in sec_edgar_request_metadata:
        f_request.write(request_metadata_item)
        f_request.write(' \n')
    
f_request.close()

with open(doc_buttons_write_reply_file, 'w') as f_reply:
    for sec_edgar_doc_buttons_url in sec_edgar_doc_buttons_list:
        f_reply.write(sec_edgar_doc_buttons_url)
        f_reply.write(' \n')
        
f_reply.close()

print (' \n')
print ('<-<-<-<-<-<-<-<-<-<----  E X E C U T I O N   C O M P L E T E  ---->->->->->->->->->->')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>    Chameleon Tutorial DSB-3-LAB-1: Download Documents from SEC Edgar      <<<<<')
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