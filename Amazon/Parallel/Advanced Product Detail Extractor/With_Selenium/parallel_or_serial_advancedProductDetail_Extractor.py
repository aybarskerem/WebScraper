from mpi4py import MPI
import urllib.request

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import sys
from time import sleep 
from datetime import datetime
import random
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import  DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import functools
from bs4 import UnicodeDammit
import traceback
import timeit
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# use MAIN_URL_TO_PROCESS, BRAND_NAME and CATEGORY specified in the configs.py file (Remove the comments of the related block to use those)
from configs import * 

startTime = datetime.now()
IS_MULTIPROCESSED = False
IS_TIME_IT = True
NUMBER_OR_REPEATS_TIMEIT = 1

print = functools.partial(print, flush=True) #flush print functions by default
def main():
  if IS_MULTIPROCESSED:
    print("Parallel execution time")
  else:
    print("Serial Execution time")
  tp = timeit.Timer("process()", "from __main__ import process")
  average_duration_seconds = tp.timeit(number=NUMBER_OR_REPEATS_TIMEIT) / NUMBER_OR_REPEATS_TIMEIT
  output_timing_results(average_duration_seconds, NUMBER_OR_REPEATS_TIMEIT)

def process():

  if IS_MULTIPROCESSED:
    # COMM VARIABLES
    global comm, nprocs, rank
    comm = MPI.COMM_WORLD
    nprocs = comm.Get_size() # there are nprocs-1 slaves and 1 master
    rank = comm.Get_rank()

  global driver_path
  maxNumberOfPagesToTraverse=int(sys.argv[1])
  driver_path=ChromeDriverManager().install()
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
  global driver
  driver = webdriver.Chrome(driver_path, options=options)

  try:
    if IS_MULTIPROCESSED:
      if rank<nprocs-1: # if slave process
          
        urlsToProcess_forThisProcess=comm.recv(source=nprocs-1) #process the urls assigned to this slave

        for url_index, url in enumerate(urlsToProcess_forThisProcess):
          currResultDict=processUrl_or_returnNextUrl(url=url, proc_index=rank, mode="processUrl")
          if currResultDict is not None:
            df = pd.DataFrame({'Processor ID':rank, 'Category':CATEGORY, 'Brand Name':BRAND_NAME, 'Product Names':currResultDict['product_names'],'Product Prices':currResultDict['product_prices'],'Product Ratings':currResultDict['product_ratings'],'User Reviews':currResultDict['user_reviews']}) 
            header=True if url_index==0 else False
            df.to_csv(CATEGORY+'.csv', index=False, encoding='utf-8', mode='a', header=header) # append to file
        comm.send(True, dest=nprocs-1) # send a signal to indicate this process is finished processing
        driver.close()
      else: # if master process
        
        allUrlsToProcess=get_all_search_urls_recursively(url=MAIN_URL_TO_PROCESS, proc_index=rank, maxNumberOfPagesToTraverse=maxNumberOfPagesToTraverse)
        number_of_urls=len(allUrlsToProcess)
        # LOAD BALANCE THE URLS ACROSS MULTIPLE PROCESSES

        # number_of_urls_each_process holds the #of urls distributed to each process (e.g. for 299 pages and 3 slave processes: 100, 100 and 99 pages respectively.)
        least_number_of_urls_each=number_of_urls//(nprocs-1)
        number_of_processes_with_one_extra_url=number_of_urls%(nprocs-1)
        number_of_urls_each_process=[least_number_of_urls_each+1 if i<number_of_processes_with_one_extra_url
                                    else least_number_of_urls_each
                                    for i in range(nprocs-1)]


        # send relevant portions of the url list to corresponding processes (e.g. for 299 pages and 3 slave processes:  0:100, 100:200, 200:299 for process 0, 1 and 2 respectively)
        start=0
        end=0
        for proc_index in range(nprocs-1):
          end=number_of_urls_each_process[proc_index]+end
          print("Proccess " + str(proc_index) + " is responsible for the pages between " + str(start) + " and " + str(end))
          comm.send(allUrlsToProcess[start:end], dest=proc_index)
          start=end
        driver.close()

        proc_index=0
        while proc_index<(nprocs-1):
          isFinished=comm.recv(source=proc_index)
          if isFinished==True:
            print("Process " + str(proc_index) + " finished its job successfully")
            proc_index+=1
          else:
            print("Error: Process " + str(proc_index) + " returned an unexpected value, waiting for it to finish again...")  
        
    else: # if not multiprocessed
      rank = 0
      allUrlsToProcess=get_all_search_urls_recursively(url=MAIN_URL_TO_PROCESS, proc_index=rank, maxNumberOfPagesToTraverse=maxNumberOfPagesToTraverse)
      for url_index, url in enumerate(allUrlsToProcess):
        currResultDict=processUrl_or_returnNextUrl(url=url, proc_index=rank, mode="processUrl")
        if currResultDict is not None:
          df = pd.DataFrame({'Processor ID':rank, 'Category':CATEGORY, 'Brand Name':BRAND_NAME, 'Product Names':currResultDict['product_names'],'Product Prices':currResultDict['product_prices'],'Product Ratings':currResultDict['product_ratings'],'User Reviews':currResultDict['user_reviews']}) 
          header=True if url_index==0 else False
          df.to_csv(CATEGORY+'.csv', index=False, encoding='utf-8', mode='a', header=header) # append to file
      driver.close()
    
    if (not IS_MULTIPROCESSED) or (IS_MULTIPROCESSED and rank == nprocs-1): # if multiprocessed, only master should calculate timings.
      print("Finished!\nPlease check the contents of the .csv files created to see the results!")
      finishTime = datetime.now()
      duration_seconds = (finishTime-startTime).total_seconds()

      days    = duration_seconds // 86400
      hours   = (duration_seconds % 86400) // 3600
      minutes = ( (duration_seconds % 86400) % 3600 ) // 60
      seconds = ( (duration_seconds % 86400) % 3600 ) % 60

      days, hours, minutes = map(int, [days, hours, minutes])

      with open("timingResults.txt", mode='a') as outputFile:
        outputFile.write("*************\n")
        outputFile.write("Script execution start date: {0}\n".format(startTime.strftime("%d/%m/%Y, %H:%M:%S")) )
        outputFile.write("Script execution duration: {0} days {1} hours {2} minutes {3} seconds\n".format(days, hours, minutes, seconds) )

  except Exception:
    print("An error occured:\n" + traceback.format_exc())
  
# When finding all search urls, to avoid "get_all_search_urls_recursively" function calling itself recursively which would increase the call stack size; processUrl_or_returnNextUrl function is used. processUrl_or_returnNextUrl comes handy returning the url as soon as it is found (similar to tail recursivity logic) and helping not to grow the call stack.
def get_all_search_urls_recursively(url, proc_index, maxNumberOfPagesToTraverse):
  '''
    Descripton: Find all search urls by crawling thru next buttons given the initial "url".

    * "proc_index" parameter is only used for print calls to indate which process is in action 
  '''
  allUrlsToProcess=[]
  urlToProcess=url
  while urlToProcess is not None:
    # do the load balancing
    allUrlsToProcess+=[urlToProcess]
    urlToProcess=processUrl_or_returnNextUrl(url=urlToProcess, proc_index=proc_index, mode="returnNextUrl", maxNumberOfPagesToTraverse=maxNumberOfPagesToTraverse)
  return allUrlsToProcess


def processUrl_or_returnNextUrl(url, proc_index, mode="processUrl", maxNumberOfPagesToTraverse=0):
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
      print("The current url being processed by process " + str(proc_index) + " to find the product details is: " + str(url))
      product_names=[]
      product_prices=[]
      product_ratings=[]
      user_reviews=[]
      for product_item in soup.find_all('div', attrs={'data-component-type':'s-search-result'}):
        product_name=product_item.find('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'}).text
        #print("Name is: " + str(product_name))
        #print(product_item.find('span',attrs={'class':'a-price','data-a-color':'base'}))

        product_price_item=product_item.find('span',attrs={'class':'a-price'})
        if product_price_item is not None: # if price information available
          product_price=product_price_item.find('span',attrs={'class':'a-offscreen'}).text
        else:
          product_price="NA"
        #print("product_price is: " + str(product_price))

        # re.compile("(?<=>).*(?= out of 5 stars)") -> the text we like to match is preceded by ">" (lookbehind) and and succeeded by " out of 5 start" (lookahead)
        #product_rating_text=product_item.find('span', attrs={'aria-label':re.compile("out of 5 stars")}).text
        #product_rating=product_rating_text.replace('out of 5 stars','')
        #print("product_rating is : " + str(product_rating))

        link_item=product_item.find('a', attrs={'class':'a-link-normal s-no-outline'})
        user_review_url="https://www.amazon.com"+link_item['href']
        # for each rating and user review added, duplicate the product name and price count
        numberOfRatingsBefore=len(product_ratings)
        numberOfUserReviewsBefore=len(user_reviews)
        get_ratings_and_user_reviews_from_url(user_review_url, product_ratings=product_ratings, user_reviews=user_reviews)
        numberOfRatingsAfter=len(product_ratings)
        numberOfUserReviewsAfter=len(user_reviews)
        numberOfRatingsAdded=numberOfRatingsAfter-numberOfRatingsBefore
        numberOfUserReviewsAdded=numberOfUserReviewsAfter-numberOfUserReviewsBefore

        assert numberOfRatingsAdded==numberOfUserReviewsAdded,"#of ratings and #of user reviews added do not match"
        for _ in range(numberOfRatingsAdded):
          product_names.append(product_name)
          product_prices.append(product_price)    

        if IS_TIME_IT: # for timing, only getting one item's reviews are enough.
          break 
      
      return {'product_names':product_names, 'product_prices':product_prices, 'product_ratings':product_ratings, 'user_reviews':user_reviews}

    elif mode=="returnNextUrl":
      # Search results are paged and there are numbers at the end of the amazon webpage directing us to those pages; we click on each of them programmatically and extract the information there.
      
      print("url is: " + url)
      selectedPageItem=soup.find('li', attrs={'class':'a-selected'})
      if selectedPageItem is not None:
        #print(UnicodeDammit.detwingle(soup).decode("utf-8") )
        currPage=int(selectedPageItem.text)
        #totalNumberOfPages=max(int(soup.find_all('li', attrs={'class':'a-normal'})[-1].text), currPage)
        #totalNumberOfPages=max(int(soup.find_all('li', attrs={'class':'a-disabled', 'aria-disabled':'true'})[-1].text), currPage)
        #unicode_safe_print(soup.find('li',attrs={'class':'a-last'}).previous_sibling.previous_sibling)
        totalNumberOfPages=max(int(soup.find('li',attrs={'class':'a-last'}).previous_sibling.previous_sibling.text),currPage)
        print("total number of pages is: " + str(totalNumberOfPages))
        
        if maxNumberOfPagesToTraverse!=-1:
          numberOfPagesToTraverse=min(totalNumberOfPages, maxNumberOfPagesToTraverse)
        else:
          numberOfPagesToTraverse=totalNumberOfPages

        print("Current page being processed by process " + str(proc_index) + " to find the next page url is: ", str(currPage) + " out of " + str(totalNumberOfPages) + " pages.")
        if currPage!=numberOfPagesToTraverse:
          # find the li element with the class "a-last", then find its a tagged element's href value which is the link to the next search result
          nextButtonUrl=soup.find('li',attrs={'class':'a-last'}).a['href'] # by clicking next find all results
          fullUrlToSearch= "https://www.amazon.com"+nextButtonUrl
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
  soup=get_url_parser(url)
  if soup is not None:  
    product_review_elements=soup.find_all('div', attrs={'data-hook':'review', 'class':'a-section review aok-relative'})
    if product_review_elements:
      for product_review_element in product_review_elements:
        rating=0
        review=""
        rating_item = product_review_element.find("a" , attrs={'class':'a-link-normal', 'title':re.compile(" out of 5 stars")})
        if rating_item and hasattr(rating_item, 'title'):
          rating_item=rating_item.attrs['title']
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


def get_url_parser(url, useSelenium=True):
  '''
    returns the "soup" object to parse the given url's html 
    returns None the url request is not successful
  '''
  if not IS_TIME_IT: # if we are timing; we should not sleep
    randomSleepAmount=random.randint(8,17)
    sleep(randomSleepAmount) # sleep around 10-30 seconds between each url request not to send too many request in a short time (so as not to get blocked). Randomness is important as well so that the server does not detect a pattern among the requests

  if useSelenium:   
    webdriver.DesiredCapabilities.CHROME['chrome.page.customHeaders.referer'] = url
    driver.get(url)
    content=driver.page_source
    #print(content)
    soup = BeautifulSoup(content, features='lxml') # features='html.parser'
    return soup
  else:
    user_agents = [
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',    
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0', 
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
      'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.216 Mobile/15E148 Safari/604.1'
      'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.216 Mobile/15E148 Safari/604.1'
      'Mozilla/5.0 (iPod; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/90.0.4430.216 Mobile/15E148 Safari/604.1'
      'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      'Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      'Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      'Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      'Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      'Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36'
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    ]
    no_of_user_agents=len(user_agents)

    # at each 10 minutes, use a different user agent from the list by rotating in a round-robin fashion
    now=datetime.now()
    user_agent_index=((now.hour*60+now.minute)//10)%no_of_user_agents
    print("The selected user agent is: " + user_agents[user_agent_index])
    # randomly choose an user agent from the list for each 

    headers = {
      'User-Agent': user_agents[user_agent_index],
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      #'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive',
      'referer': url,
      'origin': 'https://www.amazon.com',
      'dnt': '1',
      'upgrade-insecure-requests': '1',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-user': '?1',
      'sec-fetch-dest': 'document',
    }
  
    request  = urllib.request.Request(url,None,headers) # request the data from the "url"
    response = urllib.request.urlopen(request, timeout=10)
    
    # if no error indicated by the status, then read the response content.
    status = response.status
    #print("Status code is: ", str(status))
    if status >= 200 and status < 300:
        content=response.read()
        soup = BeautifulSoup(content, features='lxml') # features='html.parser'
        return soup
    else:
      return None 

def output_timing_results(duration_seconds, numberOfRepeats):
  days    = duration_seconds // 86400
  hours   = (duration_seconds % 86400) // 3600
  minutes = ( (duration_seconds % 86400) % 3600 ) // 60
  seconds = ( (duration_seconds % 86400) % 3600 ) % 60

  days, hours, minutes = map(int, [days, hours, minutes])

  with open("ExecutionTimingResults.txt", mode='a') as outputFile:
    outputFile.write("*************\n")

    if IS_MULTIPROCESSED:
      outputFile.write("MULTI-PROCESSED (PARALLEL) EXECUTION\n")
    else:
      outputFile.write("SINGLE-PROCESSED (SERIAL) EXECUTION\n")

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
  if IS_MULTIPROCESSED:
    global comm, nprocs, rank
     # COMM VARIABLES
    comm = MPI.COMM_WORLD
    nprocs = comm.Get_size() # there are nprocs-1 slaves and 1 master
    rank = comm.Get_rank()

    if len(sys.argv)!=2:
      print("Please run the script as: \n \
        mpiexec -n <#of processes to run> python " + sys.argv[0] + " <Max #of Pages To Traverse> \n" + \
        "If you like to traverse all pages without a limit (with 4 processes for example), run the script as: \n\
        mpiexec - n 4 python " + sys.argv[0] +  " -1")
      exit(1)
    main()
  else:
    if len(sys.argv)!=2:
      print("Please run the script as: \n \
        python " + sys.argv[0] + " <Max #of Pages To Traverse> \n" + \
        "If you like to traverse all pages without a limit, run the script as: \n\
        python " + sys.argv[0] +  " -1")
      exit(1)
    main()