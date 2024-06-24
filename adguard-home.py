import base64 
import requests
import re

print("script start")
output_file = "upstream_dns.txt"
gfwlist_url = 'https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt'
extra_domain = [
    "google.com.hk",
    "google.com.jp",
]
china_dns = "https://dns.alidns.com/dns-query"
global_dns = "https://1.1.1.1/dns-query"

response = requests.get(gfwlist_url)
print("download gfwlist successful")
gfwlist = base64.b64decode(response.content).decode('utf-8')

comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*' 
vaild_domain_pattern = r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,10}$'

domain_list = extra_domain
lines = gfwlist.splitlines()
for line in lines:
    if(not re.findall(comment_pattern, line)):
        domain = re.findall(domain_pattern, line)
        if(domain):
            if(domain not in domain_list):
                if(re.match(vaild_domain_pattern, domain[0])):
                   domain_list.append(domain[0])
print("convert gfwlist successful")


fs =  open(output_file, 'w')
for domain in domain_list:
    fs.write(f'[/{domain}/]{global_dns}\n')
fs.write(f'{china_dns}\n')
fs.close()
print("generate upstream dns file successful")
print("script finished")