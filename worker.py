import uuid
import sys
import json
import time
import datetime
import requests
import os
from sfsqr import generate
import dotenv

max_attempts = 5

def main():

    dotenv.load_dotenv()

    os.system('lpadmin -d Brother_QL-700')

    env=None
    
    if 'prod' in sys.argv:
        env = 'prod'
    if 'dev' in sys.argv:
        env = 'dev'
        
    if not env:
        print('use prod or dev env')
        return

    id_location = uuid.UUID(os.getenv('id_location'))

    if env=='prod':
        url = f"https://app.sfscon.it/api/users/should-i-print/{id_location}"
        
    if env=='dev':
        url = f"https://opencon.dev.digitalcube.dev/api/users/should-i-print/{id_location}"



    status = f'{env} waiting-for-print-job'
    npi=0
    while True:
        timestamp = str(datetime.datetime.now())[:19]
        
        try:
            response = requests.request("GET", url)
        except Exception as e:
            print(f"{env} ERR 1",e)
            time.sleep(10)
            continue

        try:
                
            if response.status_code != 200:
                status = 'opencon-service-not-reachable'
                print(env, timestamp, status)
                time.sleep(5)
    
    #        print(response.text)
    
            r = json.loads(response.text)        
    
            status = r['status']
            if status == 'nothing-to-print':
                if npi % 100 == 0:
                    print(env, timestamp, status, 'on',id_location)
                time.sleep(0.2)
                npi += 1
        
                continue
    
            status='printed'
                
            print(env, timestamp, '\n', json.dumps(r, indent=1))
    
            cburl = r['callback']['url']
    
            fname = generate(r)
            
            cmd = f'/usr/bin/lpr {fname}'
#            cmd = '/usr/bin/lpr res.png'
    
            print(env, 'cmd',cmd)
            os.system(cmd)
    
            
            for attempt in range(0,max_attempts+1):
                time.sleep(1)
                r = os.system(f'/usr/bin/lpstat > /tmp/lps')
                with open ('/tmp/lps','rt') as f:
                    c = f.read().strip()
                    c = c.split('\n')
                    print(env, len(c),c,'\n','-'*100)
                    if c==['']:
                        break
    
            print("attempt",attempt)
    
            os.system('/usr/bin/lprm -')
                        
            if attempt >= max_attempts:
                status = 'error'
    
            try:    
                cb = requests.request("PUT", cburl, data=json.dumps({'status':status}))
            except Exception as e:
                print(env, "ERR 2",e)
                time.sleep(10)
                continue
    
    
            print(env, cb.status_code, cb.text)
        
        except Exception as e:
            print(env, "R",e)
                

if __name__=='__main__':

    main()