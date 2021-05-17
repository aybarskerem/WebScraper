from mpi4py import MPI
import numpy
import urllib.request

from bs4 import BeautifulSoup
import pandas as pd

# We can use Selenium's webdriver if urllib.request is not favored.
#from selenium import webdriver
#driver = webdriver.Chrome() # enter tha chrome executable path as a parameter to Chrome function
#driver.get("https://www.hepsiburada.com/apple-watch-seri-3-gps-42-mm-uzay-grisi-aluminyum-kasa-ve-siyah-spor-kordon-mtf32tu-a-p-HBV00000F8RFL")

def main():
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()

  if rank == 0:
    url = "https://www.hepsiburada.com/apple-watch-seri-3-gps-42-mm-uzay-grisi-aluminyum-kasa-ve-siyah-spor-kordon-mtf32tu-a-p-HBV00000F8RFL"
    #data = {'some key': 5, 'another key': 10.5}
    comm.send(save(url), dest=3)


  elif rank == 1:
    url = "https://www.hepsiburada.com/iphone-11-128-gb-p-HBV0000122JCQ"
    comm.send(save(url), dest=3)
      

  elif rank == 2:
    url = "https://www.hepsiburada.com/asus-rog-strix-g513qm-hn081-amd-ryzen-7-5800h-16gb-1tb-ssd-rtx-3060-freedos-15-6-fhd-tasinabilir-bilgisayar-p-HBCV000004E3F3"
    comm.send(save(url), dest=3)

  elif rank == 3:
    sources=[0,1,2]
    data = comm.recv(source=sources[0])
    df = pd.DataFrame({'Ratings':data['ratings'],'Comments':data['comments']}) 
    df.to_csv('hepsiburada'+str(sources[0])+'.csv', index=False, encoding='utf-8')

    data = comm.recv(source=sources[1])
    df = pd.DataFrame({'Ratings':data['ratings'],'Comments':data['comments']}) 
    df.to_csv('hepsiburada'+str(sources[1])+'.csv', index=False, encoding='utf-8')

    data = comm.recv(source=sources[2])
    df = pd.DataFrame({'Ratings':data['ratings'],'Comments':data['comments']}) 
    df.to_csv('hepsiburada'+str(sources[2])+'.csv', index=False, encoding='utf-8')



def save(url):

  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
         'Accept': '*/*',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         #'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.9',
         'Connection': 'keep-alive',
         'referer': url,
         'origin': 'https://www.hepsiburada.com'}
  # Create a request to retrieve data using urllib.request
  request=urllib.request.Request(url,None,headers) #The assembled request
  resp = urllib.request.urlopen(request, timeout=10)

  # Check the status
  status_code = resp.status
  print(status_code) 

  comments=[]
  ratings=[]
  # if no error, then read the response contents
  if status_code >= 200 and status_code < 300:
      #print(resp.headers['Content-Type'])
      content=resp.read()
      
      soup = BeautifulSoup(content, features='lxml') # features='html.parser'
      #for a in soup.findAll('a', attrs={'class':'hermes-ReviewCard-module-34AJ_', 'itemprop':'review'}):
      for a in soup.findAll('span', attrs={'itemprop':'description'}):
        #print(a.text.encode('utf-8'))
        #comment=a.find('span', attrs={'itemprop':'description'})
        comments.append(a.text)
        ratings.append(5) # will be modified to add real rating later if needed

  return {'ratings':ratings, 'comments':comments}


if __name__ == "__main__":
  main()