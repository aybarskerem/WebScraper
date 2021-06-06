------------------------------
# DESCRIPTION:

- A more advanced version of the parallel webscraper in "Simple Product Detail Extractor", implemented for the shopping site of Amazon (https://www.amazon.com/).
- One example "url" is hard-coded in the code. Using this url, the code automatically checks other search results by tracking the urls embedded in the "next buttons" at the end of the search pages traversing all the results in the end (Actually, there are three examples urls and categories for each url are hard-coded, but the others are commented out and the comments could be removed for usage.)
- This webscraper is expected to run on 4 different cpu threads and uses "MPI" for parallelization.  
- The code extracts the product name, product price and user review information as can be seen in the .csv files. This code clicks on every product image to locate the comments and hence sends lots of url requests to Amazon website. To avoid getting blocked, high sleep amounts put in the code; so the code is expected to run slow to mimic a human on purpose.
- Note that this script assumes a certain tag to exist on the Amazon webpage's html (accessed by the url) and if Amazon changes taggings; the script should be updated accordingly in the html parsing part. Also, the urls that should be given to this script has the navigation buttons like "1 2 3 ...   400 Next" at the bottom of the page. 
- Please set the "MAIN_URL_TO_PROCESS" and "CATEGORY" variables in the source code according to your preferences.
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
```
------------------------------
# HOW TO RUN:
Run it as below to see how to set the command line parameter(s):
```
mpiexec -n 4 python parallel_advancedProductDetail_Extractor.py
```
An example call is:  
```
mpiexec -n 4 python parallel_advancedProductDetail_Extractor.py 7
```
------------------------------
# EXAMPLE COMMAND LINE OUTPUT FOR THE EXAMPLE RUN

No need to read this section, this is just to give an idea

```
> mpiexec -n 4 python parallel_advancedProductDetail_Extractor.py 7
```

The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?rh=n%3A565108&fs=true&ref=lp_565108_sar  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=2&qid=1622822191&ref=sr_pg_1  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=3&qid=1622822205&ref=sr_pg_2  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=4&qid=1622822216&ref=sr_pg_3  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=5&qid=1622822227&ref=sr_pg_4  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=6&qid=1622822239&ref=sr_pg_5  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=7&qid=1622822250&ref=sr_pg_6  
url is: https://www.amazon.com/s?rh=n%3A565108&fs=true&ref=lp_565108_sar  
Current page being processed by process 3 to find the next page url is:  1 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=2&qid=1622822191&ref=sr_pg_1  
url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=2&qid=1622822191&ref=sr_pg_1  
Current page being processed by process 3 to find the next page url is:  2 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=3&qid=1622822205&ref=sr_pg_2  
url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=3&qid=1622822205&ref=sr_pg_2  
Current page being processed by process 3 to find the next page url is:  3 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=4&qid=1622822216&ref=sr_pg_3  
url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=4&qid=1622822216&ref=sr_pg_3  
Current page being processed by process 3 to find the next page url is:  4 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=5&qid=1622822227&ref=sr_pg_4  
url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=5&qid=1622822227&ref=sr_pg_4  
Current page being processed by process 3 to find the next page url is:  5 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=6&qid=1622822239&ref=sr_pg_5  
url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=6&qid=1622822239&ref=sr_pg_5  
Current page being processed by process 3 to find the next page url is:  6 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=7&qid=1622822250&ref=sr_pg_6  
url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=7&qid=1622822250&ref=sr_pg_6  
Current page being processed by process 3 to find the next page url is:  7 out of 400 pages.  
Proccess 0 is responsible for the pages between 0 and 3  
Proccess 1 is responsible for the pages between 3 and 5  
Proccess 2 is responsible for the pages between 5 and 7  
Finished!  
Please check the contents of the .csv files created to see the results  


- The second run results (for the SPORTS category):

The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?bbn=16225014011&rh=n%3A%2116225014011%2Cn%3A10971181011&dc&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1489014608&rnid=16225014011&ref=s9_acss_bw_cts_AESPORVN_T2_w  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=2&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928109&rnid=16225014011&ref=sr_pg_1  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=3&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928136&rnid=16225014011&ref=sr_pg_2  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=4&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928167&rnid=16225014011&ref=sr_pg_3  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=5&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928189&rnid=16225014011&ref=sr_pg_4  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=6&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928221&rnid=16225014011&ref=sr_pg_5  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=7&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928250&rnid=16225014011&ref=sr_pg_6  
url is: https://www.amazon.com/s?bbn=16225014011&rh=n%3A%2116225014011%2Cn%3A10971181011&dc&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1489014608&rnid=16225014011&ref=s9_acss_bw_cts_AESPORVN_T2_w  
Current page being processed by process 3 to find the next page url is:  1 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=2&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928109&rnid=16225014011&ref=sr_pg_1  
url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=2&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928109&rnid=16225014011&ref=sr_pg_1  
Current page being processed by process 3 to find the next page url is:  2 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=3&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928136&rnid=16225014011&ref=sr_pg_2  
url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=3&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928136&rnid=16225014011&ref=sr_pg_2  
Current page being processed by process 3 to find the next page url is:  3 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=4&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928167&rnid=16225014011&ref=sr_pg_3  
url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=4&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928167&rnid=16225014011&ref=sr_pg_3  
Current page being processed by process 3 to find the next page url is:  4 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=5&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928189&rnid=16225014011&ref=sr_pg_4  
url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=5&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928189&rnid=16225014011&ref=sr_pg_4  
Current page being processed by process 3 to find the next page url is:  5 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=6&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928221&rnid=16225014011&ref=sr_pg_5  
url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=6&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928221&rnid=16225014011&ref=sr_pg_5  
Current page being processed by process 3 to find the next page url is:  6 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=7&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928250&rnid=16225014011&ref=sr_pg_6  
url is: https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011&dc&page=7&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1622928250&rnid=16225014011&ref=sr_pg_6  
Current page being processed by process 3 to find the next page url is:  7 out of 400 pages.  
Proccess 0 is responsible for the pages between 0 and 3  
Proccess 1 is responsible for the pages between 3 and 5  
Proccess 2 is responsible for the pages between 5 and 7  
Finished!  
Please check the contents of the .csv files created to see the results!  

- The third run results (for the TOOLS&HOME IMPROVEMENT category):  

The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?rh=n%3A256643011&fs=true&ref=lp_256643011_sar  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=2&qid=1622967365&ref=sr_pg_1  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=3&qid=1622967395&ref=sr_pg_2  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=4&qid=1622967426&ref=sr_pg_3  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=5&qid=1622967451&ref=sr_pg_4  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=6&qid=1622967476&ref=sr_pg_5  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=7&qid=1622967498&ref=sr_pg_6  
url is: https://www.amazon.com/s?rh=n%3A256643011&fs=true&ref=lp_256643011_sar  
Current page being processed by process 3 to find the next page url is:  1 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=2&qid=1622967365&ref=sr_pg_1  
url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=2&qid=1622967365&ref=sr_pg_1  
Current page being processed by process 3 to find the next page url is:  2 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=3&qid=1622967395&ref=sr_pg_2  
url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=3&qid=1622967395&ref=sr_pg_2  
Current page being processed by process 3 to find the next page url is:  3 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=4&qid=1622967426&ref=sr_pg_3  
url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=4&qid=1622967426&ref=sr_pg_3  
Current page being processed by process 3 to find the next page url is:  4 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=5&qid=1622967451&ref=sr_pg_4  
url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=5&qid=1622967451&ref=sr_pg_4  
Current page being processed by process 3 to find the next page url is:  5 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=6&qid=1622967476&ref=sr_pg_5  
url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=6&qid=1622967476&ref=sr_pg_5  
Current page being processed by process 3 to find the next page url is:  6 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=7&qid=1622967498&ref=sr_pg_6  
url is: https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=7&qid=1622967498&ref=sr_pg_6  
Current page being processed by process 3 to find the next page url is:  7 out of 400 pages.  
Proccess 0 is responsible for the pages between 0 and 3  
Proccess 1 is responsible for the pages between 3 and 5  
Proccess 2 is responsible for the pages between 5 and 7  
Finished!  
Please check the contents of the .csv files created to see the results!  