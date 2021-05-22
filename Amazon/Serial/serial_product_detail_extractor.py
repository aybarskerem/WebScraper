import urllib.request

from bs4 import BeautifulSoup
import pandas as pd
import sys
from time import sleep 


def main():

  maxNumberOfPagesToTraverse=int(sys.argv[1])

  url = "https://www.amazon.com/s?rh=n%3A565108&fs=true&ref=lp_565108_sar"
  data=process_url_recursively(url, maxNumberOfPagesToTraverse)
  df = pd.DataFrame({'Example Product Name':data['example_product_name'],'Product Details':data['product_details']}) 
  df.to_csv('amazon_serial.csv', index=False, encoding='utf-8')

  print("Finished!\nPlease check the contents of the .csv files created to see the results!")

# we use a helper function for this "process_url_recursively" function (named return_next_url_and_process) since we have to traverse thru urls where the the next of the next url to be processed is found in the next url. To avoid calling process_url_recursively function recursively itself before returning and hence augmenting the call stack; return_next_url_and_process function comes handy returning the url as soon as it is found and helping not to grow the call stack.
def process_url_recursively(url, maxNumberOfPagesToTraverse):
  urlToProcess=url
  while urlToProcess is not None:
    urlToProcess=return_next_url_and_process(urlToProcess, maxNumberOfPagesToTraverse)
    sleep(0.05) # sleep around 50ms between each url request not to send too many request in a short time (so as not to get blocked)
  return {'example_product_name':return_next_url_and_process.example_product_name, 'product_details':return_next_url_and_process.product_details}

def return_next_url_and_process(url, maxNumberOfPagesToTraverse):     
  soup=get_url_parser(url)
  if soup:
    for index, product_detail in enumerate(soup.find_all('div', attrs={'data-component-type':'s-search-result'})):
      return_next_url_and_process.example_product_name.append("Product" + str(index))
      return_next_url_and_process.product_details.append(product_detail.text)
      
    # Search results are paged and there are numbers at the end of the amazon webpage directing us to those pages; we click on each of them programmatically and extract the information there.
    totalNumberOfPages=int(soup.find_all('li', attrs={'class':'a-disabled', 'aria-disabled':'true'})[-1].text)
    numberOfPagesToTraverse=min(totalNumberOfPages, maxNumberOfPagesToTraverse)

    currPage=int(soup.find('li', attrs={'class':'a-selected'}).text)
    print("Current page being processed is: ", str(currPage) + " out of " + str(totalNumberOfPages) + " pages.")
    if currPage!=numberOfPagesToTraverse:
      # find the li element with the class "a-last", then find its a tagged element's href value which is the link to the next search result
      nextButtonUrl=soup.find('li',attrs={'class':'a-last'}).a['href'] # by clicking next find all results
      fullUrlToSearch= "https://www.amazon.com"+nextButtonUrl
      print("Continue searching with the page: " +fullUrlToSearch)
      return fullUrlToSearch
    else:
      print("In total, " + str(numberOfPagesToTraverse) + " pages are processed out of "+ str(totalNumberOfPages) + " pages.")
      return None
  else:
    print("Request was unsuccessful, aborting the function...")
    return None
# process_url_recursively function attributes (used like a c++ style static function variables to be used accross function calls)
return_next_url_and_process.product_details=[]
return_next_url_and_process.example_product_name=[]


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
      python " + sys.argv[0] + " <Max #of Pages To Traverse> \n" + \
      "If you like to traverse all pages without a limit, run the script as: \n\
      python " + sys.argv[0] +  " -1")
  main()