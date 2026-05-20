from api.startup import runReachabilityVerificationQuestion
from api.whirlpool import trueAtLocation, LocationPropertyPair, ReachabilityQuery, Clause
from common import MyTimer

networkName = "Internet2_reachability_net"
snapshotName = "Internet2_reachability_snapshot"

def getGoodPath(df):
    for k in df.itertuples():
        if k.Result_Label == "Good Path":
            v = k.Result
            return v.split("Bgpv4Route")[0].strip()
    return None

def hasInterference(df):
    for k in df.itertuples():
        if k.Result_Label.startswith("Potential Interference"):
            return True
    return False

def ingressNodeReaches(bf,target,ingress,dp=True):
    query = ReachabilityQuery(prefix="100.100.0.0/16",target=trueAtLocation(target),ingress=[ingress],compute_dp=dp)
    t = MyTimer()
    df = runReachabilityVerificationQuestion(bf,query)
    elapsed = t.stop()
    return (getGoodPath(df),hasInterference(df),elapsed)

def ingressNodeReachesWithInterference(bf,target,ingress,dp=True):
    tgt = LocationPropertyPair(location=target,property=[Clause(communities=["1:1"])])
    ingressAssumption = LocationPropertyPair(location=ingress,property=[Clause(communities=["1:1"])])
    query = ReachabilityQuery(prefix="100.100.0.0/16",target=tgt,assumptions=[ingressAssumption],ingress=[ingress],compute_dp=dp)
    t = MyTimer()
    df = runReachabilityVerificationQuestion(bf,query)
    elapsed = t.stop()
    return (getGoodPath(df),hasInterference(df),elapsed)

def noGoodPath(bf,target,dp=True):
    tgt = LocationPropertyPair(location=target,property=[Clause(communities=["1:1"])])
    query = ReachabilityQuery(prefix="100.100.0.0/16",target=tgt,compute_dp=dp)
    t = MyTimer()
    df = runReachabilityVerificationQuestion(bf,query)
    elapsed = t.stop()
    return (getGoodPath(df),hasInterference(df),elapsed)