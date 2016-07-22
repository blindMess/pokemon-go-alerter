import json
import requests
import time


COMMON = ['Pidgey', 'Weedle', 'Caterpie', 'Zubat', 'Rattata']

class Notifier(object):

    def __init__(self):
	self.services = json.load(open('config.json')).get('services')
	self.filterCommon = json.load(open('config.json')).get('filterCommon')

        if self.services is None:
            print("[!] Warning: No services configured!")
	if self.filterCommon is None:
	    print("[!] Warning: Parameter to Filter Common Pokemon is not set!")

    def notify(self, results):
        for i in range(len(results)):
            pokemon = results[i].split(' ')[0]

            if pokemon not in COMMON:
                results[i] = ":tada: " + results[i]
            # Don't notify on COMMON pokemon
	    if pokemon in COMMON and self.filterCommon == 1:
		results[i] = None
	
	results = filter(None, results)
        results = {'text': "Pokemon scan results:\n\n %s" % ('\n'.join(results))}

	for service in self.services:
            if service.get('webhook'):
                r = requests.post(service.get('webhook'), data=json.dumps(results))
                service['last_message'] = time.time()
            else:
                print 'Service not yet supported.'
