------------------------------
# DESCRIPTION:
  
- A more advanced version of the parallel webscraper in "Simple Product Detail Extractor", implemented for the shopping site of Amazon (https://www.amazon.com/). This script can run in both 'parallel' or 'serial' mode.  
  
- The code extracts the product name, product price and user review information as can be seen in the .csv files.  
  
- This webscraper can either use Selenium library or urllib library to send url requests to the server as well as giving an option to use urllib to make these url requests. The selenium library performed better in my tests in terms of mimicking a real user behaviour and not getting blocked when used with enough sleeps (we put sleeps between each url request to not put a burden on the webserver).  
  
- This webscraper is expected to run on multiple different cpu threads and uses "MPI" for parallelization.  
  
- One example "url" is hard-coded in the configuration file (configs.py). Using this url, the code automatically checks other search results by tracking the urls embedded in the "next buttons" at the end of the search pages traversing all the results in the end (Actually, there are three example urls, brand names and categories of products hard-coded in the config file, but the others are commented out and the comments could be removed for usage.). Hence, please set the "MAIN_URL_TO_PROCESS", "BRAND_NAME" and "CATEGORY" parameters in the config file according to your preferences.
  
- This code clicks on every product image on the given hard-coded url to locate the comments and hence sends lots of url requests to Amazon website. To avoid getting blocked, high sleep amounts put in the code; so the code is expected to run slow to mimic a human on purpose.
  
- There is 'SLEEP_BETWEEN_URL_REQUESTS' parameter in configs.py file which is set to True. This makes the corresponding process sleep between 8 and 17 seconds between each of its url request. This is important not to put a burden on the webserver and not to get blocked. The code might seem to run slow; but it is done on purpose. Still, if the code needs to be run quickly, 'SLEEP_BETWEEN_URL_REQUESTS' can be set to False. 
  
- The webscraper script outputs three csv files ( ELECTRONICS (LAPTOPS), TOOLS & HOME IMPROVEMENT and SPORTS) which the process script (which resides in the Process folder) uses to process using some NLP techniques.  
------------------------------
# SOME NOTES:
  
- Note that this script assumes a certain tag to exist on the Amazon webpage's html (accessed by the url) and if Amazon changes taggings; the script should be updated accordingly in the html parsing part. Also, the urls that should be given to this script has the navigation buttons like "1 2 3 ...   400 Next" at the bottom of the page.  
  
- Please set the configuration parameters inside the config.py before running the code and read the descriptions there to understand the parameters better.  
  
------------------------------
# DEPENDENCIES:

1) Python3

2) Download and install ms-mpi for Windows.
https://stackoverflow.com/questions/54386910/microsoft-mpi-and-mpi4py-3-0-0-python-3-7-1-is-it-currently-possible-at-all

   - Download msmpisetup.exe and msmpisdk.msi from here:
https://www.microsoft.com/en-us/download/details.aspx?id=100593
https://docs.microsoft.com/en-us/archive/blogs/windowshpc/how-to-compile-and-run-a-simple-ms-mpi-program

   - Add both C:\Program Files (x86)\Microsoft SDKs\MPI and C:\Program Files\Microsoft MPI\Bin to system PATH.

3) Library Installations (download pip3 first if not installed already):
```
pip install numpy
pip install pandas
pip install selenium
pip install webdriver-manager
```
------------------------------
# HOW TO RUN:
Run it as below (for example, for 4 processes) for a multi-processed execution:
```
mpiexec -n 4 python webscraper.py
```
Run it as below to for a single-processed execution: 
```
python webscraper.py
```
------------------------------

# OUTPUT FILES:  
  
- ELECTRONICS (LAPTOPS).csv, SPORT.csv and TOOLS & HOME IMPROVEMENT.csv files which are produced as a result of running "webscraper.py" script.
  
------------------------------
  
# SCRIPT TERMINAL OUTPUT EXAMPLES
    
- Items 5 & 6 can be checked to see the effect of single-processing and multi-processing (30 sec vs 21 sec respectively for 3 pages where we read only one product's review on each of the pages).  
- Items 7 & 8 can be checked to see the overhead of using multi-processing unneccessarily (9 sec vs 12 sec for single and multi processing respectively).  
- Item 9 can be checked to see the script terminal output and correspoonding ExecutionTimingResults.txt entry for that run. Item 9 also traverses all products on each page since its 'MAX_NUMBER_OF_MAIN_PAGES_TO_TRAVERSE' parameter is -1.     
       
1) An example output for a single-processed (IS_MULTIPROCESSED is False) execution using urllib (USE_SELENIUM is False) for a single page where SLEEP_BETWEEN_URL_REQUESTS is True:   
Serial execution  
The selected user agent is: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
total number of pages is: 2  
Current page being processed by process 0 to find the next page url is: 1 out of 2 pages.  
Total #of pages to process are 1  
The selected user agent is: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36        
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2     
The selected user agent is: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36        
Average script execution duration: 0 days 0 hours 0 minutes 42.6207206 seconds  

2) An example output for a multi-processed (IS_MULTIPROCESSED is True) execution using urllib (USE_SELENIUM is False) for a single page where SLEEP_BETWEEN_URL_REQUESTS is True:  

Parallel execution  
The selected user agent is: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
total number of pages is: 2  
Current page being processed by process 3 to find the next page url is: 1 out of 2 pages.  
Total #of pages to process are 1  
Proccess 0 is responsible for the pages between 0 and 1  
Proccess 1 is responsible for the pages between 1 and 1  
Proccess 2 is responsible for the pages between 1 and 1  
The selected user agent is: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
The selected user agent is: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36        
Process 0 finished its job successfully  
Process 1 finished its job successfully  
Process 2 finished its job successfully  
Average script execution duration: 0 days 0 hours 0 minutes 40.550230500000005 seconds  
  
3) An example output for a multi-processed (IS_MULTIPROCESSED is True) execution using selenium (USE_SELENIUM is True) for requested 3 pages (url had 2 pages only) where SLEEP_BETWEEN_URL_REQUESTS is True:  

Parallel execution  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
total number of pages is: 2  
Current page being processed by process 3 to find the next page url is: 1 out of 2 pages.  
Next search url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&page=2&qid=1627565449&rnid=2224369011&ref=sr_pg_1  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&page=2&qid=1627565449&rnid=2224369011&ref=sr_pg_1  
total number of pages is: 2  
Current page being processed by process 3 to find the next page url is: 2 out of 2 pages.  
Total #of pages to process are 2  
Proccess 0 is responsible for the pages between 0 and 1  
Proccess 1 is responsible for the pages between 1 and 2  
Proccess 2 is responsible for the pages between 2 and 2  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&page=2&qid=1627565449&rnid=2224369011&ref=sr_pg_1-   
Process 0 finished its job successfully  
Average script execution duration: 0 days 0 hours 1 minutes 1.8260138999999995 seconds-   
Process 1 finished its job successfully  
Process 2 finished its job successfully  

4) An example output for a single-processed (IS_MULTIPROCESSED is False) execution using selenium (USE_SELENIUM is True) for requested 3 pages (url had 2 pages only) where SLEEP_BETWEEN_URL_REQUESTS is True:  

Serial execution  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
The total number of pages that exist on the main page is: 2  
Current page being processed by process 0 to find the next page url is: 1 out of 2 pages.  
Next search url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&page=2&qid=1627566396&rnid=2224369011&ref=sr_pg_1  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&page=2&qid=1627566396&rnid=2224369011&ref=sr_pg_1  
The total number of pages that exist on the main page is: 2  
Current page being processed by process 0 to find the next page url is: 2 out of 2 pages.  
Total #of pages to process are 2  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&page=2&qid=1627566396&rnid=2224369011&ref=sr_pg_1  
Average script execution duration: 0 days 0 hours 1 minutes 23.204676899999995 seconds  
  

5) An example output for a single-processed (IS_MULTIPROCESSED is False) execution using selenium (USE_SELENIUM is True) for 3 pages where SLEEP_BETWEEN_URL_REQUESTS is False:

Serial execution  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&qid=1623582987&rnid=2421885011&ref=sr_nr_p_36_6  
The total number of pages that exist on the main page is: 41  
Current page being processed by process 0 to find the next page url is: 1 out of 41 pages.  
Next search url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=2&qid=1627587603&rnid=2421885011&ref=sr_pg_1  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=2&qid=1627587603&rnid=2421885011&ref=sr_pg_1  
The total number of pages that exist on the main page is: 41  
Current page being processed by process 0 to find the next page url is: 2 out of 41 pages.  
Next search url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=3&qid=1627587605&rnid=2421885011&ref=sr_pg_2  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=3&qid=1627587605&rnid=2421885011&ref=sr_pg_2  
The total number of pages that exist on the main page is: 41  
Current page being processed by process 0 to find the next page url is: 3 out of 41 pages.  
Total #of pages to process are 3  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&qid=1623582987&rnid=2421885011&ref=sr_nr_p_36_6          
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=2&qid=1627587603&rnid=2421885011&ref=sr_pg_1        
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=3&qid=1627587605&rnid=2421885011&ref=sr_pg_2        
Average script execution duration: 0 days 0 hours 0 minutes 30.7439876 seconds   
  
6) An example output for a multi-processed (IS_MULTIPROCESSED is True) execution using selenium (USE_SELENIUM is True) for 3 pages where SLEEP_BETWEEN_URL_REQUESTS is False:  

Parallel execution  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&qid=1623582987&rnid=2421885011&ref=sr_nr_p_36_6  
The total number of pages that exist on the main page is: 41  
Current page being processed by process 0 to find the next page url is: 1 out of 41 pages.  
Next search url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=2&qid=1627598313&rnid=2421885011&ref=sr_pg_1  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=2&qid=1627598313&rnid=2421885011&ref=sr_pg_1  
The total number of pages that exist on the main page is: 41  
Current page being processed by process 0 to find the next page url is: 2 out of 41 pages.  
Next search url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=3&qid=1627598316&rnid=2421885011&ref=sr_pg_2  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=3&qid=1627598316&rnid=2421885011&ref=sr_pg_2  
The total number of pages that exist on the main page is: 41  
Current page being processed by process 0 to find the next page url is: 3 out of 41 pages.  
Total #of pages to process are 3  
Proccess 1 is responsible for the urls between 0 and 1  
Proccess 2 is responsible for the urls between 1 and 2  
Proccess 3 is responsible for the urls between 2 and 3  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=2&qid=1627598313&rnid=2421885011&ref=sr_pg_1        
The current url being processed by process 3 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&page=3&qid=1627598316&rnid=2421885011&ref=sr_pg_2        
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&qid=1623582987&rnid=2421885011&ref=sr_nr_p_36_6          
Process 1 finished its job successfully  
Process 2 finished its job successfully  
Process 3 finished its job successfully  
Average script execution duration: 0 days 0 hours 0 minutes 21.250288100000002 seconds  

7) An example output for a single-processed (IS_MULTIPROCESSED is False) execution using selenium (USE_SELENIUM is True) for 1 page where SLEEP_BETWEEN_URL_REQUESTS is False:  

url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
The total number of pages that are reachable from the main page is: 2  
Current page being processed by process 0 to find the next page url is: 1 out of 2 pages.  
Total #of pages to process are 1  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
Average script execution duration: 0 days 0 hours 0 minutes 9.5610805 seconds   

8) An example output for a multi-processed (IS_MULTIPROCESSED is True) execution using selenium (USE_SELENIUM is True) for 1 page where SLEEP_BETWEEN_URL_REQUESTS is False:  

The total number of pages that are reachable from the main page is: 2  
Current page being processed by process 0 to find the next page url is: 1 out of 2 pages.  
Total #of pages to process are 1  
Proccess 1 is responsible for the urls between 0 and 1  
Proccess 2 is responsible for the urls between 1 and 1  
Proccess 3 is responsible for the urls between 1 and 1  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
Process 1 finished its job successfully  
Process 2 finished its job successfully  
Process 3 finished its job successfully  
Average script execution duration: 0 days 0 hours 0 minutes 12.3952831 seconds  

9) An example output for a single-processed (IS_MULTIPROCESSED is False) execution using selenium (USE_SELENIUM is True) for 2 pages where SLEEP_BETWEEN_URL_REQUESTS is False and MAX_NUMBER_OF_MAIN_PAGES_TO_TRAVERSE is -1:  
a) Script terminal output:   
  
The total number of pages that are reachable from the main page is: 2  
Current page being processed by process 0 to find the next page url is: 1 out of 2 pages.  
Next search url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&page=2&qid=1627675793&rnid=2224369011&ref=sr_pg_1  
url is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&page=2&qid=1627675793&rnid=2224369011&ref=sr_pg_1  
The total number of pages that are reachable from the main page is: 2  
Current page being processed by process 0 to find the next page url is: 2 out of 2 pages.  
Total #of pages to process are 2  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2  
[6560:4224:0730/231136.941:ERROR:gpu_init.cc(441)] Passthrough is not supported, GL is disabled  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&page=2&qid=1627675793&rnid=2224369011&ref=sr_pg_1  
Average script execution duration: 0 days 0 hours 10 minutes 26.03176910000002 seconds  
  
b) Corresponding 'ExecutionTimingResults.txt' entry:    
  
************************************  
SINGLE-PROCESSED (SERIAL) EXECUTION  
  
- #of processes involved is:         1  
- #of main pages processed is:       2  
  
- READ_ONLY_ONE_REVIEW_FOR_EACH_PAGE config parameter value is: False  
- USE_SELENIUM                       config parameter value is: True  
- SLEEP_BETWEEN_URL_REQUESTS         config parameter value is: True  
  
- #of times the script was run is:   1  
- Script execution start date:       30/07/2021, 23:09:35  
- Average script execution duration: 0 days 0 hours 10 minutes 26.03176910000002 seconds  


