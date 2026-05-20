import time,json

# BLOCK-TO-EXTERNAL Community 11537:888 - any edges leaving the network should NOT have the BTE community
BTE_Community = "11537:888"

MARTIANS = [ "0.0.0.0/0", "10.0.0.0/8", "127.0.0.0/8", "169.254.0.0/16", "172.16.0.0/12", "192.0.2.0/24", "192.88.99.1/32",
    "192.168.0.0/16", "198.18.0.0/15", "224.0.0.0/4", "240.0.0.0/4", "255.255.255.255/32" ]

FULL_SNAPSHOT = "../internet2/all"
INDIVIDUAL_SNAPS = "../internet2/individuals"

ROUTERS = ["atla-re0","chic","clev-re0","hous","kans-re0","losa","newy-re0","salt-re0","seat-re0","wash"]

class MyTimer:
    def __init__(self):
        self.start = time.time()
    
    def stop(self):
        end = time.time()
        return round(end - self.start,2)
    
def getJson(f):
    with open(f, 'r') as file:
        return json.load(file)
    
def counterexamplesCount(df) -> int:
    total = 0
    for k in df.itertuples():
        if k.Counterexample != "":
            total += 1
    return total

def counterexamples(df):
    df.drop(df[(df.Counterexample == "")].index, inplace=True)
    return df

def minutesFromSeconds(total):
    minutes = total // 60
    seconds = total - (minutes * 60)
    return (minutes,seconds)