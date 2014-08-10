import json
import requests

def getem(key):
    with open('results.json', 'w') as fout:
        page = 1
        total = 0
        while True:
            r =
            requests.get('http://beta.content.guardianapis.com/search?section=film&api-key=%s&page-size=50&page=%i'
                         % (page, key))
            js = r.json()
            fout.write('\n'.join(res['webTitle'].encode('utf-8', 'ignore')
                                 for res in js['response']['results']))
            page += 1
            if page > js['response']['pages']:
                break
            total += js['response']['pageSize'] * page
            print "DONE: %i" % total

if __name__ == '__main__':
    getem(sys.argv[0])


