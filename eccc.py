"""
Usage:
  eccc (-i | -s <station>...) [options]
  eccc (-h | --help)

Facilitates download of hourly, daily, or monthly climate data from Environment and Climate Change Canada

Download the data inventory:
    -i             Download the inventory of available station data and exit

Downloading station data:
    -s <station>   Station code to download. Pass the argument multiple times for more than one
                   station: e.g. -s 5051 -s 31688
    -t <timeframe> Timeframe to download: 1, hourly; 2, daily; 3, monthly [default: 2]
    -y <years>     Years to download, express multiple years as a range: e.g. 1998:2008
                   A single year can also be passed: e.g. 1998 (does not apply to monthly data)
    -m <months>    Months to download, expressed as a range: e.g. 1:12
                   If no month is given, 1:12 will be used. (only applies to hourly data)
    -g             Optional; if specified, the individual CSV files will be "glued" into a single file

Other options:
    -h --help      Show this help text
    -v --version   Print the program version and exit

Examples:
  eccc -i # downloads the data inventory csv.
  eccc -s 5051 -y 1981:2010 -g # creates a single daily .csv file for Toronto daily data
  eccc -s 5051 -y 1981:2010 -m 6:8 -t 1  # downloads hourly data for the summer months from 1981 to 2010 at Toronto
"""

from docopt import docopt
import re
import os
import sys
import urllib.request
import time

def download_file(url, filename):
    try:
        resp = urllib.request.urlretrieve(url, filename)
    except urllib.error.URLError as e:
        sys.exit("There was an error finding that file! The error was: {}".format(e))
    except urllib.error.HTTPError as e:
        sys.exit("There was an error downloading that file! The error was: {}".format(e))
    sys.exit(0)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='eccc 2.0')

    if arguments['-i']:
        print("Downloading station data inventory.")
        download_file("ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv", "Station Inventory EN.csv")

    if arguments['-t'] is None:
        timeframe = 2
    else:
        if arguments['-t'] in ['1', 'h', 'H']:
            timeframe = 1
        elif arguments['-t'][0] in ['2', "d", 'D']:
            timeframe = 2
        elif arguments['-t'][0] in ['3', 'm', 'M']:
            timeframe = 3
        else:
            sys.exit("Invalid timeframe passed.")

    if arguments['-m'] is None:
        if timeframe == 1:
            months = range(1, 13)
        else:
            months = [6]
    else:
        if timeframe != 1:
            print("Daily and monthly data is not split by month. Ignored.")
            months = [6]
        else:
            if not bool(re.search(r'(^[0-9]{1,2}$|^[0-9]{1,2}:[0-9]{1,2}$)', arguments['-m'])):
                sys.exit("Invalid month format.")
            else:
                months = [int(x) for x in arguments['-m'].split(":")]
                if any(x not in range(13) for x in months):
                    sys.exit("Months must be from 1 to 12.")
                else:
                    months = range(min(months), max(months) + 1)

    if arguments['-y'] is None:
        if timeframe != 3:
            sys.exit("Years must be specified!")
        else:
            years = [1989]
    else:
        if timeframe == 3:
            print("Monthly data is not split by year. Ignored.")
            years = [1989]
        else:
            if not bool(re.search(r'(^[0-9]{4}$|^[0-9]{4}:[0-9]{4}$)', arguments['-y'])):
                sys.exit("Invalid year format.")
            else:
                years = [int(x) for x in arguments['-y'].split(":")]
                years = range(min(years), max(years) + 1)

    for station in arguments['-s']:

        if arguments['-g']:
            first_file = True
            guess_skip = True
        else:
            first_file = False
            guess_skip = False

        for year in years:
            for month in months:
                if timeframe == 1:
                    period = "hourly"
                    filemth = "-{}".format(str(month).zfill(2))
                    fileyr = "-{}".format(year)
                elif timeframe == 2:
                    period = "daily"
                    filemth = ""
                    fileyr = "-{}".format(year)
                elif timeframe == 3:
                    period = "monthly"
                    filemth=""
                    fileyr=""

                url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={}&Year={}&Month={}&Day=14&timeframe={}&submit=Download+Data".format(station, year, month, timeframe)

                filename="{}-{}{}{}.csv".format(station, period, fileyr, filemth)

                print("Downloading", filename)
                download_file(url, filename)

                if arguments['-g']:
                    glued_filename = "{}-{}.csv".format(station, period)

                    with (open(filename, 'r')) as file:
                        lines = file.read().splitlines()

                    if guess_skip:
                        pull = lines.index(max(lines, key = len))
                        if not first_file:
                            pull += 1

                    if first_file:
                        with open(glued_filename, 'w') as file:
                            file.write("\n".join(lines[pull:]))
                            pull += 1
                            first_file = False
                    else:
                        with open(glued_filename, 'a') as file:
                            file.write("\n" + "\n".join(lines[pull:]))

                    os.remove(filename)

                time.sleep(0.5)
