------------------------------
# DESCRIPTION:

A simple webscraper for the shopping site of Amazon (https://www.amazon.com/).
One example "url" is hard-coded in the code. Using this url, the code automatically checks other search results by tracking the urls embedded in the "next buttons" at the end of the search pages traversing all the results in the end. 
Note that this script assumes a certain tag to exist on the Amazon webpage's html (accessed by the url) and if Amazon changes taggings; the script should be updated accordingly in the html parsing part.
------------------------------
# DEPENDENCIES:

1) Python3
2) Library Installations (download pip3 first if not installed already):
```
pip install numpy
pip install pandas
```
------------------------------
# HOW TO RUN:
Run it as below to see how to set the command line parameter(s):
```
python serial_product_detail_extractor.py
```
An example call is:  
```
python serial_product_detail_extractor.py 10
```
------------------------------
# EXAMPLE COMMAND LINE OUTPUT FOR THE EXAMPLE RUN:

```
> python serial_product_detail_extractor.py 10
```

Current page being processed is:  1 out of 400 pages.  
Continue searching with the page: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=2&qid=1621710737&ref=sr_pg_1  
Current page being processed is:  2 out of 400 pages.  
Continue searching with the page: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=3&qid=1621710740&ref=sr_pg_2  
Current page being processed is:  3 out of 400 pages.  
Continue searching with the page: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=4&qid=1621710744&ref=sr_pg_3  
Current page being processed is:  4 out of 400 pages.  
Continue searching with the page: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=5&qid=1621710747&ref=sr_pg_4  
Current page being processed is:  5 out of 400 pages.  
Continue searching with the page: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=6&qid=1621710749&ref=sr_pg_5  
Current page being processed is:  6 out of 400 pages.  
Continue searching with the page: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=7&qid=1621710750&ref=sr_pg_6  
Current page being processed is:  7 out of 400 pages.  
Continue searching with the page: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=8&qid=1621710753&ref=sr_pg_7  
Current page being processed is:  8 out of 400 pages.  
Continue searching with the page: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=9&qid=1621710755&ref=sr_pg_8  
Current page being processed is:  9 out of 400 pages.  
Continue searching with the page:  https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=10&qid=1621710756&ref=sr_pg_9  
Current page being processed is:  10 out of 400 pages.  
In total, 10 pages are processed out of 400 pages.  
Finished!  
Please check the contents of the .csv files created to see the results!  
