# ip_transit
 Retrieve data from peeringdb using the api without credentials

## Options
- obj: defines the data that you want to retrieve
    - ixpfx: retrieve the prefix ranges that are used on all IXs
    - lclix `id`: retireve the peers that are only present in the same region as this ix. The `ìd` is the ix id that can be retrieved by searching the ix itself
    - l: defines the logging that needs to be used for peeringdb. Credentials are mainly needed for retrieving contact details
    - p: defines the password that needs to be used for peeringdb. Credentials are mainly needd for retrieving contact details


## Output example

### retrieving all the ip's from the IXs
`python peeringdb.py --obj ixpfx`

2001:504:0:2::/64
206.126.236.0/22
208.115.136.0/23
2001:504:0:4::/64
206.223.118.0/232001:504:0:5::/64

### retrieving local peers on a specific IX
`python peeringdb.py --lclix 2381 -l JohnDoe -p changmenow`

name;asn;ip;ip6;as_set;max_pfx;max_pfx6;policy;technical;noc;presence_name;region_continent
Avanti Communications South Africa;328306;196.60.58.12 // 196.60.58.13;2001:43f8:11f0::5:272:1 // 2001:43f8:11f0::5:272:2;AS-328306;0;0;Open;peering@avantiplc.com;;WAF-IX, Lagos: Main // WAF-IX, Lagos: Main;Africa;
Avanti Communications South Africa;328306;196.60.58.12 // 196.60.58.13;2001:43f8:11f0::5:272:1 // 2001:43f8:11f0::5:272:2;AS-328306;0;0;Open;peering@avantiplc.com;;WAF-IX, Lagos: Main // WAF-IX, Lagos: Main;Africa;
Juniper Solutions;37398;198.60.58.15;2001:43f8:11f0::9216:1;;0;0;Open;;;WAF-IX, Lagos: Main;Africa;

`python peeringdb.py --lclix 2381`

name;asn;ip;ip6;as_set;max_pfx;max_pfx6;policy;technical;noc;presence_name;region_continent
Avanti Communications South Africa;328306;196.60.58.12 // 196.60.58.13;2001:43f8:11f0::5:272:1 // 2001:43f8:11f0::5:272:2;AS-328306;0;0;Open;;;WAF-IX, Lagos: Main // WAF-IX, Lagos: Main;Africa;
Avanti Communications South Africa;328306;196.60.58.12 // 196.60.58.13;2001:43f8:11f0::5:272:1 // 2001:43f8:11f0::5:272:2;AS-328306;0;0;Open;;;WAF-IX, Lagos: Main // WAF-IX, Lagos: Main;Africa;
Juniper Solutions;37398;198.60.58.15;2001:43f8:11f0::9216:1;;0;0;Open;;;WAF-IX, Lagos: Main;Africa;

