------------------------------
# DESCRIPTION:

- A simple parallel webscraper for the Turkish shopping site HepsiBurada (https://www.hepsiburada.com/).
- Five example "url"s are hard-coded in the code. Please change the variables named "urls" to fit your own choices.
- This webscraper is expected to run on multiple cpu threads and uses "MPI" for parallelization.  
- The results of running the script with 5 example urls can be found in .csv files.  
- One of the cpu threads are chosen as the master and creating the .csv files and the rest are slaves processing the urls. The urls to process are assigned to the cpus in a round-robin fashion meaning for 4 processes (3 slave) and 5 urls to process; the url indexed 0,1,2,3,4 are assigned to cpu 0,1,2,0,1 respectively.

------------------------------
# DEPENDENCIES:

1) Python3

2) Download and install ms-mpi for Windows.
https://stackoverflow.com/questions/54386910/microsoft-mpi-and-mpi4py-3-0-0-python-3-7-1-is-it-currently-possible-at-all

   - Download msmpisetup.exe and msmpisdk.msi from here:
https://www.microsoft.com/en-us/download/details.aspx?id=100593
https://docs.microsoft.com/en-us/archive/blogs/windowshpc/how-to-compile-and-run-a-simple-ms-mpi-program

   - Add both C:\Program Files (x86)\Microsoft SDKs\MPI and C:\Program Files\Microsoft MPI\Bin to system PATH.

3) Library Installations (download pip3 first if not installed already):
```
pip install numpy
pip install pandas
```
------------------------------
# HOW TO RUN:
Run it as below:
```
mpiexec -n <#of processes to run> python parallel_webscraper.py
```  
So, to run 4 processes, an example run would be:
```
mpiexec -n 4 python parallel_webscraper.py
```