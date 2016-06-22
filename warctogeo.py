import urllib
import re
import json
from urlparse import urlparse
import requests

with open('perma-landing.warc', 'r') as myfile:
    data=myfile.read().replace('\n', '')

unquoted = urllib.unquote(data)
urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', unquoted)

#with open('urls.json', 'w') as outfile:
#    json.dump(urls, outfile)


hosts = []

for url in urls:
    hosts.append(urlparse(url).netloc)


unique_hosts = list(set(hosts))

#print len(urls)
#print len(hosts)
print len(unique_hosts)
print unique_hosts

outp = []

for host in unique_hosts:
    request_url = 'http://freegeoip.net/json/%s' % host
    r = requests.get(request_url)
    print r.status_code
    print host
    if r.status_code == 200:
        d = json.loads(r.text)
        j = {'lat': d['latitude'], 'lng': d['longitude'], 'name': host}
        outp.append(j)

print json.dumps(outp)