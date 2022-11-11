import pdb
import uuid
import sys
import json
import time
import datetime
import requests
import os
from sfsqr import generate, generate2
import dotenv
import httpx
import asyncio
import logging as log

log.basicConfig(filename='print.log', level=log.INFO)

from telegram import send_message

max_attempts = 25

server = None

if 'prod' in sys.argv:
    env = 'prod'
    server = 'https://m.opencon.dev'
if 'dev' in sys.argv:
    env = 'dev'
    server = 'https://stage.opencon.dev'


async def get_tenant():
    id_tenant = None
    while not id_tenant:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f'{server}/api/v3/tenants/code/OPENCON')
                id_tenant = json.loads(r.text)['id']
        except:
            time.sleep(2)
    return id_tenant
        
async def get_conference():
    id_conference = None
    while not id_conference:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f'{server}/api/v3/conferences/acronym/sfscon-2022')
                id_conference = json.loads(r.text)['id']
        except:
            time.sleep(2)
    return id_conference
    
async def get_token(id_tenant, username, password):
    token = None
    while not token:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(f'{server}/api/v3/tenants/{id_tenant}/sessions',content=json.dumps({'username': username, 'password': password}))
                token = json.loads(r.text)['token']
        except:
            time.sleep(2)
    return token

async def get_id_location_by_name(token, id_conference, location_name):
    _location_name = None
    while not _location_name:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f'{server}/api/v3/conferences/{id_conference}/entrances', headers={'Authorization': f'Bearer {token}'})
                r = json.loads(r.text)
                if location_name not in r:
                    log.critical("location name not exists {location_name}")
                    sys.exit()
                    
                _location_name = r[location_name]
        except:
            time.sleep(2)
    return _location_name
        
        

async def main():

    dotenv.load_dotenv()
    
    log.info('printing system started')

    os.system('lpadmin -d Brother_QL-700')
#    os.system('lpadmin -d QL-700')

    global env
    
    if not env:
        print('use prod or dev env')
        return

    id_tenant = await get_tenant()
    id_conference = await get_conference()

    token = await get_token(id_tenant,'system','123')
    
    log.info(f'using tenant {id_tenant}')
    log.info(f'using conference {id_conference}')
    log.info(f'token {token}')
    
    location_name = os.getenv('location')
    log.info(f'location {location_name}')
    
    id_location = await get_id_location_by_name(token, id_conference, location_name)
    log.info(f'id_location {id_location}')
    
    url = f'{server}/api/v3/conferences/locations/{id_location}/should-i-print/'
    
    status = f'{env} waiting-for-print-job'
    npi=0
    while True:

#        time.sleep(30)
        
        response = None
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers={'Authorization': f'Bearer {token}'})
                
        except Exception as e:
            log.critical(f'.error {e} sleeping 1 sec')
            time.sleep(1)
            continue
        
        try:
            
            if response.status_code != 200:
                status = 'opencon-service-not-reachable'
                log.critical(f'error response.status_code != 200; {response.status_code} sleeping 10')
                time.sleep(1)
                continue
    
            response = json.loads(response.text)
            
            log.info(f"RESPONSE {response}")        

            if 'print' not in response or not response['print']:
                log.info('nothing-to-print')
                time.sleep(0.2)
                continue
                    
            status='printed'

            if 'title' not in response['print']:
                response['print']['title']='SFS 2022'    
            
            display_name = response['print']['first_name']
            
#            s = display_name.split(' ')
#            first_name=s[0]
            last_name=response['print']['last_name']
            first_name=response['print']['first_name']
            
#            last_name=' '.join(s[1:])
#            response['print']['first_name'] = first_name
#            response['print']['last_name'] = last_name
            

            fname = generate2(response['print'])
            
            cmd = f'/usr/bin/lpr {fname}'
#            cmd = '/usr/bin/lpr res.png'
    
            log.debug(f'cmd {cmd}')
            os.system(cmd)
            
            
            for attempt in range(0,max_attempts+1):
                time.sleep(0.45)
                r = os.system(f'/usr/bin/lpstat > /tmp/lps')
                with open ('/tmp/lps','rt') as f:
                    c = f.read().strip()
                    c = c.split('\n')
                    
                    #print(env, len(c),c,'\n','-'*100)
                    if c==['']:
                        break
    
            #print("attempt",attempt)
    
            os.system('/usr/bin/lprm -')
            
            p_status = {"printed": True}            
            if attempt >= max_attempts:
                status = 'error'
                p_status = {"printed":False}
                log.critical('not printed after {} attempts'.format(attempt))
            else:
                log.info('successfully printed {}'.format(response['print']))
                
                send_message(f'successfully printed {response}')            
            
            _url = f'{server}/api/v3/conferences/prints/{response["print"]["id_print"]}/status'
            
            async with httpx.AsyncClient() as client:
                log.info(f"Setting print job status to {p_status}")
                _response = await client.patch(_url, headers={'Authorization': f'Bearer {token}'}, content=json.dumps(p_status))
                log.info(f"response {_response.status_code} {_response.text}")
                

    
#            print(env, cb.status_code, cb.text)
        
        except Exception as e:
            print(env, "R",e)
                

if __name__=='__main__':

    asyncio.run(main())
