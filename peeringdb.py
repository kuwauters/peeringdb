import requests
import argparse
import yaml
import os
import pprint
import tqdm
from concurrent import futures
from getpass import getpass

class ix():
    def __init__(self):
        self.id = ''
        self.region_continent = ''
        self.ix = ''
        self.country = ''
        self.techmail = ''
        self.lanset = []
    
    
    def update_ix (self, input):
        self.region_continent = input['data'][0]['region_continent']
        self.ix = input['data'][0]['name']
        self.country = input['data'][0]['country']
        self.techmail = input['data'][0]['tech_email']
        self.id = input['data'][0]['id']

        for ixlan in input['data'][0]['ixlan_set']:
            (self.lanset).append(ixlan['id'])

class peer():
    def __init__(self, input):
        self.ix = input
        self.name = ''
        self.id = ''
        self.asn = ''
        self.as_set = ''
        self.max_pfx = ''
        self.max_pfx6 = ''
        self.policy = ''
        self.technical = ''
        self.noc = ''
        self.policy = ''
        self.presence = []
        self.presence_name = []
        self.region_continent = []
        self.ip = []
        self.ip6 = []
    
    def update_peer (self, input):
        self.name = input['name']
        self.id = input['id']
        self.asn = input['asn']
        self.as_set = input['irr_as_set']
        self.max_pfx = input['info_prefixes4']
        self.max_pfx6 = input['info_prefixes6']
        self.policy = input['policy_general']

    def update_presence (self, input):
        for netixlan in input['data'][0]['netixlan_set']:
            (self.presence).append(netixlan['ix_id'])
            (self.presence_name).append(netixlan['name'])
            (self.ip).append(netixlan['ipaddr4'])
            (self.ip6).append(netixlan['ipaddr6'])
    
    def update_region (self, input):
        if input['data'][0]['region_continent'] not in self.region_continent:
            (self.region_continent).append(input['data'][0]['region_continent'])
    
    def update_contact(self, input,contact_attr):
        '''
            when credentials are provided the contact details can be retrieved from peeringdb
        '''
        for contact in input['data'][0]['poc_set']:
            if contact['role'].lower() in contact_attr:
                setattr(self, contact['role'].lower(), contact['email'])



def check_prompt():
    '''
        Validate that we are receiving all necessary parameters from the prompt
            - obj: 
                - ix: get all IX's
                - peer: get all peer info 
    '''

    parser = argparse.ArgumentParser(description = 'interface on top of peeringdb for programmatic abstraction')
    parser.add_argument("--obj", metavar='objects that you want to query on top of peeringdb', help='\"ixpfx\" for all ip\'s of exchange info -- \"peer\" for peer info', required=False)
    parser.add_argument("--lclix", type = int, metavar='the ix on which you are looking for local peers', help=' the ix id from peeringdb', required=False)
    parser.add_argument("-l", type = str, metavar = 'the login to be used when obtaining confidential info from peeringdb (mail addresses)', required=False)
    parser.add_argument('-p', type = str, metavar = 'the password to be use when obtaining confidential info from peeringdb (mail addresses)', required=False)
    settings = parser.parse_args()

    return settings

def datacollection (api_url, authentication,cred):
    '''
        execute get for the given url
    '''
    if authentication:
        return (requests.get(api_url, auth=(cred[0],cred[1]))).json()
    else:
        return (requests.get(api_url)).json()

def analyse_peer(peers,attr_lst):
    print('...analysing..')
    for el in tqdm.tqdm(peers, total=len(peers)):
        if len(el.region_continent) == 1:
            for attr in attr_lst:
                if isinstance(getattr(el,attr),list):
                    try:
                        print(' // '.join(getattr(el, attr)), end=';')                  
                    except Exception as e:
                        print(e)
                else:
                    print('NA')
            print()
                    

def create_output():
    '''
        Create readable output for the user with only the limited data
    '''


def main():
    peer_lst = []
    cred = ('', '')

    cfg = yaml.load(open('conf/config.yaml'), Loader=yaml.SafeLoader)

    #What do you want to know cmd parameters
    search_obj = check_prompt()
    
    if search_obj.obj and search_obj.obj == 'ixpfx':
        #perform URL get - retrieve data from peeringdb
        ntw_rsp = datacollection('{}{}'.format(cfg['base_url'], cfg['ix']),False,cred)
        
        try:
            #retrieve specific network data
            for client in ntw_rsp['data']:
                ntw_client_rsp = datacollection('{}{}lan/{}'.format(cfg['base_url'], cfg['ix'], client['id'] ), False,cred)

                for client_ntw in ntw_client_rsp['data']:
                    for ixpfx in client_ntw['ixpfx_set']:
                        print(ixpfx['prefix'])
        except Exception as e:
            print('something went wrong in ixpfx \n {}'.format(e))
    elif search_obj.lclix:
        
        ntw_rsp = datacollection('{}{}/{}'.format(cfg['base_url'], cfg['ix'],search_obj.lclix),False,cred)
        
        try:
            print('.looking up IX LANs')
            ix_obj = ix()
            ix_obj.update_ix(ntw_rsp)
            for ixlan in ix_obj.lanset:
                ixlan_rsp = datacollection('{}{}/{}'.format(cfg['base_url'], cfg['ixlan'],ixlan),False,cred)
                
                for peer_el in ixlan_rsp['data'][0]['net_set']:
                    peer_obj = peer(ix_obj)
                    peer_obj.update_peer(peer_el)
                    peer_lst.append(peer_obj)
                
        except Exception as e:
            print('something went wrong in lclix\n {}'.format(e))

            print('..Looking up peers')

        for peer_el in tqdm.tqdm(peer_lst, total=len(peer_lst)):    
            if search_obj.l and search_obj.p:
                cred = (search_obj.l,search_obj.p)
                presence_rsp = datacollection('{}{}/{}'.format(cfg['base_url'], cfg['peer'],peer_el.id),True,cred)
                peer_el.update_contact(presence_rsp,cfg['contact'])

            else:
                presence_rsp = datacollection('{}{}/{}'.format(cfg['base_url'], cfg['peer'],peer_el.id),False,cred)

            peer_el.update_presence(presence_rsp)

            print('...looking up ix presence / regions')
            with futures.ThreadPoolExecutor(40) as executor:
                rsp_lst = []
                for ix_el in tqdm.tqdm(peer_el.presence, total = len(peer_el.presence)):
                            
                    ntw_rsp = executor.submit(datacollection,('{}{}/{}'.format(cfg['base_url'], cfg['ix'],ix_el)),False,cred)
                    rsp_lst.append(ntw_rsp)
                    
                for el in rsp_lst:
                    peer_el.update_region(el.result())

        analyse_peer(peer_lst, cfg['attr'])

    else:
        print('search object not defined, try peeringdb.py -h')


    

if __name__ == '__main__':
    main()