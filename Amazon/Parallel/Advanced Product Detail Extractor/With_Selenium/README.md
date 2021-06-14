------------------------------
# DESCRIPTION:

- A more advanced version of the parallel webscraper in "Simple Product Detail Extractor", implemented for the shopping site of Amazon (https://www.amazon.com/).

- The code extracts the product name, product price and user review information as can be seen in the .csv files.

- This webscraper uses Selenium library to send url requests to the server as well as giving an option to use urllib to make these url requests.

- This webscraper is expected to run on multiple different cpu threads and uses "MPI" for parallelization.  

- One example "url" is hard-coded in the configuration file (configs.py). Using this url, the code automatically checks other search results by tracking the urls embedded in the "next buttons" at the end of the search pages traversing all the results in the end (Actually, there are three example urls, brand names and categories of products hard-coded in the config file, but the others are commented out and the comments could be removed for usage.). Hence, please set the "MAIN_URL_TO_PROCESS", "BRAND_NAME" and "CATEGORY" parameters in the config file according to your preferences.

- This code clicks on every product image on the given hard-coded url to locate the comments and hence sends lots of url requests to Amazon website. To avoid getting blocked, high sleep amounts put in the code; so the code is expected to run slow to mimic a human on purpose.

- Note that this script assumes a certain tag to exist on the Amazon webpage's html (accessed by the url) and if Amazon changes taggings; the script should be updated accordingly in the html parsing part. Also, the urls that should be given to this script has the navigation buttons like "1 2 3 ...   400 Next" at the bottom of the page. 

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
Run it as below to see how to set the command line parameter(s):
```
mpiexec -n 2 python parallel_advancedProductDetail_Extractor.py
```
An example call is:  
```
mpiexec -n 2 python parallel_advancedProductDetail_Extractor.py -1
```
------------------------------

# OUTPUT:  

- An example output file ELECTRONICS (LAPTOPS).csv can be found which is produced as a result of running "parallel_advancedProductDetail_Extractor.py" script with the parameter blocks with the BRAND_NAME parameters of "Apple", "Lenovo", "Asus" and "Microsoft" in the config file (config.py).