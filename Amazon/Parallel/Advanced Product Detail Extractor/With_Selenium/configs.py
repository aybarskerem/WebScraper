'''
This file contains the main parameters that are used in the webscraper script.
The parameters are places block by block and categorized for readability.

NOTE: Please, only keep one block active at a time; otherwise only the last active block (the block not being comment that comes the latest in this file) is used.
'''

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

# There are 111 pages, so many; skipped for now
# MAIN_URL_TO_PROCESS = "https://www.amazon.com/s?i=tools-intl-ship&bbn=256643011&rh=n%3A256643011%2Cp_n_condition-type%3A6358196011%2Cp_89%3AGE&s=price-asc-rank&dc&fs=true&qid=1623584332&rnid=2528832011&ref=sr_nr_p_89_5"
# BRAND_NAME="GE"
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



