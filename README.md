# ip_transit
 Retrieve data from peeringdb using the api without credentials

## Options
- obj: defines the data that you want to retrieve
    - ixpfx: retrieve the prefix ranges that are used on all IXs
    - lclix `id`: retireve the peers that are only present in the same region as this ix. The `ìd` is the ix id that can be retrieved by searching the ix itself


## Output example

id961407@dl0005 peeringdb]$ python peeringdb.py --lclix 2381

Avanti Communications South Africa;328306;[u'Africa'];[u'WAF-IX, Lagos: Main', u'WAF-IX, Lagos: Main']
Avanti Communications South Africa;328306;[u'Africa'];[u'WAF-IX, Lagos: Main', u'WAF-IX, Lagos: Main']
Juniper Solutions;37398;[u'Africa'];[u'WAF-IX, Lagos: Main']
