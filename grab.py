import sys
import requests


def getem(key):
    url = ('http://beta.content.guardianapis.com/search?'
           'section=film&api-key=%s&page-size=50&page=%i')
    with open('results.json', 'w') as fout:
        page = 1
        total = 0
        while True:
            r = requests.get(
                url % (key, page))
            js = r.json()
            fout.write('\n'.join(res['webTitle'].encode('utf-8', 'ignore')
                                 for res in js['response']['results']))
            page += 1
            if page > js['response']['pages']:
                break
            total += js['response']['pageSize']
            print "DONE: %i" % total

if __name__ == '__main__':
    getem(sys.argv[0])
