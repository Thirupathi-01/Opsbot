import random
import time
import re
from datetime import datetime

message_list=[
    "INFO Login succeeded",
    "INFO User added successfully",
    "INFO Access token generated successfully",
    "ERROR 404 Page not found",
    "ERROR 403 Access denied for this account",
    "ERROR 400 Exceeds rate limiting",
    "CRITICAL Application not loading at peak times",
    "CRITICAL Moltbot,Clawdbot are getting the sensitive information of users",
    "FAILED To connect to mysql server",
    "FAILED Not having correct permissions for the user for retriving the data"
]

file_pattern=re.compile(r"^(ERROR|CRITICAL)")
with open("server.log","w") as f:
    for i in range(20):
        message=random.choice(message_list)
        f.write(message+"\n")
        key=file_pattern.match(message)
        if key:
            n=random.randint(1,5)
            for j in range(n):
                f.write(f"  Line{j+1}:stacktrace {key.group()} explanation"+"\n")
        
        time.sleep(0.5)
print("Log file created successfully!")

error_counts={}
curr_l=[]
critical_set=set()
start_pattern=re.compile(r"^(ERROR|FAILED|CRITICAL)\b")
pattern=re.compile(r"(ERROR|FAILED|CRITICAL)")

def process(l):
    full_single_log="".join(curr_l)
    key=pattern.search(full_single_log)
    if key:
        error_type=key.group()
        error_counts[error_type]=error_counts.get(error_type,0)+1
        if error_type=="CRITICAL":
            msg=l[0]
            critical_set.add(msg)

with open("server.log","r") as f:
    for msg in f:
        message=msg.strip()
        if start_pattern.search(message) and curr_l:
            process(curr_l)
            curr_l=[]
        curr_l.append(message)

if curr_l:
    process(curr_l) 
    
date=datetime.now().strftime("%d-%m-%Y")
with open(f"security_report_{date}.txt","w") as output:
    for msg in critical_set:
        output.write(msg+"\n")
        
print("Log summary:")
for i,j in error_counts.items():
    print(f'{i}:{j}')