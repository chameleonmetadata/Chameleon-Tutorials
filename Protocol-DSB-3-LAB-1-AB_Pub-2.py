#
import datetime
#~~~ SET VARIABLES (BELOW) BEFORE EXECUTION (all variables are manditory except 'WSS SEC Edgar Optional' variables)
#~~~ #~~~ These variables also exist in-line within two scripts below but have been grouped here to make the lab less complex
#~~~ #~~~ To find them in their original position in the code, search for: #--- >>>>> COMMENTED OUT FOR LAB <<<<<
#~~~

storage_hierarchy_name            = 'windows-dsb-3-lab-1-b'

job_log_prefix                    = 'PROTOCOL-DSB-3-LAB-1'
job_log_suffix                    = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")

local_server_os                   = 'Windows'        #~~~~ Operating System (not used when building directory names)
local_server_ip                   = '192.168.1.114'  #~~~~ IP of Server which will store the Edgar datasets
local_root_drive                  = 'c'              #~~~~ Root drive on server which will store the Edgar datasets
dir_purpose                       = 'dmz-ftp'        #~~~~ 1st directory level (i.e. c:/dmz-ftp)
dir_source                        = 'sec-edgar'      #~~~~ 2nd directory level (i.e. c:/dmz-ftp/sec-edgar)
dir_src_sg1                       = 'cik'            #~~~~ 3rd directory level (i.e. c:/dmz-ftp/sec-edgar/cik)
dir_src_sg2                       = 'secNum'         #~~~~ 4th directory level (i.e. c:/dmz-ftp/sec-edgar/cik/secNum)

#~~~ #~~~ WSS SEC Edgar Manditory Variables

#~~~ #~~~ To look up the CIK for another company, visit this URL---> https://www.sec.gov/edgar/searchedgar/companysearch.html
sec_company_cik                = '0001631574'      #-- &CIK (Make sure to include leading zeros)

sec_edgar_request_url_prefix      = 'https://www.sec.gov'
sec_edgar_document_request_prefix = 'Archives/edgar/data'

#~~~ #~~~ WSS SEC Edgar Optional Variables

filing_type                    = '10-K'                  #-- &type URL variable (Filter on type of fileing)
until_date                     = ' '    #-- Format: 'YYYYMMDD'   #-- &dateb URL variable (Filter on maximum filing date requested)
filing_count                   = ' '    #-- Format: '99'         #-- &count URL variable (Limit the number of filings to return)

#~~~
#~~~ SET VARIABLES (ABOVE) BEFORE EXECUTION (all variables are manditory except 'WSS SEC Edgar Optional' variables)
#~~~ #~~~ These variables also exist in-line within two scripts below but have been grouped here to make the lab less complex
#~~~ #~~~ To find them in their original position in the code, search for: #--- >>>>> COMMENTED OUT FOR LAB <<<<<


import datetime
start_time = datetime.datetime.now()

print ('<-<-<----- C H A M E L E O N   M E T A D A T A   P Y T H O N   S C R I P T  ---->->->')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>               ROUTINE NAME:                   DSB-3-LAB-1-A               <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>               Start Time:       ', start_time, '              <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('<-<-<-<-<-<-<-<-<-------  E X E C U T I O N   B E G I N S  ------->->->->->->->->->-> \n')

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

####----- DISCLAIMER  - Selecting CIK '0001631574' was completely random.
#-------- It was only selected only company because they were at the top of Edgar's most recent filings list the day I wrote this student lab
#-------- Change the 'sec_company_cik' parameter below to retrieve a different company's SEC filings from Edgar.
#-------- 

#~~~ #~~~ Storage Hierarchy Variables

#--- >>>>> COMMENTED OUT FOR LAB <<<<<storage_hierarchy_name            = 'windows-dsb-3-lab-1-b'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<
#--- >>>>> COMMENTED OUT FOR LAB <<<<<job_log_prefix                    = 'DSB-3-LAB-1-A'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<job_log_suffix                    = job_log_suffix
#--- >>>>> COMMENTED OUT FOR LAB <<<<<
#--- >>>>> COMMENTED OUT FOR LAB <<<<<local_server_os                   = 'Windows'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<local_server_ip                   = '192.168.1.114'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<local_root_drive                  = 'c'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<dir_purpose                       = 'dmz-ftp'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<dir_source                        = 'sec-edgar'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<dir_src_sg1                        = 'cik'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<dir_src_sg2                        = 'secNum'

####
##----------------- WSS Static Values Variables
#### 

##------------------------ WSS SEC Edgar Manditory
#~~~ 
#--- >>>>> COMMENTED OUT FOR LAB <<<<<sec_company_cik                = '0001631574'      #-- &CIK URL variable - Make sure to include leading zeros
#--- >>>>> COMMENTED OUT FOR LAB <<<<<
#--- >>>>> COMMENTED OUT FOR LAB <<<<<sec_edgar_request_url_prefix      = 'https://www.sec.gov'

##------------------------ WSS SEC Edgar Optional

#--- >>>>> COMMENTED OUT FOR LAB <<<<<filing_type                    = '10-K'                  #-- &type URL variable (Filter on type of fileing)
#--- >>>>> COMMENTED OUT FOR LAB <<<<<until_date                     = ' '    #-- Format: 'YYYYMMDD'   #-- &dateb URL variable (Filter on maximum filing date requested)
#--- >>>>> COMMENTED OUT FOR LAB <<<<<filing_count                   = ' '    #-- Format: '99'         #-- &count URL variable (Limit the number of filings to return)


#~~~ Initialize other variables used to build directory and file names based on request sent to Edgar

local_DMZ_sec_cik_secNum_dir      = ' '

doc_buttons_write_dir             = ' '

doc_buttons_write_request_file    = ' '
doc_buttons_write_reply_file      = ' '

#### 
####----- Python Procedure Division
#### 

#~~~ Build the request (as a URL) which will be setn to the SEC Edgar System adding any optional parameters if provided above

if not filing_type                   == ' ':
    sec_edgar_request_url            = ('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' 
                                        + sec_company_cik 
                                        + '&type=' 
                                        + filing_type)
    
if not until_date                    == ' ':
    sec_edgar_request_url            = (sec_edgar_request_url 
                                        + '&dateb=' 
                                        + until_date)

if not filing_count                  == ' ':
    sec_edgar_request_url            = (sec_edgar_request_url 
                                        + '&count' 
                                        + filing_count)


#~~~ Build the directory prefix (for ease of reuse) and the directory into which the output files will be written
output_os_dir_purpose_src_prefix = (local_root_drive + ':' + '/' 
                                    + dir_purpose + '/'
                                    + dir_source)    
    
doc_buttons_write_dir            = (output_os_dir_purpose_src_prefix + '/' 
                                    + sec_company_cik + '/')
####
##----------------- Dictionaries, Data Frames, Files Etc.
#### 

sec_edgar_request_metadata     = []
sec_edgar_doc_buttons_list     = []


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
#~~~ Build a complete URL by adding the 'documentsbutton' tags (which only have the last part of the URL) to the 'sec_edgar_request_url_prefix' variable set above.            
            sec_edgar_url = (sec_edgar_request_url_prefix + doc_button_href)
#~~~ If the full URL is not already in the dictionary (we don't want duplicates), add it to the dictionary
            if sec_edgar_url not in sec_edgar_doc_buttons_list:
                sec_edgar_doc_buttons_list.append(sec_edgar_url)
#~~~ Print the REQUEST and REPLY to and from Edgar to the console so the operator can review the execution statistics                         
    print('Request Sent to SEC Edgar:', sec_edgar_request_url, '\n')
    print('Reply Received from SEC Edgar (Documents Button Target URL): ')
    pprint.pprint(sec_edgar_doc_buttons_list)
    print('_____________________________________________________________________ \n')

#~~~ Set the names for the Directory, Request File and Reply File Names
doc_buttons_write_dir            = (output_os_dir_purpose_src_prefix + '/' 
                                    + sec_company_cik) 

doc_buttons_write_reply_file     = (output_os_dir_purpose_src_prefix + '/' 
                                    + sec_company_cik + '/' 
                                    + job_log_prefix + '_'
                                    + job_log_suffix + '_Edgar.reply')

doc_buttons_write_request_file   = (output_os_dir_purpose_src_prefix + '/' 
                                    + sec_company_cik + '/' 
                                    + job_log_prefix + '_'
                                    + job_log_suffix + '_Edgar.request') 

#~~~ Create a sub-folder in the DMZ with the name equal to the variable used for 'sec_company_cik' if it doesn't exist
if not os.path.exists(doc_buttons_write_dir):
    print('PATH Not Found:     ', doc_buttons_write_dir)
    try:
        os.makedirs(doc_buttons_write_dir)
        print(' ~ Directory Created:  ', doc_buttons_write_dir)
    except:
        print(' ~ ERROR: Creating Directory')
else:
    print('Directory Already Exists: ', doc_buttons_write_dir)

#~~~ Populate the dictionary 'sec_edgar_request_metadata' to be used when writing the doc_buttons_write_request_file
sec_edgar_request_metadata.append('DSB-3-LAB-1-A')
sec_edgar_request_metadata.append(str(start_time))
sec_edgar_request_metadata.append(job_log_suffix)

sec_edgar_request_metadata.append(sec_company_cik)

if not filing_type == ' ':
    sec_edgar_request_metadata.append(filing_type)
else:
    sec_edgar_request_metadata.append('&type NONE')
    
if not until_date == ' ':
    sec_edgar_request_metadata.append(until_date)
else:
    sec_edgar_request_metadata.append('&dateb NONE')
    
if not filing_count == ' ':
    sec_edgar_request_metadata.append(filing_count)
else:
    sec_edgar_request_metadata.append('&count NONE')

sec_edgar_request_metadata.append(sec_edgar_request_url)
sec_edgar_request_metadata.append(storage_hierarchy_name)
sec_edgar_request_metadata.append(doc_buttons_write_dir)
sec_edgar_request_metadata.append(doc_buttons_write_request_file)
sec_edgar_request_metadata.append(doc_buttons_write_reply_file)

#~~~ #~~~ Storage Hierarchy Console Messages - So the operator knows which target directories were used to store any files created

print('_____________________________________________________________________ \n')
print('Storage Hierarchy (' + storage_hierarchy_name + ') with Nodes Set As:')
print(' ~ local_server_os   = ', local_server_os)
print(' ~ ~ local_server_ip   = ', local_server_ip)
print(' ~ ~ ~ local_root_drive   = ', local_root_drive)
print(' ~ ~ ~ ~ dir_purpose        = ', dir_purpose)
print(' ~ ~ ~ ~ ~ dir_source         = ', dir_source)
print(' ~ ~ ~ ~ ~ ~ dir_src_sg1        = ', dir_src_sg1)
print(' ~ ~ ~ ~ ~ ~ ~ dir_src_sg2        = ', dir_src_sg2)
print(' ~ ~ ~ ~ ~ ~ ~ ~ JOB ID             = ', job_log_suffix)
print('_____________________________________________________________________ \n')

#~~~ Print items in dictionary 'sec_edgar_request_metadata' to the console so the operator can review the request details
print('sec_edgar_request_metadata:')
pprint.pprint(sec_edgar_request_metadata)

#~~~ Write dictionary 'sec_edgar_request_metadata' items to the doc_buttons_write_request_file
with open(doc_buttons_write_request_file, 'w') as file_request:
    for request_metadata_item in sec_edgar_request_metadata:
        file_request.write(request_metadata_item)
        file_request.write(' \n')
    
file_request.close()

#~~~ Write URL's collected above to the doc_buttons_write_reply_file
with open(doc_buttons_write_reply_file, 'w') as f_reply:
    for sec_edgar_doc_buttons_url in sec_edgar_doc_buttons_list:
        f_reply.write(sec_edgar_doc_buttons_url)
        f_reply.write(' \n')
        
f_reply.close()

#### 
####----- Python Routine Termination
#### 

end_time = datetime.datetime.now()
execution_time = end_time - start_time

print (' \n')
print ('<-<-<-<-<-<-<-<-<-<----  E X E C U T I O N   C O M P L E T E  ---->->->->->->->->->->')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>               R O U T I N E ................. DSB-3-LAB-1-A               <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>         End Time: ', end_time, '                            <<<<<')
print ('>>>>>       Start Time: ', start_time, '                            <<<<<')
print ('>>>>>                    ~~~~~~~~~~~~~~~~~~~~~~~~~~', '                            <<<<<')
print ('>>>>>   Execution Time:             ', execution_time, '                            <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('<-<-<-<-<-<-<-<-<-<----  E X E C U T I O N   C O M P L E T E  ---->->->->->->->->->->')
print (' ')
print('_____________________________________________________________________ \n')
#
#
#
####----- Chameleon Metadata Student Lab DSB-3-LAB-1-B
#
import datetime
start_time = datetime.datetime.now()

print ('<-<-<----- C H A M E L E O N   M E T A D A T A   P Y T H O N   S C R I P T  ---->->->')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>               ROUTINE NAME:                   DSB-3-LAB-1-B               <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>               Start Time:       ', start_time, '              <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('<-<-<-<-<-<-<-<-<-------  E X E C U T I O N   B E G I N S  ------->->->->->->->->->-> \n')

#### 
####----- Python Environment Division
#### 

import os
import pprint
import requests
import urllib.request
from bs4 import BeautifulSoup

#### 
####----- Working Storage Section (WSS)
#### 

#~~~ DEFINITION: A "Chameleon Metadata Protocol" is a collection of routines executed together and in sequence as a workflow.
#~~~
#~~~ 'job_log_suffix' is used so a common "JOB Prefix" can be shared by all routines run together as a protocol.
#~~~ 
#~~~ However, if that variable was NOT set by a past step, this script will ABEND. That's why we try a "DUMMY SET" to see if it exists

try:
    wss_check_protocol_datetime_exists    = job_log_suffix
except:
    job_log_suffix                        = ' '
    
#~~~ Now the variable 'job_log_suffix' may be set regardless of its state before this script executes
if not job_log_suffix       == ' ':
    print('job_log_suffix IN-MEMORY from past step:', job_log_suffix)
    print(' ~ Setting JOB ID (job_log_suffix) to: ', job_log_suffix, ' \n')
else:
    job_log_suffix          = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    print('job_log_suffix NOT SET by previous step - Initializing Now As: ', job_log_suffix)
    print(' ~ Setting JOB ID (job_log_suffix) to: ', job_log_suffix, ' \n')

#~~~ #~~~ Chameleon Metadata Storage Hierarchy Variables

#--- >>>>> COMMENTED OUT FOR LAB <<<<<storage_hierarchy_name            = 'windows-dsb-3-lab-1-b'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<
#--- >>>>> COMMENTED OUT FOR LAB <<<<<job_log_prefix                    = 'DSB-3-LAB-1-A'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<job_log_suffix                    = job_log_suffix
#--- >>>>> COMMENTED OUT FOR LAB <<<<<
#--- >>>>> COMMENTED OUT FOR LAB <<<<<local_server_os                   = 'Windows'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<local_server_ip                   = '192.168.1.114'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<local_root_drive                  = 'c'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<dir_purpose                       = 'dmz-ftp'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<dir_source                        = 'sec-edgar'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<dir_src_sg1                        = 'cik'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<dir_src_sg2                        = 'secNum'

####
##----------------- WSS Static Values Variables
#### 

##------------------------ WSS SEC Edgar Manditory
#~~~ 
#--- >>>>> COMMENTED OUT FOR LAB <<<<<sec_company_cik                = '0001631574'      #-- &CIK URL variable - Make sure to include leading zeros
#--- >>>>> COMMENTED OUT FOR LAB <<<<<
#--- >>>>> COMMENTED OUT FOR LAB <<<<<sec_edgar_request_url_prefix      = 'https://www.sec.gov'

##------------------------ WSS SEC Edgar Optional

#--- >>>>> COMMENTED OUT FOR LAB <<<<<filing_type                    = '10-K'                  #-- &type URL variable (Filter on type of fileing)
#--- >>>>> COMMENTED OUT FOR LAB <<<<<until_date                     = ' '    #-- Format: 'YYYYMMDD'   #-- &dateb URL variable (Filter on maximum filing date requested)
#--- >>>>> COMMENTED OUT FOR LAB <<<<<filing_count                   = ' '    #-- Format: '99'         #-- &count URL variable (Limit the number of filings to return)

#~~~ #~~~ SEC Edgar-related URL's and Prefixes

#--- >>>>> COMMENTED OUT FOR LAB <<<<<sec_edgar_request_url_prefix      = 'https://www.sec.gov'
#--- >>>>> COMMENTED OUT FOR LAB <<<<<sec_edgar_document_request_prefix = 'Archives/edgar/data'

sec_edgar_document_request_url    = ' '

#~~~ #~~~ Windows Directories & File Variables (Note alignment of variable names to the storage hierarchy being used)

output_os_dir_purpose_src_prefix  = ' '
output_os_dir_src_sg2_job         = ' '

output_os_hadoop_mkdir_cmds_file  = ' '
output_os_hadoop_copy_cmds_file   = ' '

output_os_replyDocButtons_file    = ' '
output_os_replyDocsMetadata_file  = ' '
output_os_replyDocsURL_file       = ' '
output_os_replyDocument_file      = ' '

#~~~ #~~~ Hadoop Directories & File Variables

hadoop_target_dir_purpose         = dir_purpose

hadoop_purpose_source1_prefix     = ' '
hadoop_mkdir_cmd_src1_prefix      = ' '
hadoop_mkdir_src_sg1_prefix       = ' '
hadoop_mkdir_src_sg2              = ' '

hadoop_copy_dir_src_sg2_job       = ' '
hadoop_copyFromLocal_prefix       = ' '

#~~~ #~~~ Filing and Document Metadata Variables

wss_enumerated_edgar_info         = ' '
wss_edgar_filing_date             = ' '
wss_edgar_filing_accepted         = ' '
wss_edgar_filing_documents        = ' '
wss_edgar_filing_period_of_rpt    = ' '

metadata_document_secNum          = ' '
metadata_document_description     = ' '
metadata_document_name            = ' '
metadata_document_size            = ' ' 

wss_doc_description               = ' '
wss_document_size                 = ' ' 

wss_hadoop_copy_command           = ' '

edgar_form_page_metadata_count    = 0
edgar_secNum_count                = 0

####
##----------------- Dictionaries, Data Frames, Files Etc.
#### 

#~~~ #~~~ Initialize all the Python dictionaries
#~~~ #~~~ 
#~~~ #~~~ #~~~ Dictionary 'sec_edgar_doc_buttons_list' was already set during DSB-3-LAB-1-A. 
#~~~ #~~~ #~~~ To run stand-alone, LAB-1-B could also READ the 'Edgar.reply' file created when LAB-1-A was executed  
#~~~ #~~~ #~~~ However, in a Learning Lab environment, it's less complex to have students execute LAB-1-A first

# sec_edgar_doc_buttons_list        = []

reply_metadata_list               = []
document_metadata_list            = []

button_page_metadata              = []

sec_edgar_doc_infoHeads           = []
sec_edgar_doc_infos               = []
sec_edgar_document_urls           = []

hadoop_mkdir_command_list         = []
hadoop_copy_command_list          = []

#### 
####----- Python Procedure Division
#### 

#~~~ Build the directories which will be used to store the outcome (reply data and job logs) of this Python routine

hadoop_purpose_source1_prefix     = (dir_purpose + '/'
                                     + dir_source)

output_os_dir_purpose_src_prefix  = (local_root_drive + ':' + '/'
                                     + hadoop_purpose_source1_prefix)

output_os_directory_cik_prefix    = (local_root_drive  + ':' + '/'
                                     + hadoop_purpose_source1_prefix + '/'
                                     + sec_company_cik)

hadoop_copyFromLocal_prefix       = ('bin/hadoop fs -copyFromLocal "//' 
                                     + local_server_ip + '/'
                                     + local_root_drive + '/' 
                                     + hadoop_purpose_source1_prefix + '/' ) 

hadoop_mkdir_cmd_src1_prefix      = ('bin/hadoop fs -mkdir /'
                                     + hadoop_purpose_source1_prefix + '/')
    
output_os_replyDocButtons_file    = (output_os_directory_cik_prefix + '/'
                                     + job_log_prefix + '_'
                                     + job_log_suffix + '_replyDocButtons.metadata')

output_os_hadoop_mkdir_cmds_file  = (output_os_directory_cik_prefix + '/'
                                     + job_log_prefix + '_'
                                     + job_log_suffix + '_mkdir.hadoop')

#~~~ IMPORTANT HEADS-UP: Python dictionary 'sec_edgar_doc_buttons_list', already in memory after executing LAB-1-A, is used below.
#~~~
#~~~ In 'real life', Protocol Scripts should READ the files created by previous steps rather than use in-memory dictionaries. 
#~~~ That way, after each step runs, its files act quiesce points in case any subsequent steps in the Protocol's workflow ABEND.
#~~~ But this is just a Student Lab, so we'll read the 'Documents Button' URL's from the Python dictionary to make things simpler.

for sec_edgar_doc_button_url in sec_edgar_doc_buttons_list:
    with urllib.request.urlopen(sec_edgar_doc_button_url) as edgar_request_url:
        edgar_request_url_read = edgar_request_url.read()

#~~~ Each time a new Documents Button URL is visited, reinitialize the form-specific Python dictionaries
    sec_edgar_doc_infoHeads         = []
    sec_edgar_doc_infos             = []

#~~~ 
#~~~ BeautifulSoup Configuration

    soup_edgar_request              = BeautifulSoup(edgar_request_url_read, "html.parser")
    
    soup_edgar_companyInfo          = soup_edgar_request.find_all('div', {"class": "companyInfo"})
    soup_edgar_companyNames         = soup_edgar_request.find_all('span', {"class": "companyName"})
    soup_edgar_identInfos           = soup_edgar_request.find_all('p', {"class": "identInfo"})
    soup_edgar_secNums              = soup_edgar_request.find_all('div', id='secNum')
    soup_edgar_formNames            = soup_edgar_request.find_all('div', id='formName')
    soup_edgar_infoHeads            = soup_edgar_request.find_all('div', {"class": "infoHead"})
    soup_edgar_infos                = soup_edgar_request.find_all('div', {"class": "info"})
    soup_document_format_files      = soup_edgar_request.find_all('div', {"summary": "Document Format Files"})
    soup_edgar_request_tables       = soup_edgar_request.find_all('table')

#~~~ Get the company name from the Edgar Documents Button target URL which has a list of documents making up a 'form' (10-K, 13-F, etc.)
    for edgar_companyName in soup_edgar_companyNames:
        edgar_companyName_text      = edgar_companyName.text
        edgar_companyName_text      = edgar_companyName_text.replace('\n', '') 
        edgar_companyName_text      = edgar_companyName_text.replace(' (see all company filings)', '')

#~~~ Get the SEC Accession Number, which is an identifier given to each individual form filing (i.e. 10-K's get different secNum each year they are filed)
    for edgar_secNum in soup_edgar_secNums:   
        edgar_secNum                      = edgar_secNum
        edgar_secNum_only                 = (edgar_secNum.text[19:])
        
        edgar_secNum_only                 = edgar_secNum_only.replace(' ', '')
        edgar_secNum_only                 = edgar_secNum_only.replace('\n', '')
        
        edgar_secNum_clean                = edgar_secNum_only.replace('-', '')

        
#~~~ Because the 'secNum' is used as a sub-directory name whilst building target directories, the directory names are rebuilt for each form

        output_os_dir_src_sg2_job         = (output_os_dir_purpose_src_prefix + '/'
                                             + sec_company_cik + '/'
                                             + edgar_secNum_only + '/'
                                             + job_log_suffix)
        
        hadoop_target_dir_purpose         = (hadoop_purpose_source1_prefix + '/'
                                             + sec_company_cik + '/'
                                             + edgar_secNum_only + '/'
                                             + job_log_suffix)
        
#~~~ Build the full Hadoop 'mkdir' and 'copyFromLocal' HDFS commands

        hadoop_mkdir_src_sg2              = (hadoop_mkdir_cmd_src1_prefix + '/'
                                             + sec_company_cik + '/'
                                             + edgar_secNum_only + '/'
                                             + job_log_suffix)
        
        hadoop_copy_dir_src_sg2_job       = (hadoop_copyFromLocal_prefix
                                             + sec_company_cik + '/'
                                             + edgar_secNum_only + '/'
                                             + job_log_suffix +'"' + ' ') #~~~ Don't forget the trailing blank space             

#~~~ Once the target JOB directory name is known, build a directory with that name if it doesn't already exists

#~~~ REMEMBER: By storing in the 'job_log-suffix' sub-directory (a child of the secNum diretory), we can do many runs per secNUM.

        if not os.path.exists(output_os_dir_src_sg2_job):
            print('PATH Not Found:     ', output_os_dir_src_sg2_job)
            try:
                os.makedirs(output_os_dir_src_sg2_job)
                print(' ~ Directory Created:  ', output_os_dir_src_sg2_job, ' \n')
            except:
                print('-+-> ERROR: Creating Directory: ', output_os_dir_src_sg2_job)                
        else:
            print('Directory Already Exists: ', output_os_dir_src_sg2_job, ' \n')

#~~~ These next BeautifulSoup bits use multiple BeautifulSoup config's (defined above) to collect the form page's headers and details

#~~~ the formName (10-K, 13-F, etc.)
    for edgar_formName in soup_edgar_formNames:
        edgar_formName_only           = (edgar_formName.text)
        edgar_formName_only           = edgar_formName_only.replace('\n', '')

#~~~ the headers from the page containing values like 'filing_date', 'SEC Accession Number', 'Period of Report', etc.
    for edgar_infoHead in soup_edgar_infoHeads:
        edgar_infoHead_only           = (edgar_infoHead.text)

#~~~ remove the line-break from each header because errant HTML tags can mess with Natural Language Processing (NLP) tasks
        edgar_infoHead_only           = edgar_infoHead_only.replace('\n', '')
        sec_edgar_doc_infoHeads.append(edgar_infoHead_only)

#~~~ Now, get each page headers' text values
    for edgar_info in soup_edgar_infos:
        sec_edgar_doc_infos.append(edgar_info.text)
        
#~~~ Next, we loop through all the 'Infos' and align their text values with their corrisponding page headers (infoHeads)            
    for i_infoHead, enumerated_doc_infoHead in enumerate(sec_edgar_doc_infoHeads):
        enumerated_edgar_info         = sec_edgar_doc_infos[i_infoHead] 

#~~~ #~~~ REMEMBER: We first loop through each URL for each Documents Button. Then we'll lopp though each dataset at each page

#~~~ Store all the metadata from each Form Page pointed to by each Documents Button on the initial reply from Edgar (LAB-1-A)
    reply_metadata_list.append(sec_company_cik + ', ' 
                               + edgar_companyName_text + ', '  
                               + edgar_secNum_only + ', ' 
                               + edgar_secNum_clean + ', ' 
                               + job_log_suffix + ', '
                               + edgar_formName_only + ', ' 
                               + sec_edgar_doc_infos[0]  + ', ' 
                               + sec_edgar_doc_infos[1] + ', ' 
                               + sec_edgar_doc_infos[2]  + ', ' 
                               + sec_edgar_doc_infos[3]  + ', ' 
                               + storage_hierarchy_name + ','
                               + output_os_dir_src_sg2_job + ', '
                               + output_os_replyDocButtons_file + ', '
                               + hadoop_target_dir_purpose + ', '
                               + hadoop_mkdir_src_sg2 + ', '
                               + sec_edgar_doc_button_url)
    
#~~~ Store the full Hadoop 'mkdir' HDFS commands in a Python dictionary so we can write them all to a file at the end of the run.

    if hadoop_mkdir_src_sg2 not in hadoop_mkdir_command_list:    
        hadoop_mkdir_command_list.append(hadoop_mkdir_src_sg2)

#~~~ Now, parse the HTML table on each 'Documents Button' page for metadata about each of the many datasets per form (per 10-K, etc.)

#~~~ HEADS UP: This bit is a little tricky.  We have a table with 5 columns and an unknown number of rows.
#~~~           But, since we know we have 5 columns, we also know each time the counter reaches 6, it means a new table row & document
#~~~           So, when the counter reaches 5, we store the document metadata, build '.metadata' file names, add to Python
#~~~           dictionaries and write the actual file to the dircotory whose name was pre-built based on the HTML details 
#~~~           collected for each dataset before the WRITE occurs

    for edgar_request_table in soup_edgar_request_tables:
#~~~ Reset this counter for each new Documents Button page (aka Form page) - 1 Form page per Button URL & many datasets per Form
        edgar_form_page_metadata_count             = 0

        for td in edgar_request_table.findAll("td"):            
            edgar_form_page_metadata_count = edgar_form_page_metadata_count + 1

#~~~ When the counter reaches 6, it means the code is reading a new row for a new dataset. So, the counter is initialized again to = 1 for
            if edgar_form_page_metadata_count      >= 6:
                edgar_form_page_metadata_count     = 1
                
#~~~ Sequence Number (the first table column) doesn't
#~~~ I'll ignore it as it's not of much value because we want ALL files & Edgar DOES NOT assign a 'seq' to the .txt files.
                
                td_findNext_string                 = (td.findNext(text=True))
            else:
                td_findNext_string                 = (td.findNext(text=True))
    
#~~~ Document Description                
                if (edgar_form_page_metadata_count == 2):
                    metadata_document_description  = td_findNext_string    

                    wss_doc_description            = metadata_document_description
                
#~~~ Document Name                
                if (edgar_form_page_metadata_count == 3):
                    metadata_document_name = td_findNext_string
            
#~~~ Document Size
#~~~ AND - edgar_form_page_metadata_count == 5 means this is the last table column for this row. So, there is extra work to do here.

                if (edgar_form_page_metadata_count == 5):
                    metadata_document_size = td_findNext_string 
                    
                    wss_document_size           = metadata_document_size
                    
                    wss_hadoop_copy_command     = (hadoop_copy_dir_src_sg2_job + hadoop_target_dir_purpose)
                                        
                    if  wss_hadoop_copy_command not in hadoop_copy_command_list:
                        hadoop_copy_command_list.append(wss_hadoop_copy_command)
        
                    metadata_document_secNum = (sec_company_cik  + ', '  
                                                + edgar_secNum_only  + ', '  
                                                + edgar_secNum_clean + ', '
                                                + metadata_document_name + ', '
                                                + wss_doc_description + ', '    
                                                + wss_document_size + ', '
                                                + job_log_suffix + ', '
                                                + storage_hierarchy_name + ','
                                                + output_os_dir_src_sg2_job + ', '
                                                + hadoop_target_dir_purpose + ', '
                                                + wss_hadoop_copy_command + ', '
                                                + sec_edgar_doc_button_url)
                    
                    output_os_replyDocsMetadata_file  = (output_os_directory_cik_prefix + '/'
                                                         + job_log_prefix + '_'
                                                         + job_log_suffix + '_replyDocuments.metadata')
                    
                    output_os_replyDocsURL_file       = (output_os_directory_cik_prefix + '/'
                                                         + job_log_prefix + '_'
                                                         + job_log_suffix + '_replyDocsURL.metadata')
                    
                    if metadata_document_secNum not in document_metadata_list:
                        document_metadata_list.append(metadata_document_secNum)
                        
                    
                    output_os_hadoop_copy_cmds_file   = (output_os_directory_cik_prefix + '/'
                                                         + job_log_prefix + '_'
                                                         + job_log_suffix + '_copyFromLocal.hadoop')
    
                    sec_edgar_document_request_url    = (sec_edgar_request_url_prefix + '/'
                                                         + sec_edgar_document_request_prefix + '/'
                                                         + sec_company_cik + '/'
                                                         + edgar_secNum_clean + '/'
                                                         + metadata_document_name)
            
                    output_os_replyDocument_file      = (output_os_dir_src_sg2_job + '/'
                                                         + metadata_document_name)
                
                    if sec_edgar_document_request_url not in sec_edgar_document_urls:
                        sec_edgar_document_urls.append(sec_edgar_document_request_url)
                    
                        requestDocURL  = requests.get(sec_edgar_document_request_url, allow_redirects=True)
                        
                        with open(output_os_replyDocument_file, 'wb')as docfile_request:
                            docfile_request.write(requestDocURL.content)

                            docfile_request.close()

#~~~ This last set of paragraphs WRITEs the five (5) Python Dictionaries out to flat-files with .meatadata & .hadoop file extensions
#~~~ It's alway best to limit the number of open flat-files at any given time - I try and have only one file open at a time.
#~~~ And, by reusing the variable 'file_request', I'm sure to remember to CLOSE each file - If not, the next file's OPEN will ABEND

with open(output_os_replyDocButtons_file, 'w') as file_request:
    for reply_metadata_item in reply_metadata_list:
        file_request.write(reply_metadata_item)
        file_request.write(' \n')
        
file_request.close()
        
with open(output_os_replyDocsMetadata_file, 'w') as file_request:
    for document_metadata_item in document_metadata_list:
        file_request.write(document_metadata_item)
        file_request.write(' \n')
    
file_request.close()

with open(output_os_replyDocsURL_file, 'w') as file_request:
    for sec_edgar_document_item in sec_edgar_document_urls:
        file_request.write(sec_edgar_document_item)
        file_request.write(' \n')
    
file_request.close()

with open(output_os_hadoop_mkdir_cmds_file, 'w') as file_request:
    for hadoop_mkdir_command_item in hadoop_mkdir_command_list:
        file_request.write(hadoop_mkdir_command_item)
        file_request.write(' \n')
    
file_request.close()

with open(output_os_hadoop_copy_cmds_file, 'w') as file_request:
    for hadoop_copy_command_item in hadoop_copy_command_list:
        file_request.write(hadoop_copy_command_item)
        file_request.write(' \n')
    
file_request.close()

#~~~ #~~~ Storage Hierarchy Console Messages - So the operator knows which target directories will be used to store any files created

print('_____________________________________________________________________ \n')
print('Storage Hierarchy (' + storage_hierarchy_name + ') with Nodes Set As:')
print(' ~ local_server_os   = ', local_server_os)
print(' ~ ~ local_server_ip   = ', local_server_ip)
print(' ~ ~ ~ local_root_drive   = ', local_root_drive)
print(' ~ ~ ~ ~ dir_purpose        = ', dir_purpose)
print(' ~ ~ ~ ~ ~ dir_source         = ', dir_source)
print(' ~ ~ ~ ~ ~ ~ dir_src_sg1        = ', dir_src_sg1)
print(' ~ ~ ~ ~ ~ ~ ~ dir_src_sg2        = ', dir_src_sg2)
print(' ~ ~ ~ ~ ~ ~ ~ ~ JOB ID             = ', job_log_suffix)
print('_____________________________________________________________________ \n')

#~~~ DEBUG print('oooooooooooooooooooooooooooooooooooooo')
#~~~ DEBUG print('SEC Edgar Reply: Target URL List Member Metadata (one collection for each Documents button in the reply webpage): ')
#~~~ DEBUG print('oooooooooooooooooooooooooooooooooooooo \n')
#~~~ DEBUG for request_metadata_item in reply_metadata_list:
#~~~ DEBUG     pprint.pprint(request_metadata_item) 
#~~~ DEBUG     print(' \n')
#~~~ DEBUG print('_____________________________________________________________________ \n')

#~~~ DEBUG print(' \n')
#~~~ DEBUG print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
#~~~ DEBUG print('Edgar Dataset Metadata (one for each Dataset listed @ each Documents button URL in the reply webpage): ')
#~~~ DEBUG print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')       
#~~~ DEBUG for document_metadata_item in document_metadata_list: 
#~~~ DEBUG     pprint.pprint(document_metadata_item)   
#~~~ DEBUG     print(' \n')
#~~~ DEBUG print('_____________________________________________________________________ \n')
#~~~ DEBUG 
#~~~ DEBUG print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
#~~~ DEBUG print('Dataset URLs by secNum (one for each Dataset listed @ each Documents button URL in the reply webpage): ')
#~~~ DEBUG print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
#~~~ DEBUG pprint.pprint(sec_edgar_document_urls)
#~~~ DEBUG print('_____________________________________________________________________ \n')

#### 
####----- Python Routine Termination
#### 

end_time = datetime.datetime.now()
execution_time = end_time - start_time

print (' \n')
print ('<-<-<-<-<-<-<-<-<-<----  E X E C U T I O N   C O M P L E T E  ---->->->->->->->->->->')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>               R O U T I N E ................. DSB-3-LAB-1-B               <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('>>>>>         End Time: ', end_time, '                            <<<<<')
print ('>>>>>       Start Time: ', start_time, '                            <<<<<')
print ('>>>>>                    ~~~~~~~~~~~~~~~~~~~~~~~~~~', '                            <<<<<')
print ('>>>>>   Execution Time:             ', execution_time, '                            <<<<<')
print ('>>>>>                                                                           <<<<<')
print ('<-<-<-<-<-<-<-<-<-<----  E X E C U T I O N   C O M P L E T E  ---->->->->->->->->->->')
# 
#############################################################################################################################
#---------------------------------------------      Chameleon-DSB-3-LAB-1-B     ---------------------------------------------
#--------------------------   © 2018 Dynamic Database Support Systems and ChameleonMetadata.com    -------------------------- 
#----------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------   MIT Creative Commons License   ---------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated  
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# 1) The above copyright notice & this permission notice shall be included in all copies or substantial portions of the Software.
#
# 2) The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to 
#    the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors 
#    or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or 
#    otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.
#############################################################################################################################