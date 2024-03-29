---
title: "ec3"
output: github_document
---




**ec3** is a Python module and a standalone command-line executable to search for and download historical Canadian climate data from Environment and Climate Change Canada's historical data archive. 

### Download

The **ec3** module can be installed via Anaconda from my personal Anaconda channel:


```bash
conda config --prepend channels conda-forge
conda config --append channels claut
conda install ec3
```

The module contains two functions: `ec3.find_station()`, and `ec3.get_data()`. The functions provide the same functionality as document in this README, check the function documentation for syntax.

The **ec3.py** script can also be executed directly in Python by downloading [**ec3.py**](https://gitlab.com/claut/ec3.py/raw/master/ec3.py?inline=false) running, e.g. `python ec3.py --help`. Check the [requirements](https://gitlab.com/claut/ec3.py/raw/master/requirements.txt) file for the libraries needed. 

You can also download a standalone version of **ec3** for Windows, Linux, or Mac. This version of the program includes a bundled Python interpreter and includes all of the necessary libraries so that you can run the program directly without installing any software. This version is ideal for users who have no interest in using Python, or who can't install software on their workstation (e.g. at a university computer lab). 

  - [Download for Linux](https://dav.conr.ca/ec3/lin/ec3)
  - [Download for Windows](https://dav.conr.ca/ec3/win/ec3.exe)
  - [Download for Mac](https://dav.conr.ca/ec3/mac/ec3)
  
**ec3** does not have a GUI, and therefore must be run from a terminal (or command prompt on Windows). On Linux and Mac, it will be necessary to set the application as executable by running:


```bash
chmod +x ec3
```

_Note: as of writing, this program can be considered to have been "lightly tested". Please report issues here!_

### Usage

**ec3** has three base commands: `inv`, `find`, and `get`. The examples below are showing the Linux version of the program. If you get an error that the command is not found, call the executable with the full directory path, or, if it is saved in the current directory, append `./` on Linux or Mac.


```bash
ec3 --help
```

```
## Usage:
##   ec3 inv
##   ec3 find [--name <name>] [--prov <province>...] [(--period <period> --type <type>)] [--recodes] [(--target <y> [<x>] [--dist <distance>])] [--outfile <filename>]
##   ec3 get -s <station>... [options] [--outfile <filename>]
##   ec3 (-h | --help)
##   ec3 --version
## 
## Facilitates download of hourly, daily, or monthly climate data from Environment and Climate Change Canada
## 
## Commands:
##   inv                  Download the inventory of available station data and exit
##   find                 Search through the inventory for available data (see "Search Options", below)
##   get                  Download data (see "Download Options", below)
## 
## Search Options
##   --name <name>        Filter stations by name, can use incomplete words, e.g. Tor
##   --prov <province>... Two letter code of the province (repeat as needed)
##   --period <period>    The period for which you need data, separated by a colon, e.g. 1981:2010
##   --type <type>        The type of data you are searching for (required if period is used)
##                        Options: 1, hourly; 2, daily; 3, monthly
##   --target <y> [<x>]   Either a station code, or space-separated latitude (N) and longitude (W) values
##   --dist <distance>    Colon-separated minimum and maximum distance from target [default: 0:100]
##   --recodes            Pass this flag for the program to suggest stations that may be combined to
##                        cover the period that you requested.
## 
## Downloading Options:
##   -s <station>         Station code to download. Pass the argument multiple times for more than one
##                        station: e.g. -s 5051 -s 31688
##   -t <timeframe>       Timeframe to download: 1, hourly; 2, daily; 3, monthly [default: 2]
##   -y <years>           Years to download, express multiple years as a range: e.g. 1998:2008
##                        A single year can also be passed: e.g. 1998 (does not apply to monthly data)
##   -m <months>          Months to download, expressed as a range: e.g. 1:12
##                        If no month is given, 1:12 will be used. (only applies to hourly data)
##   --noprogress         Pass this flag to hide the download progress bar.
## 
## Other options:
##   --outfile <filename> Save your search results to a csv file or override the name for the
##                        downloaded data.
##   -h --help            Show this help text
##   --version            Print the program version and exit
## 
## Examples:
##   ec3 inv # downloads the data inventory csv.
##   ec3 search --name Toronto # find stations with "Toronto" in their name
##   ec3 get -s 5051 -y 1981:2010 # creates a single daily .csv file for Toronto daily data
##   ec3 get -s 5051 -y 1981:2010 -m 6:8 -t 1 # downloads hourly data for the summer months from 1981 to 2010 at Toronto
```

#### `inv`

The `inv` command will download the most recent (English) version of the ECCC [Station Inventory](ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv) table (in CSV format). This command should be run periodically, as the inventory table is updated fairly regularly. If you are running from the command line, this is a prerequiste for the `find` command. If you are running the Python module, this file will be downloaded automatically once per session.


```bash
ec3 inv
```

```
## Downloading Station Inventory EN.csv to the current working directory
```

#### `find`

The search function is invoked by the `find` command. You can search by name, period of available data (specifying data type, hourly, daily, or monthly), but province, and by proximity to some target. 

As an example, run the following command to find, all stations with "Toronto" in their name. _Note, I have piped the output to head, because the list is very long. You should omit that `| head` section to see more results!_

```bash
ec3 find --name "Toronto" | head
```

```
##                                          Name  ... MLY Last Year
## 6478  PA TORONTO INTERNATIONAL TRAP AND SKEET  ...           NaN
## 6485             PA TORONTO NORTH YORK MOTORS  ...           NaN
## 6489              PA SCARBOROUGH TORONTO HUNT  ...           NaN
## 6492                       PA TORONTO HYUNDAI  ...           NaN
## 6551                                  TORONTO  ...        2006.0
## ...                                       ...  ...           ...
## 6644                       TORONTO CASTLEMERE  ...        1980.0
## 6669                        TORONTO TORBARRIE  ...        1984.0
## 6670                       TORONTO YORK MILLS  ...        1987.0
```

You can limit your results by province. e.g. find all stations in the province of Ontario:

```bash
ec3 find --prov ON | head
```

```
##                        Name Province  ... MLY First Year  MLY Last Year
## 5110           ATTAWAPISKAT  ONTARIO  ...         1968.0         1968.0
## 5111         ATTAWAPISKAT A  ONTARIO  ...            NaN            NaN
## 5112       BIG TROUT LAKE A  ONTARIO  ...            NaN            NaN
## 5113         BIG TROUT LAKE  ONTARIO  ...         1939.0         1992.0
## 5114  BIG TROUT LAKE READAC  ONTARIO  ...            NaN            NaN
## ...                     ...      ...  ...            ...            ...
## 6738          BANCROFT AUTO  ONTARIO  ...         1997.0         2006.0
## 6739           PETERBOROUGH  ONTARIO  ...            NaN            NaN
## 6740      BURNT RIVER-CLARK  ONTARIO  ...         1992.0         1992.0
```

_Note: You can pass more than one province by repeating the pattern, e.g._ `ec3 --prov ON --prov QC`

You can also limit your results by available data. e.g. find stations named "Toronto", with hourly data available from 1971 to 2000:

```bash
ec3 find --name Toronto --period 1971:2000 --type hourly
```

```
##                                    Name Province  ... HLY First Year  HLY Last Year
## 6595                   TORONTO ISLAND A  ONTARIO  ...         1957.0         2006.0
## 6605  TORONTO LESTER B. PEARSON INT'L A  ONTARIO  ...         1953.0         2013.0
## 
## [2 rows x 15 columns]
```

Searches can be passed a target of either a station ID (e.g. 5051), or space-separated latitude and longitude coordinates. The coordinates should be passed as decimal degrees of north latitude, and (positive) decimal degrees of west longitude. _Note: Negative numbers will not work as they are interpreted as command line flags._

e.g. find all stations between 0 and 100 km from Station No. 5051 (Toronto):

```bash
ec3 find --target 5051 --dist 0:100 | head
```

```
##                             Name Province  ... MLY Last Year                   Dist
## 6553                TORONTO CITY  ONTARIO  ...        2006.0                 0.0 km
## 6552     TORONTO SOLAR RADIATION  ONTARIO  ...           NaN                 0.0 km
## 6551                     TORONTO  ONTARIO  ...        2006.0                 0.0 km
## 6571           TORONTO DEER PARK  ONTARIO  ...        1933.0  1.9585072748342234 km
## 6491  PA MATTAMY ATHLETIC CENTRE  ONTARIO  ...           NaN  1.9587267101484753 km
## ...                          ...      ...  ...           ...                    ...
## 6711                  LORNEVILLE  ONTARIO  ...        1987.0   96.95204879552539 km
## 5920                  GAMEBRIDGE  ONTARIO  ...        1993.0   97.45417786384563 km
## 5815                 LAGOON CITY  ONTARIO  ...        2006.0   98.83674714790826 km
```

e.g. find all stations that are within 5 km of UTSC campus:

```bash
ec3 find --target 43.7838 79.1875 --dist 0:5
```

```
##                                      Name  ...                    Dist
## 6493  PA U OF T SCARBOROUGH TENNIS CENTRE  ...  0.46772058790516413 km
## 6630              TOR SCARBOROUGH COLLEGE  ...    0.736729501436302 km
## 6590               TORONTO HIGHLAND CREEK  ...   1.4706493130818032 km
## 6628                    TORONTO WEST HILL  ...    2.082271174320758 km
## 6607                      TORONTO MALVERN  ...    3.865321295320793 km
## 6570                  TORONTO CURRAN HALL  ...     3.88797634214092 km
## 6609                    TORONTO METRO ZOO  ...    4.067153857612105 km
## 6524                          ROUGE HILLS  ...    4.965652205701927 km
## 
## [8 rows x 20 columns]
```

Finally, there have been a number of cases where the same station has changed name and ID over its history. In this case, filtering by the period of available data might exclude these stations. If you would like the have **ec3** try to identify these cases, use the `--recodes` command line flag. The program will report any combination for which the coordinates are the same, and which, together, provide sufficient data. 


```bash
ec3 find --period 1981:2010 --type 2 --target 5051 --dist 0:10 --recodes
```

```
## Note: In addition to the stations found, the following combinations may provide sufficient baseline data.
## 
## 
## >> Combination 1 at coordinates 43.63 -79.4 
## 
## Station 5085 : TORONTO ISLAND A (1957-2006)
## Station 5086 : TORONTO IS A (AUT) (1973-1973)
## Station 30247 : TORONTO CITY CENTRE (2006-2014)
## Station 48549 : TORONTO CITY CENTRE (2010-2021)
## 
## 
##          Name Province Climate ID  ...  DLY First Year  DLY Last Year    Dist
## 6551  TORONTO  ONTARIO    6158350  ...          1840.0         2017.0  0.0 km
## 
## [1 rows x 16 columns]
```

By default, the results of a search are not saved. The output will also likely be truncated due to some of Pythons print limitations. To save the full results to a CSV file, pass the `--outfile` flag with a filename: 

```bash
ec3 find --name "Toronto" --outfile results.csv | head
```

```
##                                          Name  ... MLY Last Year
## 6478  PA TORONTO INTERNATIONAL TRAP AND SKEET  ...           NaN
## 6485             PA TORONTO NORTH YORK MOTORS  ...           NaN
## 6489              PA SCARBOROUGH TORONTO HUNT  ...           NaN
## 6492                       PA TORONTO HYUNDAI  ...           NaN
## 6551                                  TORONTO  ...        2006.0
## ...                                       ...  ...           ...
## 6644                       TORONTO CASTLEMERE  ...        1980.0
## 6669                        TORONTO TORBARRIE  ...        1984.0
## 6670                       TORONTO YORK MILLS  ...        1987.0
```

The results can then be explored in a spreadsheet program or in Python, R, etc.

```bash
cat results.csv | head
```

```
## Name,Province,Climate ID,Station ID,WMO ID,TC ID,Latitude (Decimal Degrees),Longitude (Decimal Degrees),Latitude,Longitude,Elevation (m),First Year,Last Year,HLY First Year,HLY Last Year,DLY First Year,DLY Last Year,MLY First Year,MLY Last Year
## PA TORONTO INTERNATIONAL TRAP AND SKEET,ONTARIO,6156159,52731,,Z5N,44.19,-79.66,441108100,-793950800,234.5,2014,2015,2014.0,2015.0,,,,
## PA TORONTO NORTH YORK MOTORS,ONTARIO,6156168,52678,,L1D,43.72,-79.47,434307100,-792807400,186.5,2014,2015,2014.0,2015.0,,,,
## PA SCARBOROUGH TORONTO HUNT,ONTARIO,6156172,52641,,L2A,43.68,-79.27,434100000,-791614900,133.5,2014,2015,2014.0,2015.0,,,,
## PA TORONTO HYUNDAI,ONTARIO,6156177,52640,,L1C,43.7,-79.45,434156200,-792705700,186.5,2014,2015,2014.0,2015.0,,,,
## TORONTO,ONTARIO,6158350,5051,71266.0,,43.67,-79.4,434000000,-792400000,112.5,1840,2017,1953.0,1969.0,1840.0,2017.0,1840.0,2006.0
## TORONTO SOLAR RADIATION,ONTARIO,6158352,41863,71626.0,TRF,43.67,-79.4,434000000,-792400000,166.0,2018,2018,,,2018.0,2018.0,,
## TORONTO CITY,ONTARIO,6158355,31688,71508.0,XTO,43.67,-79.4,434000000,-792400000,112.5,2002,2021,2002.0,2021.0,2002.0,2021.0,2003.0,2006.0
## TORONTO CITY CENTRE,ONTARIO,6158359,48549,71265.0,YTZ,43.63,-79.4,433739000,-792346000,76.8,2009,2021,2009.0,2021.0,2010.0,2021.0,,
## TORONTO AGINCOURT,ONTARIO,6158363,5052,,,43.78,-79.27,434700000,-791600000,179.8,1895,1968,,,1895.0,1968.0,1895.0,1968.0
```

#### `get`

When you are ready to download the data, you can do so using the `get` command. `get` takes the following information: 

- `-s <station>`: the station code to download; this can be passed multiple times to download multiple stations. 
- `-t <timeframe`: the time frame to download: 1, hourly, 2, daily [default], or 3, monthly.
- `-y <years>`: colon-separated start and end years (or single year) e.g. `1981:2010` (not needed for monthly data)
- `-m <months>`: colon-separated start and end months (or single month) e.g. `6:8` (only used for hourly data)

In the examples below, I will use the `--noprogress` flag to hide the progress bar, because it doesn't look nice in the README. You can omit that option so that you can track the files as they are being downloaded.

As an example, let's get the hourly spring data for Toronto Pearson in 1989 and 1990.

```bash
ec3 get -s 5097 -t 1 -y 1989:1990 -m 3:5 --noprogress
```

```
## Saving data to 5097-hourly-1989-1990-m3-5.csv
```

By default, the data will be saved to a filename called _&lt;station&lg;-&lt;timeframe&gt;-&lt;years&gt;&lt;months&gt;.csv_. To change the filename, pass the `--outfile` flag, as we did to save search results. 


```bash
ec3 get -s 5097 -t 1 -y 1989 -m 4 --noprogress --outfile a_nerd_is_born.csv
```

```
## Saving data to a_nerd_is_born.csv
```


```bash
cat a_nerd_is_born.csv | head -75 | tail -1 
```

```
## 5097,-79.63,43.68,TORONTO LESTER B. PEARSON INT'L A,6158733,1989-04-04 01:00,1989,4,4,01:00,4.4,,4.4,,100,,11.0,,15,,0.0,,99.11,,,,,,Fog
```

### Notes

**ec3** is my third offering of an "eccc" program. The first implementation was an R package that was deprecated in favour of [**canadaHCD**](https://github.com/gavinsimpson/canadaHCD) and [**canadaHCDx**](https://gitlab.com/ConorIA/canadaHCDx/). After encountering lab mates who do not use R, I implemented "eccc" as a [bash script](https://gitlab.com/ConorIA/shell-scripts/blob/master/eccc/eccc), however that version still required some relatively complex set-up on Windows (Cygwin or WSL). The name **ec3** is a play on the fact that it is both the third version of "eccc", and that there are three C's in "eccc".

As of the time of writing, **ec3** is really just a Python port of the "eccc" shell script, and the `find_stations()` functionality of **canadaHCDx**. Plans for the future include cleaning up the code and adding some more defensive programming to the module's functions (there aren't really any checks at the moment). Finally, the file size for the standalone binaries is currently very large. I hope to reduce this size if possible.

_The version of **ec3** used to generate this README was **ec3 2.1.8**._


