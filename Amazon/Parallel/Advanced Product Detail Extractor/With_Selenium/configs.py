'''
Configuration file for the webscraper script.

1) DESCRIPTIONS:
This file contains two types of parameters where the 1st type is parameters which are active all the time and the 2nd  type is parameters that should be active (non commmented-out) block-wise only. These starting point of these parameters are indicated as "1st TYPE PARAMETERS" and "2nd TYPE PARAMETERS (BLOCK-WISE ACTIVE PARAMETERS)" in comments in this file.

The 2nd type (block) parameters' are placed block by block and categorized for readability.

2) SOME PARAMETER DESCRIPTIONS:
- if MAX_NUMBER_OF_MAIN_PAGES_TO_TRAVERSE is -1; then it means traverse all the pages.

3) NOTES:

NOTE: Please refer to the comments 

NOTE: Please, only keep one block active at a time for the 2nd type; otherwise only the last active block (the block not being commented out that comes the latest in this file) is used.

NOTE:
For a correct comparision of parallel and serial execution time of the script; for MAX_NUMBER_OF_MAIN_PAGES_TO_TRAVERSE, please set a value which is multiple of #of slave processes (which is the total #of processes running - 1) so that each process deals with equal amount of pages. This way, each of the processes in parallel execution would be busy with some task. 

For timing comparisons, please also make sure that 'MAIN_URL_TO_PROCESS' contains more than or equal to MAX_NUMBER_OF_MAIN_PAGES_TO_TRAVERSE pages at the bottom; otherwise we would only process as many pages as the pages reachable from 'MAIN_URL_TO_PROCESS'.
'''

############################# 1st TYPE PARAMETERS #############################
MASTER_PROCESS_RANK = 0 # Only meaningful if webscraper is run with multiple processes. Here we use rank = 0 for master process; however we can set it to any value in [0, nprocs-1].
MAX_NUMBER_OF_MAIN_PAGES_TO_TRAVERSE = -1 # How many main pages that the webscraper should scrape. '-1' means traverse all the pages. Note that each main page contains multiple products where each product has a link directing us to its reviews & ratings page; here we only consider the main pages (the pages that are reached on the url indicated by 'MAIN_URL_TO_PROCESS' config parameter by clicking on 1, 2, 3, ..... at the bottom of the page). 
READ_ONLY_ONE_REVIEW_FOR_EACH_PAGE   = False # If True, it limits #of url requests (stops clicking on other products to get the reviews). If False, there occurs no limitation. This can be useful for comparison of parallel and serial running of the script to only test the speed of a subset of the urls.
NUMBER_OR_REPEATS_TIMEIT             = 1    # How many times 'timeit' module run the script (or process funtion) to time the script.
USE_SELENIUM                         = True # Whether to use selenium or urllib for webscraping. It should be set to True if Selenium False if urllib
SLEEP_BETWEEN_URL_REQUESTS           = True # This makes the corresponding process sleep between 8 and 17 seconds between each of its url request. This is important not to put a burden on the webserver and not to get blocked. The code might seem to run slow; but it is done on purpose. Still, if the code needs to be run quickly, 'SLEEP_BETWEEN_URL_REQUESTS' can be set to False. 

############################# 2nd TYPE PARAMETERS (BLOCK-WISE ACTIVE PARAMETERS) #############################
# ############################# ELECTRONICS CATEGORY #############################
# All product data retreived from the urls below (please check ELECTRONICS (LAPTOPS).csv file)

MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3AApple%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623747634&rnid=2224369011&ref=sr_nr_p_n_condition-type_2"
BRAND_NAME="Apple"
CATEGORY="ELECTRONICS (LAPTOPS)"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_89%3ALenovo%2Cp_n_condition-type%3A2224371011%2Cp_36%3A30000-&s=price-asc-rank&dc&fs=true&qid=1623582987&rnid=2421885011&ref=sr_nr_p_36_6"
# BRAND_NAME="Lenovo"
# CATEGORY="ELECTRONICS (LAPTOPS)"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_36%3A30000-%2Cp_n_condition-type%3A2224371011%2Cp_89%3AAcer&s=price-asc-rank&dc&fs=true&qid=1623583719&rnid=2528832011&ref=sr_nr_p_89_3"
# BRAND_NAME="Acer"
# CATEGORY="ELECTRONICS (LAPTOPS)"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_36%3A30000-%2Cp_n_condition-type%3A2224371011%2Cp_89%3AASUS&s=price-asc-rank&dc&fs=true&qid=1623583470&rnid=2528832011&ref=sr_nr_p_89_4"
# BRAND_NAME="ASUS"
# CATEGORY="ELECTRONICS (LAPTOPS)"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_36%3A30000-%2Cp_n_condition-type%3A2224371011%2Cp_89%3AHP&s=price-asc-rank&dc&fs=true&qid=1623583697&rnid=2528832011&ref=sr_nr_p_89_2"
# BRAND_NAME="HP"
# CATEGORY="ELECTRONICS (LAPTOPS)"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_36%3A30000-%2Cp_89%3AMicrosoft%2Cp_n_condition-type%3A2224371011&s=price-asc-rank&dc&fs=true&qid=1623583096&rnid=2224369011&ref=sr_nr_p_n_condition-type_1"
# BRAND_NAME="Microsoft"
# CATEGORY="ELECTRONICS (LAPTOPS)"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=computers&bbn=565108&rh=n%3A565108%2Cp_36%3A30000-%2Cp_n_condition-type%3A2224371011%2Cp_89%3ADell&s=price-asc-rank&dc&fs=true&qid=1623583668&rnid=2528832011&ref=sr_nr_p_89_7"
# BRAND_NAME="Dell"
# CATEGORY="ELECTRONICS (LAPTOPS)"


# ############################# TOOLS & HOME IMPROVEMENT CATEGORY #############################
# All data except for those which belong to "GE" brand not retrieved (please check TOOLS & HOME IMPROVEMENT.csv file)

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=tools-intl-ship&bbn=256643011&rh=n%3A256643011%2Cp_n_condition-type%3A6358196011%2Cp_89%3AEveryDrop+by+Whirlpool&s=price-asc-rank&dc&fs=true&qid=1623583866&rnid=2528832011&ref=sr_nr_p_89_1"
# BRAND_NAME="EveryDrop by Whirlpool"
# CATEGORY="TOOLS & HOME IMPROVEMENT"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=tools-intl-ship&bbn=256643011&rh=n%3A256643011%2Cp_n_condition-type%3A6358196011%2Cp_89%3ACommand&s=price-asc-rank&dc&fs=true&qid=1623583997&rnid=2528832011&ref=sr_nr_p_89_2"
# BRAND_NAME="Command"
# CATEGORY="TOOLS & HOME IMPROVEMENT"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=tools-intl-ship&bbn=256643011&rh=n%3A256643011%2Cp_n_condition-type%3A6358196011%2Cp_89%3ATenmiro&s=price-asc-rank&dc&fs=true&qid=1623584064&rnid=2528832011&ref=sr_nr_p_89_3"
# BRAND_NAME="Tenmiro"
# CATEGORY="TOOLS & HOME IMPROVEMENT"


# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=tools-intl-ship&bbn=256643011&rh=n%3A256643011%2Cp_n_condition-type%3A6358196011%2Cp_89%3AFlux+Phenom&s=price-asc-rank&dc&fs=true&qid=1623584266&rnid=2528832011&ref=sr_nr_p_89_4"
# BRAND_NAME="Flux Phenom"
# CATEGORY="TOOLS & HOME IMPROVEMENT"


# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=tools-intl-ship&bbn=256643011&rh=n%3A256643011%2Cp_n_condition-type%3A6358196011%2Cp_89%3ABrita&s=price-asc-rank&dc&fs=true&qid=1623584350&rnid=2528832011&ref=sr_nr_p_89_6"
# BRAND_NAME="Brita"
# CATEGORY="TOOLS & HOME IMPROVEMENT"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=tools-intl-ship&bbn=256643011&rh=n%3A256643011%2Cp_n_condition-type%3A6358196011%2Cp_89%3ABissell&s=price-asc-rank&dc&fs=true&qid=1623584381&rnid=2528832011&ref=sr_nr_p_89_7"
# BRAND_NAME="Bissell"
# CATEGORY="TOOLS & HOME IMPROVEMENT"


# ############################# SPORTS CATEGORY #############################
# All product data retreived from the urls below (please check SPORT.csv file)

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011%2Cp_n_condition-type%3A6503254011%2Cp_89%3AFitbit&s=price-asc-rank&dc&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1623593252&rnid=2528832011&ref=sr_nr_p_89_1"
# BRAND_NAME="Fitbit"
# CATEGORY="SPORTS"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011%2Cp_n_condition-type%3A6503254011%2Cp_89%3ABand-Aid&s=price-asc-rank&dc&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1623593264&rnid=2528832011&ref=sr_nr_p_89_2"
# BRAND_NAME="Band-Aid"
# CATEGORY="SPORTS"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011%2Cp_n_condition-type%3A6503254011%2Cp_89%3AFit+Simplify&s=price-asc-rank&dc&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1623593301&rnid=2528832011&ref=sr_nr_p_89_3"
# BRAND_NAME="Fit Simplify"
# CATEGORY="SPORTS"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011%2Cp_n_condition-type%3A6503254011%2Cp_89%3AOKELA&s=price-asc-rank&dc&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1623593321&rnid=2528832011&ref=sr_nr_p_89_4"
# BRAND_NAME="OKELA"
# CATEGORY="SPORTS"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011%2Cp_n_condition-type%3A6503254011%2Cp_89%3ATaylorMade&s=price-asc-rank&dc&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1623593351&rnid=2528832011&ref=sr_nr_p_89_5"
# BRAND_NAME="TaylorMade"
# CATEGORY="SPORTS"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011%2Cp_n_condition-type%3A6503254011%2Cp_89%3AComfyBrace&s=price-asc-rank&dc&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1623593370&rnid=2528832011&ref=sr_nr_p_89_6"
# BRAND_NAME="ComfyBrace"
# CATEGORY="SPORTS"

# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=sporting-intl-ship&bbn=16225014011&rh=n%3A16225014011%2Cn%3A10971181011%2Cp_n_condition-type%3A6503254011%2Cp_89%3AHoyle&s=price-asc-rank&dc&fst=as%3Aoff&pf_rd_i=16225014011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a3460e00-9eac-4cab-9814-093998a3f6d8&pf_rd_r=JXKT0E53MMQJ11T35FG8&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1623593387&rnid=2528832011&ref=sr_nr_p_89_7"
# BRAND_NAME="Hoyle"
# CATEGORY="SPORTS"



