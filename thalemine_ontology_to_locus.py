import json
import requests
import re
import thalemine_common

def search(arg):

    # Assumes client is passing in a valid GO text description
    # This is a bad assumption - this code is illustrative of 
    # how to package an Intermine template as a simpler-to-use API
    terms = arg['terms']
    
    # Make the request
    payload = {'name': 'ontologyTermSyn_genes', 'constraint1': 'Gene.ontologyAnnotations.ontologyTerm.synonyms.name', 'op1': 'CONTAINS', 'format': 'json', 'value1': terms}
    svc_url = thalemine_common.template_url()
    r = requests.get(thalemine_common.template_url(), params=payload)
    p = re.compile('AT[1-5MC]G[0-9]{5,5}', re.IGNORECASE)
    
    # Iterate over the results
    for result in r.json()['results']:
    
        # I really don't like that we rely on array position to pull out results
        # so, I validate that we are are returning an AGI locus
        locus = result[0].upper()
        if p.search(locus):
			record = { 'class': 'locus_property',
						'locus': result[0].upper(),
						'properties': [ {'type': 'logical_text_match', 'value': terms },
										{'type': 'text_description', 'value': result[3] } ]
        }
        
        print json.dumps(record)
        print '---'
    
def list(arg):
    # We don't support a list context for this API
    pass
