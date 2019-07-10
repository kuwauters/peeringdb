import requests
import argparse
import yaml
import os
import pprint


class ix():
    def __init__(self):
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

        for ixlan in input['data'][0]['ixlan_set']:
            (self.lanset).append(ixlan['id'])
        




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
    settings = parser.parse_args()

    return settings

def datacollection (api_url):
    '''
        execute get for the given url
    '''
    return requests.get(api_url)

def create_output():
    '''
        Create readable output for the user with only the limited data
    '''


def main():
    cfg = yaml.load(open('conf/config.yaml'), Loader=yaml.SafeLoader)

    #What do you want to know cmd parameters
    search_obj = check_prompt()
    
    if search_obj.obj and search_obj.obj == 'ixpfx':
        #perform URL get - retrieve data from peeringdb
        ntw_rsp = datacollection('{}{}'.format(cfg['base_url'], cfg['ix']))
        
        try:
            #retrieve specific network data
            for client in ntw_rsp.json()['data']:
                ntw_client_rsp = datacollection('{}{}lan/{}'.format(cfg['base_url'], cfg['ix'], client['id'] ))

                for client_ntw in ntw_client_rsp.json()['data']:
                    for ixpfx in client_ntw['ixpfx_set']:
                        print(ixpfx['prefix'])
        except:
            print('something went wrong in ixpfx')
    elif search_obj.lclix:
        
        ntw_rsp = datacollection('{}{}/{}'.format(cfg['base_url'], cfg['ix'],search_obj.lclix))
        
        try:
            ix_obj = ix()
            ix_obj.update_ix(ntw_rsp.json())
            print (ix_obj.lanset)
            
        except:
            print('something went wrong in lclix')

    else:
        print('search object not defined, try peeringdb.py -h')


if __name__ == '__main__':
    main()