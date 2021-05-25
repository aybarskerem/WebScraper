------------------------------
# DESCRIPTION:

- A more advanced version of the parallel webscraper in "Simple Product Detail Extractor", implemented for the shopping site of Amazon (https://www.amazon.com/).
- One example "url" is hard-coded in the code. Using this url, the code automatically checks other search results by tracking the urls embedded in the "next buttons" at the end of the search pages traversing all the results in the end.
- This webscraper is expected to run on 4 different cpu threads and uses "MPI" for parallelization.  
- The code extracts the product name, product price and user review information as can be seen in the .csv files. This code clicks on every product image to locate the comments and hence sends lots of url requests to Amazon website. To avoid getting blocked, high sleep amounts put in the code; so the code is expected to run slow to mimic a human on purpose.
- Note that this script assumes a certain tag to exist on the Amazon webpage's html (accessed by the url) and if Amazon changes taggings; the script should be updated accordingly in the html parsing part.
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
Run it as below to see how to set the command line parameter(s):
```
mpiexec -n 4 python parallel_advancedProductDetail_Extractor.py
```
An example call is:  
```
mpiexec -n 4 python parallel_advancedProductDetail_Extractor.py 4
```
------------------------------
# EXAMPLE COMMAND LINE OUTPUT FOR THE EXAMPLE RUN:

```
> mpiexec -n 4 python parallel_advancedProductDetail_Extractor.py 4
```

The current url being processed by process 1 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=3&qid=1621978830&ref=sr_pg_2  
Name is: Lenovo - IdeaPad 3 15" Laptop - Intel Core i3-1005G1-8GB Memory - 256GB SSD - Platinum Grey - 81WE011UUS  
product_price is: $465.00  
Name is: Dell Inspiron 3583 15ö Laptop Intel Celeron û 128GB SSD û 4GB DDR4 û 1.6GHz - Intel UHD Graphics 610 - Windows 10 Home - Inspiron 15 3000 Series - New  
product_price is: $365.00  
Name is: HP Pavilion x360 14 Convertible 2-in-1 Laptop, 14ö Full HD Touchscreen Display, Intel Core i5, 8 GB DDR4 RAM, 512 GB SSD Storage, Windows 10 Home, Backlit Keyboard (14-dh2011nr, 2020 Model)  
product_price is: NA  
Name is: Lenovo IdeaPad 3 14" Laptop, 14.0" FHD 1920 x 1080 Display, AMD Ryzen 5 3500U Processor, 8GB DDR4 RAM, 256GB SSD, AMD Radeon Vega 8 Graphics, Narrow Bezel, Windows 10, 81W0003QUS, Abyss Blue  
product_price is: $568.00  
Name is: Lenovo IdeaPad Flex 5 2-in-1 Laptop, 14" Full HD IPS Touch Screen, AMD Ryzen 7 4700U, Webcam, Backlit Keyboard, Fingerprint Reader, USB-C, HDMI, Windows 10 Home, 16GB RAM, 512GB PCIe SSD  
product_price is: $729.00  
Name is: Lenovo Chromebook S330 Laptop, 14-Inch FHD (1920 x 1080) Display, MediaTek MT8173C Processor, 4GB LPDDR3, 64GB eMMC, Chrome OS, 81JW0000US, Business Black  
product_price is: $279.99  
Name is: LG Gram 17Z90P - 17" WQXGA (2560x1600) Ultra-Lightweight Laptop, Intel evo with 11th gen CORE i7 1165G7 CPU , 16GB RAM, 1TB SSD, Alexa Built-in, 19.5 Hours Battery, Thunderbolt 4, Black - 2021  
product_price is: $1,696.99  
Name is: HP Pavilion Gaming 15-Inch Micro-EDGE Laptop, Intel Core i5-9300H Processor, NVIDIA GeForce GTX 1650 (4 GB), 8 GB SDRAM, 256 GB SSD, Windows 10 Home (15-dk0020nr, Shadow Black/Acid Green)  
product_price is: $726.90  
Name is: Dell Inspiron 15 3505 Full HD Laptop (FHD), 15.6 inch - AMD Ryzen 5 3450U, 12GB DDR4 RAM, 512GB SSD, AMD Radeon Vega 8 Graphics, Windows Laptop (10) - Black (Latest Model)  
product_price is: NA  
Name is: Dell Inspiron 15 5502, 15.6 inch FHD Thin & Light Laptop - Intel Core i5-1135G7, 8GB 3200MHz DDR4 RAM, 512GB SSD, Iris Xe Graphics, Windows 10 Home - Silver (Latest Model)  
product_price is: $693.88  
Name is: Dell Inspiron 15 3000 Laptop (2021 Latest Model), 15.6" HD Display, Intel N4020 Dual-Core Processor, 8GB RAM, 256GB SSD, Webcam, HDMI, Bluetooth, Wi-Fi, Black, Windows 10  
product_price is: $469.00  
Name is: HP Chromebook 11-inch Laptop - Up to 15 Hour Battery Life - MediaTek - MT8183 - 4 GB RAM - 32 GB eMMC Storage - 11.6-inch HD Display - with Chrome OS - (11a-na0021nr, 2020 Model, Snow White)  
product_price is: $227.99  
Name is: Samsung Galaxy Book Pro Laptop Computer, 15.6" AMOLED Screen, i7 11th Gen, 16GB Memory, 512GB SSD, Long-Lasting Battery, Mystic Blue  
product_price is: $1,299.99  
Name is: 2020 HP 14 inch HD Laptop, Intel Celeron N4020 up to 2.8 GHz, 4GB DDR4, 64GB eMMC Storage, WiFi 5, Webcam, HDMI, Windows 10 S /Legendary Accessories (Google Classroom or Zoom Compatible) (Rose Gold)  
product_price is: $399.99  
Name is: Dell 9310 XPS 2 in 1 Convertible, 13.4 Inch FHD+ Touchscreen Laptop, Intel Core i7-1165G7, 32GB 4267MHz LPDDR4x RAM, 512GB SSD, Intel Iris Xe Graphics, Windows 10 Home - Platinum Silver (Latest Model)  
product_price is: $1,680.00  
Name is: HP Stream 14-Inch Touchscreen Laptop, AMD Athlon 3050U2a, 4 GB SDRAM, 64 GB eMMC, Windows 10 Home in S Mode with Office 365 Personal for One Year (Silver), cm. Accessories  
product_price is: $326.99  
Name is: ASUS VivoBook 15 Thin and Light Laptop- 15.6ö Full HD, Intel i5-1035G1 CPU, 8GB RAM, 512GB SSD, Backlit KeyBoard, Fingerprint, Windows 10- F512JA-AS54, Slate Gray  
product_price is: $688.90  
Name is: ASUS ZenBook 14 Ultra-Slim Laptop 14ö FHD NanoEdge Bezel Display, Intel Core i7-1165G7, NVIDIA MX450, 16GB RAM, 512GB SSD, ScreenPad 2.0, Thunderbolt 4, Windows 10 Pro, Pine Grey, UX435EG-XH74  
product_price is: $1,198.99  
Name is: 2020 HP 17.3" HD+ Premium Laptop Computer, AMD Ryzen 5 3500U Quad-Core Up to 3.7GHz, 12GB DDR4 RAM, 256GB SSD, DVDRW, AMD Radeon Vega 8, 802.11ac WiFi, Bluetooth 4.2, USB 3.1, HDMI, Black, Windows 10  
product_price is: $699.99  
Name is: Apple MacBook Air MJVM2LL/A 11.6-Inch laptop(1.6 GHz Intel i5, 128 GB SSD, Integrated Intel HD Graphics 6000, Mac OS X Yosemite (Renewed)  
product_price is: $399.00  
Name is: Acer Predator Helios 300 Gaming Laptop, Intel i7-10750H, NVIDIA GeForce RTX 2060 6GB, 15.6" Full HD 144Hz 3ms IPS Display, 16GB Dual-Channel DDR4, 512GB NVMe SSD, Wi-Fi 6, RGB Keyboard, PH315-53-72XD  
product_price is: $1,530.00  
Name is: New Dell XPS 15 9500 15.6 inch UHD+ Touchscreen Laptop (Silver) Intel Core i7-10750H 10th Gen, 16GB DDR4 RAM, 1TB SSD, Nvidia GTX 1650 Ti with 4GB GDDR6, Window 10 Pro (XPS9500-7845SLV-PUS)  
product_price is: $1,980.00  
Name is: 2021 HP 14 inch HD Laptop Newest for Business and Student, AMD Athlon Silver 3050U (Beat i5-7200U), 16GB DDR4 RAM, 512GB SSD, 802.11ac, WiFi, Bluetooth, HDMI, Windows 10 w/HESVAP 3in1 Accessories  
product_price is: $589.00  
Name is: ASUS VivoBook 15 Thin & Light Laptop, 15.6ö FHD Display, AMD Quad Core R7-3700U CPU, 8GB DDR4 RAM, 512GB PCIe SSD, AMD Radeon Vega 10 Graphics, Fingerprint, Windows 10 Home, Slate Gray, F512DA-NH77  
product_price is: $679.00  
The current url being processed by process 2 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=4&qid=1621978834&ref=sr_pg_3  
Name is: HP 14" Touchscreen Home and Business Laptop Ryzen 3-3200U, 8GB RAM, 128GB M.2 SSD, Dual-Core up to 3.50 GHz, Vega 3 Graphics, RJ-45, USB-C, 4K Output HDMI, Bluetooth, Webcam, 1366x768, Win 10  
product_price is: $444.00  
Name is: Lenovo Ideapad L340 Gaming Laptop, 15.6 Inch FHD (1920 X 1080) IPS Display, Intel Core i5-9300H Processor, 8GB DDR4 RAM, 512GB Nvme SSD, NVIDIA GeForce GTX 1650, Windows 10, 81LK00HDUS, Black  
product_price is: $755.00  
Name is: HP Chromebook x360 14-inch HD Touchscreen Laptop, Intel Celeron N4000, 4 GB RAM, 32 GB eMMC, Chrome (14b-ca0010nr, Ceramic White/Mineral Silver)  
product_price is: $325.99  
Name is: Dell Latitude E7470 14in Laptop, Core i5-6300U 2.4GHz, 8GB Ram, 256GB SSD, Windows 10 Pro 64bit (Renewed)  
product_price is: $429.99  
Name is: Acer C720 11.6in Chromebook Intel Celeron 1.40GHz Dual Core Processor, 2GB RAM, 16GB W/Chrome OS (Renewed)  
product_price is: $127.00  
Name is: ASUS ZenBook Pro Duo UX581 Laptop, 15.6ö 4K UHD NanoEdge Touch Display, Intel Core i9-10980HK, 32GB RAM, 1TB PCIe SSD, GeForce RTX 2060, ScreenPad Plus, Windows 10 Pro, Celestial Blue, UX581LV-XS94T  
product_price is: $2,899.99  
Name is: Razer Blade 15 Advanced Gaming Laptop 2021: Intel Core i7-10875H 8-Core, NVIDIA GeForce RTX 3070, 15.6ö QHD 240Hz, 16GB RAM, 1TB SSD - CNC Aluminum - Chroma RGB - THX Spatial Audio - Thunderbolt 3  
product_price is: $2,499.99  
Name is: HP Chromebook 14 - 14" HD Non-Touch Intel Pentium Silver N5000, Intel UHD Graphics 605, 4GB RAM, 64GB eMMC, WiFi, Bluetooth, Audio by B&O, Chrome OS (Renewed)  
product_price is: $193.00  
Name is: 2020 HP Envy x360 2-in-1 13.3" FHD IPS Touchscreen Laptop Intel Evo Platform 11th Gen Core i7-1165G7 8GB Memory 512GB SSD Pale Gold - Backlit Keyboard -Fingerprint Reader -Thunderbolt - WiFi 6  
product_price is: $899.00  
Name is: Apple MacBook Pro 13in Core i5 Retina 2.7GHz (MF840LL/A), 8GB Memory, 256GB Solid State Drive (Renewed)  
product_price is: $599.00  
Name is: Microsoft Surface Laptop 4 13.5öáTouch-Screen û AMD Ryzená5 Surface Edition -á8GB Memory -á256GB Solid State Drive (Latest Model)á-áPlatinum  
product_price is: NA  
Name is: HP 14-inch Chromebook HD Touchscreen Laptop PC (Intel Celeron N3350 up to 2.4GHz, 4GB RAM, 32GB Flash Memory, WiFi, HD Camera, Bluetooth, Up to 10 hrs Battery Life, Chrome OS , Black)  
product_price is: NA  
Name is: Acer Nitro 5 Gaming Laptop, 10th Gen Intel Core i5-10300H,NVIDIA GeForce GTX 1650 Ti, 15.6" Full HD IPS 144Hz Display, 8GB DDR4,256GB NVMe SSD,WiFi 6, DTS X Ultra,Backlit Keyboard,AN515-55-59KS  
product_price is: $729.99  
Name is: 2021 Newest Acer Aspire 5 Slim Laptop, 15.6 inches Full HD IPS Display, AMD Ryzen 3 3200U, Vega 3 Graphics, 8GB DDR4, 256GB SSD, Backlit Keyboard, Windows 10 + Oydisen Cloth  
product_price is: $469.99  
Name is: Dell Inspiron 14 5406 2 in 1 Convertible Laptop, 14-inch FHD Touchscreen Laptop - Intel Core i7-1165G7, 12GB 3200MHz DDR4 RAM, 512GB SSD, Iris Xe Graphics, Windows 10 Home - Titan Grey (Latest Model)  
product_price is: $886.61  
Name is: Google Pixelbook Go - Lightweight Chromebook Laptop - Up to 12 Hours Battery Life[1] - Touch Screen Chromebook - Just Black  
product_price is: NA  
Name is: Microsoft Surface Laptop 3 û 13.5" Touch-Screen û Intel Core i5 - 8GB Memory - 256GB Solid State Drive û Matte Black  
product_price is: $873.76  
Name is: Dell ChromeBook 11 -Intel Celeron 2955U, 4GB Ram, 16GB SSD, WebCam, HDMI, (11.6 HD Screen 1366x768) (Renewed)  
product_price is: $117.35  
Name is: 2021 Newest Dell Inspiron 15 3000 Series 3593 Laptop, 15.6" HD Non-Touch, 10th Gen Intel Core i3-1005G1 Processor, 8GB RAM, 256GB PCIe NVMe SSD, Webcam, HDMI, Wi-Fi, Bluetooth, Windows 10 Home, Black  
product_price is: $449.00  
Name is: Microsoft Surface Laptop Go - 12.4" Touchscreen - Intel Core i5 - 8GB Memory - 128GB SSD - Sandstone  
product_price is: NA  
Name is: 2020 HP 15.6" HD LED Display Laptop, Intel Pentium Gold 6405U Processor, 4GB DDR4 RAM, 128GB SSD, HDMI, Webcam, WI-FI, Windows 10 S, Scarlet Red  
product_price is: NA  
Name is: Apple 13in MacBook Air, 1.8GHz Intel Core i5 Dual Core Processor, 8GB RAM, 128GB SSD, Mac OS, Silver, MQD32LL/A (Newest Version) (Renewed)  
product_price is: $529.00  
Name is: Fast Dell Latitude E5470 HD Business Laptop Notebook PC (Intel Core i5-6300U, 8GB Ram, 256GB Solid State SSD, HDMI, Camera, WiFi, SC Card Reader) Win 10 Pro (Renewed).  
product_price is: $385.00  
Name is: Dell Inspiron 17 3793 2020 Premium 17.3ö FHD Laptop Notebook Computer, 10th Gen 4-Core Intel Core i5-1035G1 1.0 GHz, 16GB RAM, 512GB SSD + 1TB HDD, DVD,Webcam,Bluetooth,Wi-Fi,HDMI, Win 10 Home  
product_price is: $840.00  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?rh=n%3A565108&fs=true&ref=lp_565108_sar  
Name is: 2020 Apple MacBook Air with Apple M1 Chip (13-inch, 8GB RAM, 256GB SSD Storage) - Space Gray  
product_price is: NA  
Name is: Acer Nitro 5 Gaming Laptop, 9th Gen Intel Core i5-9300H, NVIDIA GeForce GTX 1650, 15.6" Full HD IPS Display, 8GB DDR4, 256GB NVMe SSD, Wi-Fi 6, Backlit Keyboard, Alexa Built-in, AN515-54-5812  
product_price is: $749.99  
Name is: 2020 Apple MacBook Pro with Apple M1 Chip (13-inch, 8GB RAM, 256GB SSD Storage) - Space Gray  
product_price is: NA  
Name is: Acer Aspire 5 Slim Laptop, 15.6 inches Full HD IPS Display, AMD Ryzen 3 3200U, Vega 3 Graphics, 4GB DDR4, 128GB SSD, Backlit Keyboard, Windows 10 in S Mode, A515-43-R19L, Silver  
product_price is: $430.00  
Name is: Lenovo Flex 5 14" 2-in-1 Laptop, 14.0" FHD (1920 x 1080) Touch Display, AMD Ryzen 5 4500U Processor, 16GB DDR4, 256GB SSD, AMD Radeon Graphics, Digital Pen Included, Win 10, 81X20005US, Graphite Grey  
product_price is: $624.99  
Name is: ASUS Laptop L210 Ultra Thin Laptop, 11.6ö HD Display, Intel Celeron N4020 Processor, 4GB RAM, 64GB Storage, NumberPad, Windows 10 Home in S Mode  
product_price is: $229.99  
Name is: 2019 Apple MacBook Pro (16-inch, 16GB RAM, 1TB Storage, 2.3GHz Intel Core i9) - Space Gray  
product_price is: $2,589.00  
Name is: ASUS F512JA-AS34 VivoBook 15 Thin and Light Laptop, 15.6ö FHD Display, Intel i3-1005G1 CPU, 8GB RAM, 128GB SSD, Backlit Keyboard, Fingerprint, Windows 10 Home in S Mode, Slate Gray  
product_price is: $462.00  
Name is: Acer Chromebook Spin 311 Convertible Laptop, Intel Celeron N4020, 11.6" HD Touch, 4GB LPDDR4, 32GB eMMC, Gigabit Wi-Fi 5, Bluetooth 5.0, Google Chrome, CP311-2H-C679  
product_price is: $261.02  
Name is: Acer Predator Helios 300 Gaming Laptop, Intel i7-10750H, NVIDIA GeForce RTX 3060 Laptop GPU, 15.6" Full HD 144Hz 3ms IPS Display, 16GB DDR4, 512GB NVMe SSD, WiFi 6, RGB Keyboard, PH315-53-71HN  
product_price is: $1,349.99  
Name is: Acer Aspire 5 A515-55-56VK, 15.6" Full HD IPS Display, 10th Gen Intel Core i5-1035G1, 8GB DDR4, 256GB NVMe SSD, Intel Wireless WiFi 6 AX201, Fingerprint Reader, Backlit Keyboard, Windows 10 Home  
product_price is: $549.99  
Name is: Acer Swift 3 Thin & Light Laptop, 14" Full HD IPS, AMD Ryzen 7 4700U Octa-Core with Radeon Graphics, 8GB LPDDR4, 512GB NVMe SSD, Wi-Fi 6, Backlit KB, Fingerprint Reader, Alexa Built-in  
product_price is: $679.99  
Name is: HP 15 Laptop, 11th Gen Intel Core i5-1135G7 Processor, 8 GB RAM, 256 GB SSD Storage, 15.6ö Full HD IPS Display, Windows 10 Home, HP Fast Charge, Lightweight Design (15-dy2021nr, 2020)  
product_price is: $739.00  
Name is: SAMSUNG XE350XBA-K01US Chromebook 4 + Chrome OS 15.6" Full HD Intel Celeron Processor N4000 4GB RAM 32GbáEmmc Gigabit Wi-Fi, Silver  
product_price is: $231.46  
Name is: Lenovo Chromebook C330 2-in-1 Convertible Laptop, 11.6-Inch HD (1366 x 768) IPS Display, MediaTek MT8173C Processor, 4GB LPDDR3, 64 GB eMMC, Chrome OS, 81HY0000US, Blizzard White  
product_price is: $287.18  
Name is: ASUS F512DA-EB51 VivoBook 15 Thin and Light Laptop, 15.6ö Full HD, AMD Quad Core R5-3500U CPU, 8GB DDR4 RAM, 256GB PCIe SSD, AMD Radeon Vega 8 Graphics, Windows 10 Home, Slate Gray  
product_price is: $604.00  
Name is: Lenovo IdeaPad 3 15" Laptop, 15.6" HD (1366 x 768) Display, AMD Ryzen 3 3250U Processor, 4GB DDR4 Onboard RAM, 128GB SSD, AMD Radeon Vega 3 Graphics, Windows 10, 81W10094US, Business Black  
product_price is: $359.99  
Name is: Lenovo Legion 5 Gaming Laptop, 15.6" FHD (1920x1080) IPS Screen, AMD Ryzen 7 4800H Processor, 16GB DDR4, 512GB SSD, NVIDIA GTX 1660Ti, Windows 10, 82B1000AUS, Phantom Black  
product_price is: $1,149.00  
Name is: Lenovo Chromebook Flex 5 13" Laptop, FHD (1920 x 1080) Touch Display, Intel Core i3-10110U Processor, 4GB DDR4 Onboard RAM, 64GB eMMC, Intel Integrated Graphics, Chrome OS, 82B80006UX, Graphite Grey  
product_price is: $396.95  
Name is: ASUS VivoBook 15 F515 Thin and Light Laptop, 15.6ö FHD Display, Intel Core i3-1005G1 Processor, 4GB DDR4 RAM, 128GB PCIe SSD, Fingerprint Reader, Windows 10 Home in S Mode, Slate Grey, F515JA-AH31  
product_price is: $369.99  
Name is: Microsoft Surface Pro 7 û 12.3" Touch-Screen - 10th Gen Intel Core i5 - 8GB Memory - 128GB SSD (Latest Model) û Platinum (VDV-00001)  
product_price is: NA  
Name is: 2020 Apple MacBook Pro with Intel Processor (13-inch, 16GB RAM, 512GB SSD Storage) - Space Gray  
product_price is: $1,599.00  
Name is: Apple MacBook Air MD760LL/A 13.3-Inch Laptop (Intel Core i5 Dual-Core 1.3GHz up to 2.6GHz, 4GB RAM, 128GB SSD, Wi-Fi, Bluetooth 4.0) (Renewed)  
product_price is: $389.00  
Name is: Razer Blade 15 Base Gaming Laptop 2021: Intel Core i7-10750H 6 Core, NVIDIA GeForce RTX 3060, 15.6" FHD 1080p 144Hz, 16GB, 512GB SSD - CNC Aluminum - Chroma RGB Lighting - Thunderbolt 3  
product_price is: $1,699.99  
The current url being processed by process 0 to find the product details is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=2&qid=1621978827&ref=sr_pg_1  
Name is: Lenovo ThinkPad E14 14" FHD Business Laptop Computer, Intel Quad-Core i5 10210U Up to 4.2GHz (Beats i7-7500U), 16GB DDR4 RAM, 512GB SSD + 1TB HDD, Bluetooth 5.0, Windows 10 Pro, 64GB USB Flash Drive  
product_price is: $917.00  
Name is: LincPlus 14" Slim Metal Laptop 4GB RAM 64GB eMMC Storage Upgradeable up to 512GB Windows 10 S Intel Celeron N3350 Netbook Computer Full HD Fanless Quiet Notebook  
product_price is: $299.00  
Name is: YELLYOUTH Laptop 15.6 inch Notebook Intel Quad Core 6GB RAM 120GB SSD Full HD Display with WiFi Mini HDMI Windows 10 Laptop Computer Silver  
product_price is: $279.99  
Name is: HP Stream 11.6-inch HD Laptop, Intel Celeron N4000, 4 GB RAM, 32 GB eMMC, Windows 10 Home in S Mode with Office 365 Personal for 1 Year (11-ak0020nr, Diamond White)  
product_price is: $239.99  
Name is: Asus L510MA-DS04 15.6" Celeron N4020 4 GB RAM 128 GB eMMC  
product_price is: $354.99  
Name is: HP Chromebook 14-inch HD Laptop, Intel Celeron N4000, 4 GB RAM, 32 GB eMMC, Chrome (14a-na0020nr, Ceramic White)  
product_price is: NA  
Name is: HP Stream 14-inch Laptop, Intel Celeron N4000, 4 GB RAM, 64 GB eMMC, Windows 10 Home in S Mode with Office 365 Personal for 1 Year (14-cb186nr, Brilliant Black) (9MV74UA#ABA)  
product_price is: $271.99  
Name is: 2021 Newest Dell Inspiron 3000 Laptop, 15.6 HD LED-Backlit Display, Intel Celeron Processor N4020, 8GB DDR4 RAM, 128GB PCIe SSD, Online Meeting Ready, Webcam, WiFi, HDMI, Bluetooth, Win10 Home, Black  
product_price is: $459.00  
Name is: 2020 Flagship HP 14 Chromebook Laptop Computer 14" HD SVA Anti-Glare Display Intel Celeron Processor 4GB DDR4 64GB eMMC Backlit WiFi Webcam Chrome OS (Renewed)  
product_price is: $199.00  
Name is: HP Chromebook 14-inch HD Laptop, Intel Celeron N4000, 4 GB RAM, 32 GB eMMC, Chrome (14a-na0010nr, Mineral Silver)  
product_price is: NA  
Name is: Razer Blade 15 Base Gaming Laptop 2020: Intel Core i7-10750H 6-Core, NVIDIA GeForce RTX 2060, 15.6" FHD 1080p 144Hz, 16GB RAM, 512GB SSD, CNC Aluminum, Chroma RGB Lighting, Thunderbolt 3, Black  
product_price is: $1,479.99  
Name is: Lenovo Legion 5 15.6" Gaming Laptop 144Hz AMD Ryzen 7-4800H 16GB RAM 512GB SSD RTX 2060 6GB Phantom Black - AMD Ryzen 7 4800H Octa-core - NVIDIA GeForce RTX 2060 6GB - (IPS)  
product_price is: $1,289.99  
Name is: Samsung Chromebook 4 Chrome OS 11.6" HD Intel Celeron Processor N4000 4GB RAM 32GB eMMC Gigabit Wi-Fi - XE310XBA-K01US  
product_price is: $186.05  
Name is: 2020 Newest Acer Aspire 5 Slim Laptop 15.6" FHD IPS Display, AMD Ryzen 3 3200u (up to 3.5GHz), Vega 3 Graphics, 8GB RAM DDR4, 256GB PCIe SSD, Backlit KB,WiFi,HDMI, Win10 w/Ghost Manta Accessories  
product_price is: $479.00  
Name is: HP Chromebook 11-inch Laptop - MediaTek - MT8183 - 4 GB RAM - 32 GB eMMC Storage - 11.6-inch HD Display - with Chrome OS - (11a-na0010nr, 2020 Model)  
product_price is: $198.29  
Name is: 2021 Newest HP 15 15.6" HD Display Laptop Computer, AMD Ryzen 3 3250U(up to 3.5GHz, Beat i3-8130U), 8GB DDR4 RAM, 128GB SSD+1TB HDD, WiFi, Bluetooth, HDMI, Webcam, Remote Work, Win 10 S, AllyFlex MP  
product_price is: $499.00  

  
  Name is: 2020 Newest HP 14 Inch Premium Laptop, AMD Athlon Silver 3050U up to 3.2 GHz(Beat i5-7200U), 8GB DDR4 RAM, 128GB SSD, Bluetooth, Webcam,WiFi,Type-C, HDMI, Windows 10 S, Black + Laser HDMI  
product_price is: $399.00  
Name is: Used Chromebook in Good Condition C720 Lightweight Laptop Computer 11.6 inches 4GB RAM 16GB eMMC - Celeron 2955U Ultra-Light Design Chrome OS Online Class  
product_price is: $161.45  
Name is: Lenovo IdeaPad 3 Intel i5-1035G1 Quad Core 12GB RAM 256GB SSD 15.6-inch Touch Screen Laptop  
product_price is: $599.90  
Name is: HP 2-in-1 Convertible Chromebook, 14inch HD Touchscreen, Intel Quad-Core Pentium Silver N5030 Processor Up to 3.10GHz, 4GB Ram, 128GB SSD, Intel UHD Graphics, Webcam, Chrome OS(Renewed (14inch/128GB)  
product_price is: $288.99  
Name is: 2020 Lenovo ThinkPad E15 15.6" FHD Full HD (1920x1080) Business Laptop (Intel 10th Quad Core i5-10210U, 16GB DDR4 RAM, 512GB PCIe SSD) Type-C, HDMI, Windows 10 Pro + HDMI Cable  
product_price is: $973.91  
Name is: Apple MacBook Pro with Apple M1 Chip (13-inch, 16GB RAM, 256GB SSD Storage) - Space Gray (Latest Model) Z11B000E3  
product_price is: $1,449.99  
Name is: Newest HP Pavilion Intel Pentium Silver N5000 4GB 128GB SSD Windows 10 Laptop Red  
product_price is: $352.99  
Name is: 2021 Newest Dell Inspiron 3000 Laptop, 15.6 HD LED-Backlit Display, Intel Pentium Silver N5030 Processor, 16GB DDR4 RAM, 256GB PCIe Solid State Drive, Online Meeting Ready, Webcam, Win10 Home, Black  
product_price is: $539.00  
Name is: HP 15.6 inch HD LED Display Laptop 2020 (Intel Pentium Gold 6405U Processor, 4 GB DDR4 RAM, 128 GB SSD, HDMI, Webcam, WI-FI, Windows 10 S) Scarlet Red (Renewed)  
product_price is: $333.50  
Name is: 2021 HP Stream 14" HD Thin and Light Laptop, Intel Celeron N4000 Processor, 4GB RAM, 64GB eMMC, HDMI, Webcam, WiFi, Bluetooth, 1 Year Microsoft 365, Windows 10 S, Rose Pink, W/ IFT Accessories  
product_price is: $408.00  
Name is: Dell Gaming G3 15 3500, 15.6 inch FHD Laptop - Intel Core i5-10300H, 8GB DDR4 RAM, 512GB SSD, NVIDIA GeForce GTX 1650 Ti 4GB GDDR6 , Windows 10 Home - Eclipse Black (Latest Model)  
product_price is: $848.00  
Name is: ASUS VivoBook 17.3" FHD IPS LED Backlight Premium Laptop | AMD Ryzen3 3250U | 8GB DDR4 RAM | 256GB SSD | USB Type-C | WiFi | HDMI | Windows 10  
product_price is: $505.00  
Name is: Apple MacBook Air MJVM2LL/A 11.6 Inch Laptop (Intel Core i5 Dual-Core 1.6GHz up to 2.7GHz, 4GB RAM, 128GB SSD, Wi-Fi, Bluetooth 4.0, Integrated Intel HD Graphics 6000, Mac OS) (Renewed)  
product_price is: $384.97  
Name is: Alienware m15 R3 15.6inch FHD Gaming Laptop (Lunar Light) Intel Core i7-10750H 10th Gen, 16GB DDR4 RAM, 512GB SSD, Nvidia GeForce RTX 2060 6GB GDDR6, Windows 10 Home (AWm15-7272WHT-PUS)  
product_price is: $1,678.99  
Name is: BMAX X15 Laptop Computers, 15.6" FHD (1920 x 1080) Display, Intel 4120 up to 2.6 GHz, 8GB DDR4, 256GB SSD Storage, HDMI, Webcam, WI-FI, Windows 10 - Space Grey  
product_price is: $359.00  
Name is: Laptop Computer Notebook 14-Inch Windows-10 û WINNOVO WinBook N140 6GB RAM 64GB ROM Intel Celeron Processor HD IPS Display Numeric Touchpad 5G WiFi HDMI (Space Grey)  
product_price is: $269.99  
Name is: BMAX Y11 2 in 1 Laptop, Touchscreen 11.6" FHD (1920 x 1080) Display, 360 Degree Convertible, Intel N4120 Processor, 8GB LPDDR4, 256GB SATA SSD, Windows 10, Type-C, HDMI, All-Metal Body  
product_price is: $369.00  
url is: https://www.amazon.com/s?rh=n%3A565108&fs=true&ref=lp_565108_sar  
Current page being processed by process 3 to find the next page url is:  1 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=2&qid=1621978827&ref=sr_pg_1  
url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=2&qid=1621978827&ref=sr_pg_1  
Current page being processed by process 3 to find the next page url is:  2 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=3&qid=1621978830&ref=sr_pg_2  
url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=3&qid=1621978830&ref=sr_pg_2  
Current page being processed by process 3 to find the next page url is:  3 out of 400 pages.  
Next search url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=4&qid=1621978834&ref=sr_pg_3  
url is: https://www.amazon.com/s?i=computers&rh=n%3A565108&fs=true&page=4&qid=1621978834&ref=sr_pg_3  
Current page being processed by process 3 to find the next page url is:  4 out of 400 pages.  
Proccess 0 is responsible for the pages between 0 and 2  
Proccess 1 is responsible for the pages between 2 and 3  
Proccess 2 is responsible for the pages between 3 and 4  
Finished!  
Please check the contents of the .csv files created to see the results!  