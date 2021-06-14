------------------------------
# DESCRIPTION:

- A more advanced version of the parallel webscraper in "Simple Product Detail Extractor", implemented for the shopping site of Amazon (https://www.amazon.com/).
- There are two versions for parallel webscraping in this folder where one uses Selenium framework and the other uses urllib librar's request function to retrieve web pages. The webscraping results are written to a .csv file at the end. The one that uses Selenium also outputs one more field to the .csv which is "Brand Name" and separates the .csv files by their "CATEGORY" configuration parameter which can be found in their corresponding configs.py files. The one using urllib only outputs one .csv file combining all categories.
- The script using the Selenium framework worked better in my tests for mimicing a real user's activity so as not to get blocked.
- The scripts sleep some random amount between 8 and 17 seconds so that we do not cause a heavy load on the server.