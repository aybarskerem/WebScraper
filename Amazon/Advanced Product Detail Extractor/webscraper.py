from mpi4py import MPI
import urllib.request

from bs4 import BeautifulSoup
import pandas as pd
from time import sleep 
from datetime import datetime
import random
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import timeit
import configs # use MAIN_URL_TO_PROCESS, BRAND_NAME and CATEGORY specified in the configs.py file (Remove the comments of the related block to use those)
import functools
print = functools.partial(print, flush=True) #flush print functions by default

START_TIME = datetime.now()
NUMBER_OF_PAGES_TO_PROCESS = 0
def main():
  # COMM VARIABLES
  global comm, nprocs, rank 
  comm   = MPI.COMM_WORLD
  nprocs = comm.Get_size() # for multiprocessing there are nprocs-1 slaves (their ranks are 0, 1, ... nprocs-2)  and 1 master (its rank is nprocs-1) whereas for single-processing nprocs is 1 and the process' rank is 0.
  rank   = comm.Get_rank()
    
  if nprocs > 1:
    if rank == configs.MASTER_PROCESS_RANK: # print it only once
      print("Parallel execution")
  else:
    print("Serial execution")
  tp = timeit.Timer("process()", "from __main__ import process")
  average_duration_seconds = tp.timeit(number=configs.NUMBER_OR_REPEATS_TIMEIT) / configs.NUMBER_OR_REPEATS_TIMEIT

  if (nprocs > 1 and rank == configs.MASTER_PROCESS_RANK) or (nprocs == 1 and rank == 0): # after all slaves called and finished with the 'process' function (so handed their work to master to be outputted and then master merged these works), we can output the timing )
    output_timing_results(average_duration_seconds, configs.NUMBER_OR_REPEATS_TIMEIT, START_TIME, nprocs)

def process():
  
  global NUMBER_OF_PAGES_TO_PROCESS
  if configs.USE_SELENIUM: # initialize Selenium drivers with custom settings
    global driver
    headers = {
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Encoding': 'none',
        #'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'origin': 'https://www.amazon.com',
        'dnt': '1', # do not track
        'upgrade-insecure-requests': '1', # prefer an encrypted and authenticated response from the server
        'sec-fetch-site': 'same-origin',
      }

    for key, value in headers.items():
      webdriver.DesiredCapabilities.CHROME['chrome.page.customHeaders.'+ key] = value

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"]) # disable pop-ups
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # to get rid of "Google being controlled by automated software info bar"
    #options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

  if nprocs > 1:
    if rank != configs.MASTER_PROCESS_RANK: # if slave process       
      urlsToProcess_forThisProcess = comm.recv(source=configs.MASTER_PROCESS_RANK) #process the urls assigned to this slave
      processUrls_and_output_csv(urlsToProcess_forThisProcess)
      if configs.USE_SELENIUM:
        driver.quit()
      comm.send(True, dest=configs.MASTER_PROCESS_RANK) # send a signal to master to indicate that this slave process is finished processing  
    else: # if master process
      
      allUrlsToProcess           = get_all_search_urls_recursively(url=configs.MAIN_URL_TO_PROCESS)
      NUMBER_OF_PAGES_TO_PROCESS = len(allUrlsToProcess)
      print("Total #of pages to process are {}".format(NUMBER_OF_PAGES_TO_PROCESS) )
      if configs.USE_SELENIUM:
        driver.quit()
      distributed_urls_forEachProcess, startAndEnds_for_distributed_urls_forEachProcess = loadBalance_urls_toProcesses(allUrlsToProcess, nprocs-1)
      
      distributed_urls_index = 0
      for proc_index in range(nprocs):
        if proc_index != configs.MASTER_PROCESS_RANK:
          print("Proccess {0} is responsible for the urls between {1} and {2}\n".format(proc_index, *startAndEnds_for_distributed_urls_forEachProcess[distributed_urls_index] ) )
          comm.send(distributed_urls_forEachProcess[distributed_urls_index], dest=proc_index)
          distributed_urls_index += 1

      for proc_index in range(nprocs):
        if proc_index != configs.MASTER_PROCESS_RANK:
          isFinished = comm.recv(source=proc_index)
          if isFinished:
            print("Process " + str(proc_index) + " finished its job successfully")
          else:
            print("Error: Process " + str(proc_index) + " returned an unexpected value!")  
      
  else: # if single-processed
    allUrlsToProcess = get_all_search_urls_recursively(url=configs.MAIN_URL_TO_PROCESS)
    NUMBER_OF_PAGES_TO_PROCESS = len(allUrlsToProcess)
    print("Total #of pages to process are {}".format(NUMBER_OF_PAGES_TO_PROCESS))

    processUrls_and_output_csv(allUrlsToProcess)
    if configs.USE_SELENIUM:
      driver.quit()

def processUrls_and_output_csv(urlsToProcess_and_Output):
  for url_index, url in enumerate(urlsToProcess_and_Output):
    currResultDict = processUrl_or_returnNextUrl(url=url, mode="processUrl")
    if currResultDict is not None:
      df = pd.DataFrame({'Processor ID':rank, 'Category':configs.CATEGORY, 'Brand Name':configs.BRAND_NAME, 'Product Names':currResultDict['product_names'],'Product Prices':currResultDict['product_prices'],'Product Ratings':currResultDict['product_ratings'],'User Reviews':currResultDict['user_reviews']}) 

      mode, header = ('w', True) if url_index == 0 else ('a', False)
      df.to_csv(configs.CATEGORY+'.csv', index=False, encoding='utf-8', mode=mode, header=header) # append to file

def loadBalance_urls_toProcesses(urls_to_distribute, numberOfSlaveProcesses):
  '''
  LOAD BALANCE THE URLS ACROSS MULTIPLE PROCESSES

  Parameters:
    - urls_to_distribute     (list of strings): Urls (pages) to be divided among multiple processes
    - numberOfSlaveProcesses (int):             #of worker processes that the urls should be distributed to equally (or almost equally) 
 
  Returns:
    - distributed_urls_forEachProcess:                  A list of urls (strings) for each process respectively (the object at index 0, 1, 2 represents the urls to process for process 0, 1, 2 ... etc.). At each index, this variable contains a certain portion (list of some urls) of the 'urls_to_distribute' input parameter.
    - startAndEnds_for_distributed_urls_forEachProcess: A list of (start, end) index pairs to know starting / ending urls for each process to process.

  NOTE: This function is only meaningful when nprocs > 1 is True (which is multi-processed code)
  '''
  distributed_urls_forEachProcess   = []
  startAndEnds_for_distributed_urls_forEachProcess = []
  number_of_urls_to_process = len(urls_to_distribute)
  # number_of_rows_each_process holds the #of rows distributed to each process (e.g. for a total of 299 rows and 3 slave processes: 100, 100 and 99 rows respectively for process 0, 1 and 2 respectively.)
  least_number_of_urls_for_each_process=number_of_urls_to_process // numberOfSlaveProcesses
  number_of_processes_with_one_extra_url=number_of_urls_to_process % numberOfSlaveProcesses
  number_of_rows_each_process=[least_number_of_urls_for_each_process+1 if i<number_of_processes_with_one_extra_url
                              else least_number_of_urls_for_each_process
                              for i in range(numberOfSlaveProcesses)]

  # send relevant portions of the urls to corresponding processes (e.g. for 299 pages and 3 slave processes:  0:100, 100:200, 200:299 for process 0, 1 and 2 respectively)
  start = 0
  end   = 0
  for slave_proc_index in range(numberOfSlaveProcesses):
    end   = number_of_rows_each_process[slave_proc_index] + end
    startAndEnds_for_distributed_urls_forEachProcess.append((start, end))
    distributed_urls_forEachProcess.append(urls_to_distribute[start:end])
    start = end
  
  return distributed_urls_forEachProcess, startAndEnds_for_distributed_urls_forEachProcess

# When finding all search urls, to avoid "get_all_search_urls_recursively" function calling itself recursively which would increase the call stack size; processUrl_or_returnNextUrl function is used. processUrl_or_returnNextUrl comes handy returning the url as soon as it is found and helping not to grow the call stack.
def get_all_search_urls_recursively(url):
  '''
    Descripton: Find all search urls by crawling thru next buttons at the bottom of the 'url' parameter given.
  '''
  allUrlsToProcess = []
  urlToProcess     = url
  while urlToProcess is not None:
    allUrlsToProcess.append(urlToProcess)
    urlToProcess = processUrl_or_returnNextUrl(url=urlToProcess, mode="returnNextUrl")
  return allUrlsToProcess


def processUrl_or_returnNextUrl(url, mode="processUrl"):
  '''
  Description: Proccess the given "url" or returns the url embedded in the next button.

  * There are two modes that "mode" parameter can take"processUrl" and "returnNextUrl"..
   - If the mode is "processUrl",    this function only returns the url embedded in the next button by parsing the "url" parameter.
   - If the mode is "returnNextUrl", this function returns a dictionary containing product details and an example product name

  * "proc_index" parameter is only used for print calls to indate which process is in actino 
  '''
  soup=get_url_parser(url)

  if soup is not None:        
    if mode=="processUrl":
      print("The current url being processed by process {0} to find the product details is: {1}\n".format(rank, url))
      product_names   = []
      product_prices  = []
      product_ratings = []
      user_reviews    = []
      for product_item in soup.find_all('div', attrs={'data-component-type':'s-search-result'}):
        product_name       = product_item.find('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'}).text
        product_price_item = product_item.find('span',attrs={'class':'a-price'})
        if product_price_item is not None: # if price information available
          product_price = product_price_item.find('span',attrs={'class':'a-offscreen'}).text
        else:
          product_price = "NA"
        #print("product_price is: " + str(product_price))

        # re.compile("(?<=>).*(?= out of 5 stars)") -> the text we like to match is preceded by ">" (lookbehind) and and succeeded by " out of 5 start" (lookahead)
        #product_rating_text=product_item.find('span', attrs={'aria-label':re.compile("out of 5 stars")}).text
        #product_rating=product_rating_text.replace('out of 5 stars','')
        #print("product_rating is : " + str(product_rating))

        link_item       = product_item.find('a', attrs={'class':'a-link-normal s-no-outline'})
        user_review_url = "https://www.amazon.com" + link_item['href']
        # for each rating and user review added, duplicate the product name and price count
        numberOfRatingsBefore     = len(product_ratings)
        numberOfUserReviewsBefore = len(user_reviews)
        get_ratings_and_user_reviews_from_url(user_review_url, product_ratings=product_ratings, user_reviews=user_reviews)
        numberOfRatingsAfter     = len(product_ratings)
        numberOfUserReviewsAfter = len(user_reviews)
        numberOfRatingsAdded     = numberOfRatingsAfter     - numberOfRatingsBefore
        numberOfUserReviewsAdded = numberOfUserReviewsAfter - numberOfUserReviewsBefore

        assert numberOfRatingsAdded == numberOfUserReviewsAdded, "#of ratings and #of user reviews added do not match"
        for _ in range(numberOfRatingsAdded):
          product_names.append(product_name)
          product_prices.append(product_price)    

        if configs.READ_ONLY_ONE_REVIEW_FOR_EACH_PAGE: # for timing, only getting one item's reviews are enough.
          break 
      
      return {'product_names':product_names, 'product_prices':product_prices, 'product_ratings':product_ratings, 'user_reviews':user_reviews}

    elif mode == "returnNextUrl":
      # Search results are paged and there are numbers at the end of the amazon webpage directing us to those pages; we click on each of them programmatically and extract the information there.
      
      print( "url is: {0}".format(url) )
      selectedPageItem = soup.find('li', attrs={'class':'a-selected'})
      if selectedPageItem is not None:
        #print(UnicodeDammit.detwingle(soup).decode("utf-8") )
        currPage = int(selectedPageItem.text)
        #totalNumberOfPages=max(int(soup.find_all('li', attrs={'class':'a-normal'})[-1].text), currPage)
        #totalNumberOfPages=max(int(soup.find_all('li', attrs={'class':'a-disabled', 'aria-disabled':'true'})[-1].text), currPage)
        #unicode_safe_print(soup.find('li',attrs={'class':'a-last'}).previous_sibling.previous_sibling)
        totalNumberOfPages = max(int(soup.find('li',attrs={'class':'a-last'}).previous_sibling.previous_sibling.text),currPage)
        print("The total number of pages that exist on the main page is: " + str(totalNumberOfPages))
        
        if configs.MAX_NUMBER_OF_MAIN_PAGES_TO_TRAVERSE != -1:
          numberOfPagesToTraverse = min(totalNumberOfPages, configs.MAX_NUMBER_OF_MAIN_PAGES_TO_TRAVERSE)
        else:
          numberOfPagesToTraverse = totalNumberOfPages

        print("Current page being processed by process {0} to find the next page url is: {1} out of {2} pages.".format(rank, currPage, totalNumberOfPages))

        if currPage != numberOfPagesToTraverse:
          # find the li element with the class "a-last", then find its a tagged element's href value which is the link to the next search result
          nextButtonUrl   = soup.find('li',attrs={'class':'a-last'}).a['href'] # by clicking next find all results
          fullUrlToSearch = "https://www.amazon.com"+nextButtonUrl
          print("Next search url is: " +fullUrlToSearch)
          return fullUrlToSearch
        else:
          return None # we are already at the last page
      else:
        print("Either this product only has one page or url request is unsuccessful, please check the url to verify: " + url)
        return None  
  else:
    print("Request was unsuccessful, aborting the function...")
    return None

def get_ratings_and_user_reviews_from_url(url,product_ratings,user_reviews):
  '''
  fills product_ratings and user_reviews arrays.
  '''
  soup = get_url_parser(url)
  if soup is not None:  
    product_review_elements = soup.find_all('div', attrs={'data-hook':'review', 'class':'a-section review aok-relative'})
    if product_review_elements:
      for product_review_element in product_review_elements:
        rating      = 0
        review      = ""
        rating_item = product_review_element.find("a" , attrs={'class':'a-link-normal', 'title':re.compile(" out of 5 stars")})
        if rating_item and hasattr(rating_item, 'title'):
          rating_item = rating_item.attrs['title']
          rating=rating_item.replace(' out of 5 stars','')        
        else:
          print("Could not retrieve a rating for the url " + url)
          continue # could not retrieve rating for this element

        review_item = product_review_element.find("div" , attrs={'data-hook':'review-collapsed', 'aria-expanded':'false', 'class':'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'})

        # if there is only an image; then there would be no review body and hence no span or no span.text (but there would be only review title and rating; but we need reviews)
        if review_item and \
        hasattr(review_item, 'span') and review_item.span and \
        hasattr(review_item.span, 'text'):
          review=review_item.span.text       
        else:
          print("Could not retrieve a review for the url " + url)
          continue  
        
        product_ratings.append(rating)
        user_reviews.append(review)    

  else:
    print("The Request to the url to get comments was unsuccessful, aborting the function...")


def get_url_parser(url):
  '''
    returns the "soup" object to parse the given url's html 
    returns None the url request is not successful
  '''
  if configs.SLEEP_BETWEEN_URL_REQUESTS:
    randomSleepAmount = random.randint(8,17)
    sleep(randomSleepAmount) # sleep around 10-30 seconds between each url request not to send too many request in a short time (so as not to get blocked). Randomness is important as well so that the server does not detect a pattern among the requests

  if configs.USE_SELENIUM:   
    webdriver.DesiredCapabilities.CHROME['chrome.page.customHeaders.referer'] = url
    driver.get(url)
    content = driver.page_source   # unicode_safe_print(content)
    soup    = BeautifulSoup(content, features='lxml') # features='html.parser'
    return soup
  else:
    user_agents = [
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
      # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
      # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',    
      # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
      # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0', 
      # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
      # 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.216 Mobile/15E148 Safari/604.1'
      # 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.216 Mobile/15E148 Safari/604.1'
      # 'Mozilla/5.0 (iPod; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.216 Mobile/15E148 Safari/604.1'
      # 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      # 'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      # 'Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      # 'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      # 'Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      # 'Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      # 'Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      # 'Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    ]
    # at each 10 minutes, use a different user agent from the list by rotating in a round-robin fashion
    no_of_user_agents = len(user_agents)
    now              = datetime.now()
    user_agent_index = ( (now.hour * 60 + now.minute) // 10) % no_of_user_agents
    print("The selected user agent is: {0}".format(user_agents[user_agent_index]) ) # randomly choose an user agent from the list for each 
    
    headers = {
      'User-Agent': user_agents[user_agent_index],
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      #'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Encoding': 'none',
      # 'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive',
      'referer': url,
      'origin': 'https://www.amazon.com',
      'dnt': '1',
      'upgrade-insecure-requests': '1',
      'sec-fetch-site': 'same-origin',
      # 'sec-fetch-mode': 'navigate',
      # 'sec-fetch-user': '?1',
      # 'sec-fetch-dest': 'document',
    }
  
    request  = urllib.request.Request(url, None, headers) # request the data from the "url"
    response = urllib.request.urlopen(request, timeout=10)
    
    # if no error indicated by the status, then read the response content.
    status = response.status
    #print("Status code is: ", str(status))
    if status >= 200 and status < 300:
        content = response.read()
        soup    = BeautifulSoup(content, features='lxml') # features='html.parser'
        return soup
    else:
      return None 

def output_timing_results(duration_seconds, numberOfRepeats, startTime, numberOfProcesses=None):
  '''
  Parameters:
    duration_seconds (int):                       The duration of each run of the process function in process_csv.py
    numberOfRepeats  (int):                       The #of times the process function is called for timeit
    startTime        (datetime.datetime object):  The time the process script started
    nprocs           (int):                       #of MPI processes active
 
  Returns:
    Nothing
  '''
  days    = duration_seconds // 86400
  hours   = (duration_seconds % 86400) // 3600
  minutes = ( (duration_seconds % 86400) % 3600 ) // 60
  seconds = ( (duration_seconds % 86400) % 3600 ) % 60

  days, hours, minutes = map(int, [days, hours, minutes])

  with open("ExecutionTimingResults.txt", mode='a') as outputFile:
    outputFile.write("*************\n")

    if nprocs > 1:
      outputFile.write("MULTI-PROCESSED (PARALLEL) EXECUTION\n")
    else:
      outputFile.write("SINGLE-PROCESSED (SERIAL) EXECUTION\n")
    
    if numberOfProcesses:
      outputFile.write("#of processes involved is: {}\n".format(numberOfProcesses))
    else:
      outputFile.write("#of processes involved is: NA\n") 

    outputFile.write("#of pages processed is: {}\n".format(NUMBER_OF_PAGES_TO_PROCESS))
    outputFile.write("Does the code sleep between each url request?: {}\n".format("Yes" if configs.SLEEP_BETWEEN_URL_REQUESTS else "No"))
    outputFile.write("#of repeats is: {}\n".format(numberOfRepeats))
    outputFile.write("Script execution start date: {0}\n".format(startTime.strftime("%d/%m/%Y, %H:%M:%S")) )
    outputFile.write("Average script execution duration: {0} days {1} hours {2} minutes {3} seconds\n".format(days, hours, minutes, seconds) )

    print("Average script execution duration: {0} days {1} hours {2} minutes {3} seconds\n".format(days, hours, minutes, seconds))
    
def unicode_safe_print(string_to_print):
  try:
    print(string_to_print)
  except UnicodeEncodeError:
    # print char by char, replacing non-printable characters by ?
    for ch in string_to_print:
      try:
        print(ch, end="")
      except UnicodeEncodeError:
        print('?', end="")
    print("")

if __name__ == "__main__": 
  main()