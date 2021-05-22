import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

# We can use Selenium's webdriver if urllib.request is not favored.
#from selenium import webdriver
#driver = webdriver.Chrome() # enter tha chrome executable path as a parameter to Chrome function
#driver.get("https://www.hepsiburada.com/apple-watch-seri-3-gps-42-mm-uzay-grisi-aluminyum-kasa-ve-siyah-spor-kordon-mtf32tu-a-p-HBV00000F8RFL")

def main():
    urls=[
      "https://www.hepsiburada.com/apple-watch-seri-3-gps-42-mm-uzay-grisi-aluminyum-kasa-ve-siyah-spor-kordon-mtf32tu-a-p-HBV00000F8RFL",
       "https://www.hepsiburada.com/iphone-11-128-gb-p-HBV0000122JCQ",
       "https://www.hepsiburada.com/asus-rog-strix-g513qm-hn081-amd-ryzen-7-5800h-16gb-1tb-ssd-rtx-3060-freedos-15-6-fhd-tasinabilir-bilgisayar-p-HBCV000004E3F3",
       "https://www.hepsiburada.com/samsung-galaxy-a21s-64-gb-samsung-turkiye-garantili-p-HBV00000V3WE7",
       "https://www.hepsiburada.com/vestel-50u9500-50-127-ekran-uydu-alicili-4k-ultra-hd-smart-led-tv-p-HBV00000PJVIM"
    ]
    for index, url in enumerate(urls):
    #data = {'some key': 5, 'another key': 10.5}
      data=save(url)
      df = pd.DataFrame({'Ratings':data['ratings'],'Comments':data['comments']}) 
      df.to_csv('hepsiburada'+str(index)+'.csv', index=False, encoding='utf-8')

    print("Finished!\nPlease check the contents of the .csv files created to see the results!")


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
         
  request=urllib.request.Request(url,None,headers) # request the data from the "url"
  response = urllib.request.urlopen(request, timeout=10)

  comments=[]
  ratings=[]
  
  # if no error indicated by the status, then read the response content.
  status = response.status
  if status >= 200 and status < 300:
      content=response.read()
      soup = BeautifulSoup(content, features='lxml') # features='html.parser'
      #for comment in soup.find_all('a', attrs={'class':'hermes-ReviewCard-module-34AJ_', 'itemprop':'review'}):
      for comment in soup.find_all('span', attrs={'itemprop':'description'}):
        #print(comment.text.encode('utf-8'))
        #comment=soup.find('span', attrs={'itemprop':'description'})
        comments.append(comment.text)
        ratings.append(5) # will be modified to add real rating later if needed

  return {'ratings':ratings, 'comments':comments}


if __name__ == "__main__":
  main()