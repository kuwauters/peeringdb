import requests
import argparse
import yaml
import os
import pprint


def check_prompt():
    '''
        Validate that we are receiving all necessary parameters from the prompt
            - obj: 
                - ix: get all IX's
                - peer: get all peer info 
    '''

    parser = argparse.ArgumentParser(description = 'interface on top of peeringdb for programmatic abstraction')
    parser.add_argument("--obj", metavar='objects that you want to query on top of peeringdb', help='\"ixpfx\" for all ip\'s of exchange info -- \"peer\" for peer info', required=True)
    settings = parser.parse_args()

    return settings.obj

def datacollection (api_url):
    '''
        execute get for the given url
    '''
    return requests.get(api_url)


def main():
    cfg = yaml.load(open('conf/config.yaml'), Loader=yaml.SafeLoader)

    #What do you want to know cmd parameters
    search_obj = check_prompt()

    if search_obj == 'ixpfx':
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
            print('something went wrong')
    else:
        print('search object not defined')


if __name__ == '__main__':
    main()