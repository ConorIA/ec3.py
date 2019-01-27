ec3
================

**ec3** is a Python program and a standalone command-line executable to search for and download historical Canadian climate data from Environment and Climate Change Canada's historical data archive.

### Download

**ec3** can be executed via Python by downloading [**ec3.py**](https://gitlab.com/ConorIA/ec3.py/raw/master/ec3.py?inline=false) and executing via Python, e.g. `python ec3.py --help`. Check the [requirements](https://gitlab.com/ConorIA/ec3.py/raw/master/requirements.txt) file for the libraries needed.

You can also download a standalone version of **ec3** for Windows, Linux, or Mac. This version of the program includes a bundled Python interpreter and includes all of the necessary libraries so that you can run the program directly without installing any software. This version is ideal for users who have no interest in using Python, or who can't install software on their workstation (e.g. at a university computer lab).

-   [Download for Linux](https://dav.conr.ca/ec3/lin/ec3)
-   [Download for Windows](https://dav.conr.ca/ec3/win/ec3.exe)
-   [Download for Mac](https://dav.conr.ca/ec3/mac/ec3)

**ec3** does not have a GUI, and therefore must be run from a terminal (or command prompt on Windows). On Linux and Mac, it will be necessary to set the application as executable by running:

``` bash
chmod +x ec3
```

*Note: as of writing, the Linux and Windows versions are lightly tested. The Mac version has not been tested. Please report issues here!*

### Usage

**ec3** has three base commands: `inv`, `find`, and `get`. Note, that the usage examples below are showing the Linux version of the program. On Windows, you should use `ec3.exe` instead of `ec3`. For a full description of all available commands and options, type:

``` bash
./ec3 --help
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

#### `inv`

The `inv` command will download the most recent (English) version of the ECCC [Station Inventory](ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv) table (in CSV format). This command should be run periodically, as the inventory table is updated fairly regularly. This command is also a prerequisite to any of the search functions.

*I may make the download automatic in the future, but 1.3 MB is not a trivial amount to download on each run and I have not delved into caching the table the way that I do in [**canadaHCDx**](https://gitlab.com/ConorIA/canadaHCDx/blob/master/R/get_station_data.R). Contributions are welcome.*

``` bash
./ec3 inv
```

    ## Downloading Station Inventory EN.csv to current working directory

#### `find`

The search function is invoked by the `find` command. You can search by name, period of available data (specifying data type, hourly, daily, or monthly), but province, and by proximity to some target.

As an example, run the following command to find, all stations with "Toronto" in their name. *Note, I have piped the output to head, because the list is very long. You should omit that `| head` section to see more results!*

``` bash
./ec3 find --name "Toronto" | head
```

    ##                           Name Province  ... MLY First Year  MLY Last Year
    ## 6537                   TORONTO  ONTARIO  ...         1840.0         2006.0
    ## 6538   TORONTO SOLAR RADIATION  ONTARIO  ...            NaN            NaN
    ## 6539              TORONTO CITY  ONTARIO  ...         2003.0         2006.0
    ## 6540       TORONTO CITY CENTRE  ONTARIO  ...            NaN            NaN
    ## 6541         TORONTO AGINCOURT  ONTARIO  ...         1895.0         1968.0
    ## 6542    TORONTO ASHBRIDGES BAY  ONTARIO  ...         1958.0         1997.0
    ## 6543       TORONTO BALMY BEACH  ONTARIO  ...         1953.0         1955.0
    ## 6544       TORONTO BEACON ROAD  ONTARIO  ...         1962.0         1975.0
    ## 6545        TORONTO BERMONDSEY  ONTARIO  ...         1973.0         1984.0

You can limit your results by province. e.g. find all stations in the province of Ontario:

``` bash
./ec3 find --prov ON | head
```

    ##                            Name Province  ... MLY First Year  MLY Last Year
    ## 5099               ATTAWAPISKAT  ONTARIO  ...         1968.0         1968.0
    ## 5100             ATTAWAPISKAT A  ONTARIO  ...            NaN            NaN
    ## 5101           BIG TROUT LAKE A  ONTARIO  ...            NaN            NaN
    ## 5102             BIG TROUT LAKE  ONTARIO  ...         1939.0         1992.0
    ## 5103      BIG TROUT LAKE READAC  ONTARIO  ...            NaN            NaN
    ## 5104             BIG TROUT LAKE  ONTARIO  ...            NaN            NaN
    ## 5105           CENTRAL PATRICIA  ONTARIO  ...         1953.0         1978.0
    ## 5106                  DONA LAKE  ONTARIO  ...         1990.0         1990.0
    ## 5107                  EAR FALLS  ONTARIO  ...         1928.0         1999.0

*Note: You can pass more than one province by repeating the pattern, e.g.* `./ec3 --prov ON --prov QC`

You can also limit your results by available data. e.g. find stations named "Toronto", with hourly data available from 1971 to 2000:

``` bash
./ec3 find --name Toronto --period 1971:2000 --type hourly
```

    ##                                    Name Province  ... HLY First Year  HLY Last Year
    ## 6581                   TORONTO ISLAND A  ONTARIO  ...         1957.0         2006.0
    ## 6591  TORONTO LESTER B. PEARSON INT'L A  ONTARIO  ...         1953.0         2013.0
    ## 
    ## [2 rows x 15 columns]

Searches can be passed a target of either a station ID (e.g. 5051), or space-separated latitude and longitude coordinates. The coordinates should be passed as decimal degrees of north latitude, and (positive) decimal degrees of west longitude. *Note: Negative numbers will not work as they are interpreted as command line flags.*

e.g. find all stations between 0 and 100 km from Station No. 5051 (Toronto):

``` bash
./ec3 find --target 5051 --dist 0:100 | head
```

    ##                                 Name  ...                   Dist
    ## 6539                    TORONTO CITY  ...                 0.0 km
    ## 6538         TORONTO SOLAR RADIATION  ...                 0.0 km
    ## 6537                         TORONTO  ...                 0.0 km
    ## 6557               TORONTO DEER PARK  ...  1.9585072748345755 km
    ## 6477      PA MATTAMY ATHLETIC CENTRE  ...   1.958726710148121 km
    ## 6618              TORONTO SHERBOURNE  ...  3.2853644805861606 km
    ## 6462  PA DUFFERIN AND ST. CLAIR CIBC  ...  3.4116926360325173 km
    ## 6555               TORONTO BROADVIEW  ...  4.0324702425710255 km
    ## 6588               TORONTO LEASIDE S  ...   4.118383821538006 km

e.g. find all stations that are within 5 km of UTSC campus:

``` bash
./ec3 find --target 43.2860 79.1873 --dist 0:5
```

    ##                    Name Province  ... MLY Last Year                  Dist
    ## 6074  PORT WELLER (AUT)  ONTARIO  ...        2006.0  4.800419249348278 km
    ## 
    ## [1 rows x 20 columns]

Finally, there have been a number of cases where the same station has changed name and ID over its history. In this case, filtering by the period of available data might exclude these stations. If you would like the have **ec3** try to identify these cases, use the `--recodes` command line flag. The program will report any combination for which the coordinates are the same, and which, together, provide sufficient data.

``` bash
./ec3 find --period 1981:2010 --type 2 --target 5051 --dist 0:10 --recodes
```

    ## Note: In addition to the stations found, the following combinations may provide sufficient baseline data.
    ## 
    ## 
    ## >> Combination 1 at coordinates 43.63 -79.4 
    ## 
    ## Station 48549: TORONTO CITY CENTRE
    ## Station 30247: TORONTO CITY CENTRE
    ## Station 5086: TORONTO IS A (AUT)
    ## Station 5085: TORONTO ISLAND A
    ## 
    ## 
    ##          Name Province Climate ID  ...  DLY First Year  DLY Last Year    Dist
    ## 6537  TORONTO  ONTARIO    6158350  ...          1840.0         2017.0  0.0 km
    ## 
    ## [1 rows x 16 columns]

By default, the results of a search are not saved. The output will also likely be truncated due to some of Pythons print limitations. To save the full results to a CSV file, pass the `--outfile` flag with a filename:

``` bash
./ec3 find --name "Toronto" --outfile results.csv | head
```

    ##                           Name Province  ... MLY First Year  MLY Last Year
    ## 6537                   TORONTO  ONTARIO  ...         1840.0         2006.0
    ## 6538   TORONTO SOLAR RADIATION  ONTARIO  ...            NaN            NaN
    ## 6539              TORONTO CITY  ONTARIO  ...         2003.0         2006.0
    ## 6540       TORONTO CITY CENTRE  ONTARIO  ...            NaN            NaN
    ## 6541         TORONTO AGINCOURT  ONTARIO  ...         1895.0         1968.0
    ## 6542    TORONTO ASHBRIDGES BAY  ONTARIO  ...         1958.0         1997.0
    ## 6543       TORONTO BALMY BEACH  ONTARIO  ...         1953.0         1955.0
    ## 6544       TORONTO BEACON ROAD  ONTARIO  ...         1962.0         1975.0
    ## 6545        TORONTO BERMONDSEY  ONTARIO  ...         1973.0         1984.0

The results can then be explored in a spreadsheet program or in Python, R, etc.

``` bash
cat results.csv | head
```

    ## Name,Province,Climate ID,Station ID,WMO ID,TC ID,Latitude (Decimal Degrees),Longitude (Decimal Degrees),Latitude,Longitude,Elevation (m),First Year,Last Year,HLY First Year,HLY Last Year,DLY First Year,DLY Last Year,MLY First Year,MLY Last Year
    ## TORONTO,ONTARIO,6158350,5051,71266.0,,43.67,-79.4,434000000,-792400000,112.5,1840,2017,1953.0,1969.0,1840.0,2017.0,1840.0,2006.0
    ## TORONTO SOLAR RADIATION,ONTARIO,6158352,41863,71626.0,TRF,43.67,-79.4,434000000,-792400000,166.0,2018,2018,,,2018.0,2018.0,,
    ## TORONTO CITY,ONTARIO,6158355,31688,71508.0,XTO,43.67,-79.4,434000000,-792400000,112.5,2002,2019,2002.0,2019.0,2002.0,2019.0,2003.0,2006.0
    ## TORONTO CITY CENTRE,ONTARIO,6158359,48549,71265.0,YTZ,43.63,-79.4,433739000,-792346000,76.8,2009,2019,2009.0,2019.0,2010.0,2019.0,,
    ## TORONTO AGINCOURT,ONTARIO,6158363,5052,,,43.78,-79.27,434700000,-791600000,179.8,1895,1968,,,1895.0,1968.0,1895.0,1968.0
    ## TORONTO ASHBRIDGES BAY,ONTARIO,6158370,5053,,,43.67,-79.32,434000000,-791900000,74.1,1958,1997,,,1958.0,1997.0,1958.0,1997.0
    ## TORONTO BALMY BEACH,ONTARIO,6158381,5054,,,43.67,-79.28,434000000,-791700000,99.1,1953,1956,,,1953.0,1956.0,1953.0,1955.0
    ## TORONTO BEACON ROAD,ONTARIO,6158384,5055,,,43.75,-79.27,434500000,-791600000,167.6,1962,1975,,,1962.0,1975.0,1962.0,1975.0
    ## TORONTO BERMONDSEY,ONTARIO,6158385,5056,,,43.72,-79.32,434300000,-791900000,138.4,1973,1984,,,1973.0,1984.0,1973.0,1984.0

#### `get`

When you are ready to download the data, you can do so using the `get` command. `get` takes the following information:

-   `-s <station>`: the station code to download; this can be passed multiple times to download multiple stations.
-   `-t <timeframe`: the time frame to download: 1, hourly, 2, daily \[default\], or 3, monthly.
-   `-y <years>`: colon-separated start and end years (or single year) e.g. `1981:2010` (not needed for monthly data)
-   `-m <months>`: colon-separated start and end months (or single month) e.g. `6:8` (only used for hourly data)

As an example, let's get the hourly spring data for Toronto Pearson in 1989 and 1990.

``` bash
./ec3 get -s 5097 -t 1 -y 1989:1990 -m 3:5
```

    ## Downloading 5097-hourly-1989-03.csv to /tmp/tmpqb45bjtw
    ## Downloading 5097-hourly-1989-04.csv to /tmp/tmpqb45bjtw
    ## Downloading 5097-hourly-1989-05.csv to /tmp/tmpqb45bjtw
    ## Downloading 5097-hourly-1990-03.csv to /tmp/tmpqb45bjtw
    ## Downloading 5097-hourly-1990-04.csv to /tmp/tmpqb45bjtw
    ## Downloading 5097-hourly-1990-05.csv to /tmp/tmpqb45bjtw
    ## Saving data to 5097-hourly.csv

By default, the data will be saved to a filename called *&lt;station≶-&lt;timeframe&gt;.csv*. To change the filename, pass the `--outfile` flag, as we did to save search results.

``` bash
./ec3 get -s 5097 -t 1 -y 1989 -m 4 --outfile a_nerd_is_born.csv
```

    ## Downloading 5097-hourly-1989-04.csv to /tmp/tmps47tsumi
    ## Saving data to a_nerd_is_born.csv

``` bash
cat a_nerd_is_born.csv | head -75 | tail -1 
```

    ## 1989-04-04 01:00,1989,4,4,01:00,4.4,,4.4,,100,,11.0,,15,,0.0,,99.11,,,,,,Fog

### Notes

**ec3** is my third offering of an "eccc" program. The first implementation was an R package that was deprecated in favour of [**canadaHCD**](https://github.com/gavinsimpson/canadaHCD) and [**canadaHCDx**](https://gitlab.com/ConorIA/canadaHCDx/). After encountering lab mates who do not use R, I implemented "eccc" as a [bash script](https://gitlab.com/ConorIA/shell-scripts/blob/master/eccc/eccc), however that version still required some relatively complex set-up on Windows (Cygwin or WSL). The name **ec3** is a play on the fact that it is both the third version of "eccc", and that there are three C's in "eccc".

As of the time of writing, **ec3** is really just a Python port of the "eccc" shell script, and the `find_stations()` functionality of **canadaHCDx**. Plans for the future include restructuring the program so that it can be imported as a Python module and used directly in Python as well as on the command line. Again, contributions are most welcome.

Finally, the file size for the standalone binaries is currently very large. I hope to reduce this size if possible.
