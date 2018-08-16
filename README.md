# education / DSB-3 / DSB-3-LAB-1-A
#
This script will read a known SEC Edgar System Central Index Key (CIK) and make a REQUEST to Edgar 
for SEC filings associated with that CIK and store the URL for each filing.  
#
If you don't know the company's CIK, you can look it up here: https://www.sec.gov/edgar/searchedgar/companysearch.html
#
The following two variables MUST be set before execution:
#
1: doc_buttons_write_dir_perfix = 'c:/DMZ_FTP-Receiving/sec-edgar' 

2: sec_company_cik              = '0001631574'      
#
The following two variables are optional and may be set before execution to filter results (in DSB-3-LAB-1-A filing_type has been set):
1: filing_type                  = '10-K'       #-- &type URL variable
2: until_data                   = '20181231'   #-- &dateb URL variable
3: filing_count                 = '15'         #-- &count URL variable
