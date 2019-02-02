"""
Usage:
  ec3 inv
  ec3 find [--name <name>] [--prov <province>...] [(--period <period> --type <type>)] [--recodes] [(--target <y> [<x>] [--dist <distance>])] [--outfile <filename>]
  ec3 get -s <station>... [options] [--outfile <filename>]
  ec3 (-h | --help)
  ec3 --version

Facilitates download of hourly, daily, or monthly climate data from Environment and Climate Change Canada

Commands:
  inv                  Download the inventory of available station data and exit
  find                 Search through the inventory for available data (see "Search Options", below)
  get                  Download data (see "Download Options", below)

Search Options
  --name <name>        Filter stations by name, can use incomplete words, e.g. Tor
  --prov <province>... Two letter code of the province (repeat as needed)
  --period <period>    The period for which you need data, separated by a colon, e.g. 1981:2010
  --type <type>        The type of data you are searching for (required if period is used)
                       Options: 1, hourly; 2, daily; 3, monthly
  --target <y> [<x>]   Either a station code, or space-separated latitude (N) and longitude (W) values
  --dist <distance>    Colon-separated minimum and maximum distance from target [default: 0:100]
  --recodes            Pass this flag for the program to suggest stations that may be combined to
                       cover the period that you requested.

Downloading Options:
  -s <station>         Station code to download. Pass the argument multiple times for more than one
                       station: e.g. -s 5051 -s 31688
  -t <timeframe>       Timeframe to download: 1, hourly; 2, daily; 3, monthly [default: 2]
  -y <years>           Years to download, express multiple years as a range: e.g. 1998:2008
                       A single year can also be passed: e.g. 1998 (does not apply to monthly data)
  -m <months>          Months to download, expressed as a range: e.g. 1:12
                       If no month is given, 1:12 will be used. (only applies to hourly data)

Other options:
  --outfile <filename> Save your search results to a csv file or override the name for the
                       downloaded data.
  -h --help            Show this help text
  --version            Print the program version and exit

Examples:
  ec3 inv # downloads the data inventory csv.
  ec3 search --name Toronto # find stations with "Toronto" in their name
  ec3 get -s 5051 -y 1981:2010 # creates a single daily .csv file for Toronto daily data
  ec3 get -s 5051 -y 1981:2010 -m 6:8 -t 1 # downloads hourly data for the summer months from 1981 to 2010 at Toronto
"""

from docopt import docopt
import re
import os
from sys import exit
import urllib.request
import pandas as pd
from time import sleep
from geopy.distance import distance
from operator import itemgetter
from warnings import warn
from tempfile import mkdtemp


def download_file(url, filename):
    print("Downloading", os.path.basename(filename), "to",
          os.path.dirname(filename) if os.path.dirname(filename) != '' else "current working directory")
    try:
        resp = urllib.request.urlretrieve(url, filename)
    except urllib.error.URLError as e:
        raise Exception("There was an error finding that file! The error was: {}".format(e))
    except urllib.error.HTTPError as e:
        raise Exception("There was an error downloading that file! The error was: {}".format(e))


def guess_skip(filename):
    with (open(filename, 'r')) as file:
        lines = file.read().splitlines()
    return lines.index(max(lines, key = len))


def station_search(name=None, province=None, period=None, type=None, detect_recodes=False, target=None, dist=range(101)):

    filename = "Station Inventory EN.csv"
    if not os.path.isfile(filename):
        raise Exception("Cannot find the station inventory. Download it with 'ec3 inv'")

    inv = pd.read_csv(filename, skiprows = guess_skip(filename))
    # Correct some placeholder coordinates (list comp because otherwise I get warnings)
    inv['Latitude (Decimal Degrees)'] = [i if i != 40 else '' for i in inv['Latitude (Decimal Degrees)']]
    inv['Longitude (Decimal Degrees)'] = [i if i != -50 else '' for i in inv['Longitude (Decimal Degrees)']]

    filt = inv.copy()

    if name is not None:
        nmreg = re.compile(name, flags = re.IGNORECASE)
        filt = filt[filt.Name.isin(list(filter(nmreg.match, filt.Name)))]

        if filt.shape[0] == 0:
            print("No results!")
            return

    if province is not None:
        p_pass = [i.upper() for i in province]
        p_codes = ["AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE",
                    "QC", "SK", "YT"]
        if all([len(i) == 2 for i in p_pass]):
            if not all([i.upper() in p_codes for i in province]):
                raise Exception("Incorrect province code(s) provided.")
            indeces = [i for i, x in enumerate([i in p_pass for i in p_codes]) if x]
            pull_prov = itemgetter(*indeces)(sorted(list(set(inv.Province))))
            if isinstance(pull_prov, str):
                pull_prov = [pull_prov]

            filt = filt[filt.Province.isin(pull_prov)]

        if filt.shape[0] == 0:
            print("No results!")
            return

    # Next, set the data we are interested in, if necessary
    if period is not None:
        if type is None:
            warn("No data type passed. Ignoring data filter.")
        else:
            if type == 1 or type[0] in ['1', 'h', 'H']:
                wantcols = ['HLY First Year', 'HLY Last Year']
                dropcols = ['DLY First Year', 'DLY Last Year', 'MLY First Year', 'MLY Last Year']
            elif type == 2 or type[0] in ['2', 'd', 'D']:
                wantcols = ['DLY First Year', 'DLY Last Year']
                dropcols = ['HLY First Year', 'HLY Last Year', 'MLY First Year', 'MLY Last Year']
            elif type == 3 or type[0] in ['3' 'm', 'M']:
                wantcols = ['MLY First Year', 'MLY Last Year']
                dropcols = ['HLY First Year', 'HLY Last Year', 'DLY First Year', 'DLY Last Year']
            else:
                period = None
                warn("Invalid data type passed. Ignoring data filter.")

    if target is not None:
        if isinstance(target, int):
            coords = inv[['Latitude (Decimal Degrees)', 'Longitude (Decimal Degrees)']][inv['Station ID'] == target]
            p1 = tuple(coords.values[0])
        elif len(target) == 2:
            p1 = target

        filt = filt.assign(Dist = filt[['Latitude (Decimal Degrees)', 'Longitude (Decimal Degrees)']].apply(lambda x: distance(tuple(x), p1), axis = 1))
        filt = filt[(filt.Dist <= max(dist)) & (filt.Dist >= min(dist))]

        if filt.shape[0] == 0:
            print("No results!")
            return

        filt = filt.sort_values('Dist')

    if period is not None:
        filt = filt.drop(dropcols, axis=1)
        inside = filt[(filt[wantcols[0]] <= min(period)) & (filt[wantcols[1]] >= max(period))]
        outside = filt[~filt['Station ID'].isin(inside['Station ID'])]
        filt = inside

        if detect_recodes:
            # Try to detected cases where the StationID has changed
            coords = outside[['Station ID', 'Latitude (Decimal Degrees)', 'Longitude (Decimal Degrees)']].groupby(['Latitude (Decimal Degrees)', 'Longitude (Decimal Degrees)']).count().reset_index()
            coords = coords[coords['Station ID'] > 1]
            printed = False
            for rw in coords.index:
                dups = outside[(outside['Latitude (Decimal Degrees)'] == coords['Latitude (Decimal Degrees)'][rw]) &
                               (outside['Longitude (Decimal Degrees)'] == coords['Longitude (Decimal Degrees)'][rw])]
                if (~dups[wantcols[0]].isnull().any()) & (min(dups[wantcols[0]]) <= min(period)):
                    if (~dups[wantcols[1]].isnull().any()) & (max(dups[wantcols[1]]) >= max(period)):
                        if min(dups[wantcols[1]]) <= max(dups[wantcols[0]]):
                            if not printed:
                                print("Note: In addition to the stations found, the following combinations may provide sufficient baseline data.\n\n")
                                printed = True
                                combo = 1
                            print(">> Combination", combo, "at coordinates", coords['Latitude (Decimal Degrees)'][rw], \
                                  coords['Longitude (Decimal Degrees)'][rw], "\n")
                            for r in range(dups.shape[0]):
                                print("Station {}: {}".format(dups.iloc[[r]]['Station ID'].values[0], dups.iloc[[r]].Name.values[0]))
                            print("\n")
                            combo += combo

        if filt.shape[0] == 0:
            print("No results!")
            return

    return filt


def get_data(stations=None, timeframe=2, years=None, months=range(1,13)):

    tempdir = mkdtemp()

    if not timeframe in [1, 2, 3]:
        if not re.search('1|H|h|2|D|d|3|M|m', timeframe):
            raise Exception("Invalid timeframe passed.")
        elif timeframe[0] in ['1', 'h', 'H']:
            timeframe = 1
        elif timeframe[0] in ['2', "d", 'D']:
            timeframe = 2
        else:
            timeframe = 3

    if isinstance(months, int):
        months = [months]

    if timeframe != 1:
        ## Daily and monthy data are not split by month.
        months = [6]

    if years is None:
        if timeframe != 3:
            raise Exception("Years must be specified!")
        else:
            years = [1989]
    else:
        if timeframe == 3:
            print("Monthly data is not split by year. Ignored.")
            years = [1989]

    for station in stations:

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
                filename = os.path.join(tempdir, "{}-{}{}{}.csv".format(station, period, fileyr, filemth))
                download_file(url, filename)

                try:
                    dat
                except NameError:
                    dat = pd.read_csv(filename, skiprows = guess_skip(filename)).assign(Station=station)
                else:
                    dat = dat.append(pd.read_csv(filename, skiprows = guess_skip(filename)).assign(Station=station))

                sleep(0.5)

    cols = dat.columns.tolist()
    return dat[cols[-1:] + cols[:-1]]


if __name__ == '__main__':
    arguments = docopt(__doc__, version='ec3 2.0')

    DEBUG = os.getenv('DEBUG', False)

    if DEBUG:
        print(arguments)

    if arguments['find']:
        if arguments['--period'] is not None:
            if not bool(re.search(r'(^[0-9]{4}$|^[0-9]{4}:[0-9]{4}$)', arguments['--period'])):
                warn("Invalid period format.")
                period = None
            else:
                period = [int(x) for x in arguments['--period'].split(":")]
        else:
            period = None

        if arguments['--target'] is not None:
            if arguments['<x>'] is None:
                try:
                    target = int(arguments['--target'])
                except ValueError:
                    exit("Target value could not be coerced to integer. Typo?")
            else:
                try:
                    target = float(arguments['--target'])
                except ValueError:
                    exit("Latitude value could not be coerced to a number. Typo?")
                try:
                    target = (target, -float(arguments['<x>']))
                except ValueError:
                    exit("Longitude value could not be coerced to a number. Typo?")
        else:
            target = None

        if arguments['--dist'] is not None:
            if not bool(re.search(r'(^[0-9]{1,4}:[0-9]{1,4}$)', arguments['--dist'])):
                warn("Invalid dist format.")
                dist = range(101)
            else:
                dist = [int(x) for x in arguments['--dist'].split(":")]
                dist = range(min(dist), max(dist) + 1)
        else:
            dist = None

        province = None if len(arguments['--prov']) == 0 else arguments['--prov']

        results = station_search(name=arguments['--name'], province=province,
                                 period=period, type=arguments['--type'],
                                 detect_recodes=arguments['--recodes'],
                                 target=target, dist=dist)

        if results is not None:
            if arguments['--outfile'] is not None:
                results.to_csv(arguments['--outfile'], index=False)
            print(results)

        exit(0)

    if arguments['inv']:
        download_file("ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv", "Station Inventory EN.csv")
        exit(0)

    if arguments['get']:

        if not arguments['-t'] in [1, 2, 3]:
            if not re.search('1|H|h|2|D|d|3|M|m', arguments['-t']):
                exit("Invalid timeframe passed.")
            elif arguments['-t'][0] in ['1', 'h', 'H']:
                timeframe = 1
            elif arguments['-t'][0] in ['2', "d", 'D']:
                timeframe = 2
            else:
                timeframe = 3

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
                    raise Exception("Invalid month format.")
                else:
                    months = [int(x) for x in arguments['-m'].split(":")]
                    if any(x not in range(13) for x in months):
                        raise Exception("Months must be from 1 to 12.")
                    else:
                        months = range(min(months), max(months) + 1)

        if arguments['-y'] is None:
            if timeframe != 3:
                stop("Years must be specified!")
            else:
                years = [1989]
        else:
            if timeframe == 3:
                print("Monthly data is not split by year. Ignored.")
                years = [1989]
            else:
                if not bool(re.search(r'(^[0-9]{4}$|^[0-9]{4}:[0-9]{4}$)', arguments['-y'])):
                    stop("Invalid year format.")
                else:
                    years = [int(x) for x in arguments['-y'].split(":")]
                    years = range(min(years), max(years) + 1)

        OUT = get_data(stations=arguments['-s'], timeframe=timeframe,
                       years=years, months=months)

        if arguments['--outfile'] is not None:
            outfile = arguments['--outfile']
        else:
            outfile = "{}-{}-{}{}.csv".format(
              '+'.join(['5051', '5097']),
              ['hourly', 'daily', 'monthly'][timeframe - 1],
              re.sub(':', '-', arguments['-y']),
              '' if timeframe != 1 or arguments['-s'] is None else '-m' + re.sub(':', '-', arguments['-m']))
        print("Saving data to", outfile)
        OUT.to_csv(outfile, index=False)
        exit(0)
