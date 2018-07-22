#! /bin/python/env
# Author: github.com/rush-dev

import requests
import argparse
import time
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description='This utility submits a URL to urlscan.io and posts the results to the terminal.'
)

# Required arguments
required = parser.add_argument_group('required arguments')
required.add_argument(
    "-u",
    "--url",
    help="submits a single URL for review.",
    action="store",
    type=str,
    required=True)

args = parser.parse_args()

def url_scan(url):
    api_key = 'ENTER-API-KEY-HERE'
    base_url = 'https://urlscan.io/api/v1/scan/'
    headers = {"Content-Type": "application/json", "API-Key": "%s" % api_key}
    data = '{"url": "%s"}' % url

    request = requests.post(base_url, headers=headers, data=data)
    response = request.json()


    uuid = response['uuid']
    message = response['message']
    result = response['result']
    api_results = response['api']
    visibility = response['visibility']
    print(f'Message:          {message}')
    print(f'ScanID:           {uuid}')
    print(f'Visibility:       {visibility}')
    print(f'Results Page:     {result}')
    print(f'Results API Page: {api_results}')

    # Results page takes about 30 seconds to complete / Added in loading bar for visual bliss
    print(f'Scanning {url}...')
    for i in tqdm(range(10)):
        time.sleep(3)

    results_request = requests.get(api_results)
    results_response = results_request.json()

    try:
        if results_response['message'] == 'notdone':
            time.sleep(20)
            results_request = requests.get(api_results)
            results_response = results_request.json()

    except KeyError:
        pass

    if '404' == str(results_request.status_code):
        time.sleep(10)
        results_request = requests.get(api_results)
        results_response = results_request.json()

    try:
        if results_response['data']['requests'][0]['response']['failed']['errorText'] == "net::ERR_NAME_NOT_RESOLVED":
            print('We could not scan this website! Erorr name could not be resolved. ')

    except KeyError:
        screenshot = results_response['task']['screenshotURL']
        effective_url = results_response['data']['requests'][0]['request']['documentURL']
        links = results_response['data']['links']
        malicious = results_response['stats']['malicious']
        asn = results_response['meta']['processors']['asn']['data']

        if malicious > 0:
            threat = results_response['meta']['processors']['gsb']['data']['matches']
            print('\n*****WARNING SEE THREAT BELOW*****')

            for i in threat:
                threat_type = i['threatType']
                threat_url = i['threat']['url']

            print(f'ThreatType:       {threat_type}')
            print(f'ThreatURL:        {threat_url}')
            print(f'\n*****Results*****')
            print('IP Address - AS(Autonomous System) - Organization')

        else:
            print(f'\n*****Results*****')
            print('IP Address - AS(Autonomous System) - Organization')

        for line in asn:
            org_name = line['name']
            country = line['country']
            asn_value = line['asn']
            ip = line['ip']
            print(ip, '-',f'AS{asn_value}', '-',f'({org_name})')

        # print(f'Org:              {asn_name}')
        print(f'\nEffectiveURL:     {effective_url}')
        print(f'Screenshot:       {screenshot}\n')

        for line in links:
            sorted_links = line['href']
            print(f'Links:            {sorted_links}')

def main():
    url_scan(args.url)

if __name__ == '__main__':
    main()
