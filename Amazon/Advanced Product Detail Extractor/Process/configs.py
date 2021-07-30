MASTER_PROCESS_RANK = 0 # Only meaningful if webscraper is run with multiple processes. Here we use rank = 0 for master process; however we can set it to any value in [0, nprocs-1].
READING_RATIO_FOR_INPUT_CSVs = 0.01 # It represents how much of the input files (in csv format for now) we should process. MUST BE BETWEEN [0, 1]. For example 0.1 means; process 1/10th of each of the input files (in terms of rows) and 1 means read them all.
NUMBER_OR_REPEATS_TIMEIT = 1
CREATE_WORD_CLOUD   = True
CREATE_BAG_OF_WORDS = True
CREATE_SENTIMENT_ANALYSIS_RESULTS = True

