import requests
from time import time
from datetime import datetime
import pytz

mvgAPI = "https://www.mvg.de/"
apiBase = mvgAPI + "api/fib/v2/departure"
stationQuery = mvgAPI + "api/fib/v2/location"
interruptionsURL = mvgAPI + ".rest/betriebsaenderungen/api/interruptions?_="
headers = {
    "gzip": "true",
    "X-Requested-With": "XMLHttpRequest",
    "X-MVG-Authorization-Key": "5af1beca494712ed38d313714d4caff6",
    "Referer": "https://www.mvg.de/dienste/abfahrtszeiten.html",
    "Accept-Encoding": "gzip",
}


def get_stationinfo(station_name):
    url = stationQuery

    params = {
        "query" : "Westendstraße" #globalId=de:09162:260
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    return response

def get_departureinfo(stationid):
    url = apiBase

    """
    qs: {
				limit: (payload.limit || payload.maxEntries || 10) + 5,
				offsetInMinutes:0,
				transportTypes: payload.transportTypes || Object.entries(payload.transportTypesToShow).filter(x => x[1]).map(x => x[0].toUpperCase()).join(","),
				globalId: payload.globalId
			}
    {
        'bannerHash': '',
        'cancelled': False,
        'delayInMinutes': 0,
        'destination': 'Neuperlach Süd',
        'divaId': '010U5',
        'label': 'U5',
        'messages': [],
        'network': 'swm',
        'occupancy': 'UNKNOWN',
        'plannedDepartureTime': 1709203980000,
        'platform': 2,
        'platformChanged': False,
        'realtime': True,
        'realtimeDepartureTime': 1709203980000,
        'sev': False,
        'stopPointGlobalId': 'de:09162:260:51:52',
        'trainType': '',
        'transportType': 'UBAHN'
    }
    """
    params = {
        "offsetInMinutes": 0,
        "globalId": "de:09162:260",
        "limit": 6
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    return response


def get_departure_html():
    departures = get_departureinfo("de:09162:260").json()
    tz = pytz.timezone('Europe/Berlin')
    html = ""
    for departure in departures:
        departuretime = departure['realtimeDepartureTime']/1000
        datetime_berlin = datetime.fromtimestamp(departuretime).astimezone(tz)
        formatted_departure = datetime_berlin.strftime('%H:%M')

        html += f"""
            <div class="container border">
                <div class="box box-one">{departure["label"]}</div>
                <div class="box box-two">{departure["destination"]}</div>
                <div class="box box-three">{formatted_departure}</div>
            </div>
        """

    return html


def get_interruptions():
    currtime = str(int(time()*1000))
    url = interruptionsURL + currtime

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    return response


def main():
    #stationinfo = get_stationinfo("Westendstraße")
    get_departureinfo("de:09162:260")
    #get_interruptions()


if __name__ == "__main__":
    main()