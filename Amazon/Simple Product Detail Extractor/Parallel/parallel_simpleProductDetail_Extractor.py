from mpi4py import MPI
import urllib.request

from bs4 import BeautifulSoup
import pandas as pd
import sys
from time import sleep 


def main():

  MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?rh=n%3A565108&fs=true&ref=lp_565108_sar" # used in the master process
  maxNumberOfPagesToTraverse=int(sys.argv[1])
  comm = MPI.COMM_WORLD
  nprocs = comm.Get_size() # there are nprocs-1 slaves and 1 master
  rank = comm.Get_rank()


  if rank<nprocs-1: # if slave process
      # for all urls assigned to this slave, process all of them
      urlsToProcess_forThisProcess=comm.recv(source=nprocs-1)
      combinedDict_forThisProcess={'example_product_name':[], 'product_details':[]}
      for url_index, url in enumerate(urlsToProcess_forThisProcess):
        currResultDict=processUrl_or_returnNextUrl(url, maxNumberOfPagesToTraverse, mode="processUrl", proc_index=rank)
        for key, value in currResultDict.items(): # Add the current result to the overall list to be written to a csv file 
          combinedDict_forThisProcess[key].extend(value)
      comm.send(combinedDict_forThisProcess, dest=nprocs-1)

  else: # if master process
    allUrlsToProcess=get_all_search_urls_recursively(MAIN_URL_TO_PROCESS, maxNumberOfPagesToTraverse, proc_index=rank)
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
        df = pd.DataFrame({'Example Product Name':data['example_product_name'],'Product Details':data['product_details']}) 
        df.to_csv('amazon_parallel'+str(proc_index)+'.csv', index=False, encoding='utf-8')

    print("Finished!\nPlease check the contents of the .csv files created to see the results!")

# When finding all search urls, to avoid "get_all_search_urls_recursively" function calling itself recursively which would increase the call stack size; processUrl_or_returnNextUrl function is used. processUrl_or_returnNextUrl comes handy returning the url as soon as it is found (similar to tail recursivity logic) and helping not to grow the call stack.
def get_all_search_urls_recursively(url, maxNumberOfPagesToTraverse, proc_index):
  '''
    Descripton: Find all search urls by crawling thru next buttons given the initial "url".

    * "proc_index" parameter is only used for print calls to indate which process is in action 
  '''
  allUrlsToProcess=[]
  urlToProcess=url
  while urlToProcess is not None:
    # do the load balancing
    allUrlsToProcess+=[urlToProcess]
    urlToProcess=processUrl_or_returnNextUrl(urlToProcess, maxNumberOfPagesToTraverse, proc_index=proc_index, mode="returnNextUrl")
    sleep(0.05) # sleep around 50ms between each url request not to send too many request in a short time (so as not to get blocked)
  return allUrlsToProcess


def processUrl_or_returnNextUrl(url, maxNumberOfPagesToTraverse, proc_index, mode="processUrl"):
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
      example_product_name=[]
      product_details=[]
      for index, product_detail in enumerate(soup.find_all('div', attrs={'data-component-type':'s-search-result'})):
        example_product_name.append("Product " + str(index))
        product_details.append(product_detail.text)
      
      return {'example_product_name':example_product_name, 'product_details':product_details}

    elif mode=="returnNextUrl":
      # Search results are paged and there are numbers at the end of the amazon webpage directing us to those pages; we click on each of them programmatically and extract the information there.
      totalNumberOfPages=int(soup.find_all('li', attrs={'class':'a-disabled', 'aria-disabled':'true'})[-1].text)
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


def get_url_parser(url):
  '''
    returns the "soup" object to parse the given url's html 
    returns None the url request is not successful
  '''
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
         'Accept': '*/*',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         #'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.9',
         'Connection': 'keep-alive',
         'referer': url,
         'origin': 'https://www.amazon.com'}

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