from mpi4py import MPI
import urllib.request

from bs4 import BeautifulSoup
import pandas as pd
import sys
from time import sleep 
from datetime import datetime


def main():

  # MAIN PARAMETERS TO BE USED IN THE PROGRAM (Note that these constants are only used in the master process)
  MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?rh=n%3A565108&fs=true&ref=lp_565108_sar"
  maxNumberOfPagesToTraverse=int(sys.argv[1])

  # COMM VARIABLES
  comm = MPI.COMM_WORLD
  nprocs = comm.Get_size() # there are nprocs-1 slaves and 1 master
  rank = comm.Get_rank()

  if rank<nprocs-1: # if slave process
      # for all urls assigned to this slave, process all of them
      combinedDict_forThisProcess={}
      urlsToProcess_forThisProcess=comm.recv(source=nprocs-1)  
      for url_index, url in enumerate(urlsToProcess_forThisProcess):
        currResultDict=processUrl_or_returnNextUrl(url=url, proc_index=rank, mode="processUrl")
        for key, value in currResultDict.items(): # Add the current result to the overall list to be written to a csv file 
          combinedDict_forThisProcess.setdefault(key,[]).extend(value) # create keys according to what exists in currResultDict
      comm.send(combinedDict_forThisProcess, dest=nprocs-1)

  else: # if master process
    allUrlsToProcess=get_all_search_urls_recursively(url=MAIN_URL_TO_PROCESS, proc_index=rank, maxNumberOfPagesToTraverse)
    number_of_urls=len(allUrlsToProcess)
    # Load balance the urls across multiple CPUs

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

    # receive the processed urls containing the data as a dictionary where each value is a python list to be used as column data for the .csv files
    for proc_index in range(nprocs-1):
        data = comm.recv(source=proc_index)
        if data != {}: # if data is empty; then so no url has been processed by the process that sent this data
          df = pd.DataFrame({'Product Names':data['product_names'],'Product Prices':data['product_prices'],'User Reviews':data['user_reviews']}) 
          df.to_csv('amazon_parallel'+str(proc_index)+'.csv', index=False, encoding='utf-8')

    print("Finished!\nPlease check the contents of the .csv files created to see the results!")

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
    urlToProcess=processUrl_or_returnNextUrl(url=urlToProcess, proc_index=proc_index, mode="returnNextUrl", maxNumberOfPagesToTraverse)
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
      user_reviews=[]
      for index, product_item in enumerate(soup.find_all('div', attrs={'data-component-type':'s-search-result'})):
        product_name=product_item.find('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'}).text
        print("Name is: " + str(product_name))
        #print(product_item.find('span',attrs={'class':'a-price','data-a-color':'base'}))

        product_price_item=product_item.find('span',attrs={'class':'a-price'})
        if product_price_item is not None: # if price information available
          product_price=product_price_item.find('span',attrs={'class':'a-offscreen'}).text
        else:
          product_price="NA"
        print("product_price is: " + str(product_price))

        link_item=product_item.find('a', attrs={'class':'a-link-normal s-no-outline'})
        user_review_url="https://www.amazon.com"+link_item['href']
        user_review=get_user_review_from_url(user_review_url)
    
        product_names.append(product_name)
        product_prices.append(product_price)   
        user_reviews.append(user_review)
      
      return {'product_names':product_names, 'product_prices':product_prices, 'user_reviews':user_reviews}

    elif mode=="returnNextUrl":
      # Search results are paged and there are numbers at the end of the amazon webpage directing us to those pages; we click on each of them programmatically and extract the information there.
      
      print("url is: " + url)
      #print(soup)
      totalNumberOfPages=int(soup.find_all('li', attrs={'class':'a-disabled', 'aria-disabled':'true'})[-1].text)
      #totalNumberOfPages=int(soup.find('li',attrs={'class':'a-last'}).previous_sibling().text)
      numberOfPagesToTraverse=min(totalNumberOfPages, maxNumberOfPagesToTraverse)

      currPage=int(soup.find('li', attrs={'class':'a-selected'}).text)
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
    print("Request was unsuccessful, aborting the function...")
    return None

def get_user_review_from_url(url):
  review=""
  soup=get_url_parser(url)
  if soup is not None:  
    for product_review_item in soup.find_all('div', attrs={'data-hook':'review-collapsed', 'aria-expanded':'false', 'class':'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'}):
      review = product_review_item.find("span" , recursive=False).text # there should be only one child like this
      #print(review)
  else:
    print("The Request to the url to get comments was unsuccessful, aborting the function...")

  return review

def get_url_parser(url):
  '''
    returns the "soup" object to parse the given url's html 
    returns None the url request is not successful
  '''
  sleep(0.5) # sleep around 500ms between each url request not to send too many request in a short time (so as not to get blocked)

  user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
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

  # at each minute, use a different user agent from the list by rotating in a round-robin fashion
  user_agent_index=datetime.now().minute%no_of_user_agents
  headers = {
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93  Safari/537.36',
    #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
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


if __name__ == "__main__":
  if len(sys.argv)!=2:
    print("Please run the script as: \n \
      mpiexec -n <#of processes to run> python " + sys.argv[0] + " <Max #of Pages To Traverse> \n" + \
      "If you like to traverse all pages without a limit with 4 processes for example, run the script as: \n\
      mpiexec - n 4 python " + sys.argv[0] +  " -1")
  main()