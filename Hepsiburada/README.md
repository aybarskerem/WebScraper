------------------------------
# DESCRIPTION:

A simple parallel webscraper for the Turkish shopping site HepsiBurada (https://www.hepsiburada.com/)  is added.
Three example "url"s are hard-coded in the code. Please change the variables named "url" to your own choices.
This webscraper is expected to run on 4 different cpu threads and uses "MPI" for parallelization.

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
pip install selenium
pip install pandas
```
------------------------------
# HOW TO RUN:
Run it as below:
```
mpiexec -n 4 python parallel_webscraper.py
```
