import random
import time

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

with open("server.log","w") as f:
    for i in range(20):
        message=random.choice(message_list)
        f.write(message+"\n")
        time.sleep(0.5)
print("Log file created successfully!")

error_counts={}
with open("server.log","r") as f, open("security_alert.txt","w") as output:
    for i in f:
        message=i.strip()

        if "ERROR" in message:
            error_counts["ERROR"]=error_counts.get("ERROR",0)+1
        if "CRITICAL" in message:
            error_counts["CRITICAL"]=error_counts.get("CRITICAL",0)+1
            output.write(message[9:]+"\n")
        if "FAILED" in message:
            error_counts["FAILED"]=error_counts.get("FAILED",0)+1
        
print("summary")
for i,j in error_counts.items():
    print(f'{i}:{j}')
    print()