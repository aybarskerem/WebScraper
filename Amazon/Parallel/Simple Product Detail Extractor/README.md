------------------------------
# DESCRIPTION:

- A simple parallel webscraper for the shopping site of Amazon (https://www.amazon.com/).
- One example "url" is hard-coded in the code. Using this url, the code automatically checks other search results by tracking the urls embedded in the "next buttons" at the end of the search pages traversing all the results in the end.
- This webscraper is expected to run on 4 different cpu threads and uses "MPI" for parallelization.  
- The code extracts the general product information as can be seen in the .csv files.
- Note that this script assumes a certain tag to exist on the Amazon webpage's html (accessed by the url) and if Amazon changes taggings; the script should be updated accordingly in the html parsing part.
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
mpiexec -n 4 python parallel_simpleProductDetail_Extractor.py
```
An example call is:  
```
mpiexec -n 4 python parallel_simpleProductDetail_Extractor.py 10
```
------------------------------
# EXAMPLE COMMAND LINE OUTPUT FOR THE EXAMPLE RUN:

```
> mpiexec -n 4 python parallel_simpleProductDetail_Extractor.py 10
```

The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=8&qid=1621708131&ref=sr_pg_7  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=9&qid=1621708134&ref=sr_pg_8  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=10&qid=1621708137&ref=sr_pg_9  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=5&qid=1621708121&ref=sr_pg_4  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=6&qid=1621708123&ref=sr_pg_5  
The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=7&qid=1621708127&ref=sr_pg_6  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?rh=n%3A565108&fs=true&ref=lp_565108_sar
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=2&qid=1621708114&ref=sr_pg_1  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=3&qid=1621708116&ref=sr_pg_2  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=4&qid=1621708118&ref=sr_pg_3  
Current page being processed by process 3 to find the next page url is:  1 out of 400 pages.
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=2&qid=1621708114&ref=sr_pg_1  
Current page being processed by process 3 to find the next page url is:  2 out of 400 pages.
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=3&qid=1621708116&ref=sr_pg_2  
Current page being processed by process 3 to find the next page url is:  3 out of 400 pages.
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=4&qid=1621708118&ref=sr_pg_3  
Current page being processed by process 3 to find the next page url is:  4 out of 400 pages.
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=5&qid=1621708121&ref=sr_pg_4  
Current page being processed by process 3 to find the next page url is:  5 out of 400 pages.
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=6&qid=1621708123&ref=sr_pg_5  
Current page being processed by process 3 to find the next page url is:  6 out of 400 pages.
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=7&qid=1621708127&ref=sr_pg_6  
Current page being processed by process 3 to find the next page url is:  7 out of 400 pages.
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=8&qid=1621708131&ref=sr_pg_7  
Current page being processed by process 3 to find the next page url is:  8 out of 400 pages.
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=9&qid=1621708134&ref=sr_pg_8  
Current page being processed by process 3 to find the next page url is:  9 out of 400 pages.
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=10&qid=1621708137&ref=sr_pg_9  
Current page being processed by process 3 to find the next page url is:  10 out of 400 pages.
Proccess 0 is responsible for the pages between 0 and 4  
Proccess 1 is responsible for the pages between 4 and 7  
Proccess 2 is responsible for the pages between 7 and 10  
Finished!  
Please check the contents of the .csv files created to see the results!  

