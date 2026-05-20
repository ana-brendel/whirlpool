from api.startup import runIsolationVerificationQuestion,runWhirlpoolQuery,create
from api.whirlpool import negate, trueAtLocation, outgoingEdgesFrom, incomingEdgesTo
from api.whirlpool import LocationPropertyPair, IsolationQuery, Clause, OUTGOING
from common import counterexamplesCount,FULL_SNAPSHOT,INDIVIDUAL_SNAPS,BTE_Community,MyTimer

networkName = "BlockToExternal_Check_net"
snapshotName = "BlockToExternal_Check_snapshot"

def isoViolations(df):
    for k in df.itertuples():
        if k.Location_Relevance == "Violation Note":
            return k.Network_Locations
    return ""

def blockToExternal(bf,dp=True):
    target = LocationPropertyPair(location=OUTGOING,property=[Clause(communities=[negate(BTE_Community)])])
    query = IsolationQuery(target=target,compute_dp=dp)
    t = MyTimer()
    df = runIsolationVerificationQuestion(bf,query)
    elapsed = t.stop()
    return (counterexamplesCount(df),elapsed)

def blockToExternalWithIsolation(bf,dp=True):
    target = LocationPropertyPair(location=OUTGOING,property=[Clause(communities=[negate(BTE_Community)])])
    query = IsolationQuery(target=target,isolate_violations=True,compute_dp=dp)
    t = MyTimer()
    df = runIsolationVerificationQuestion(bf,query)
    elapsed = t.stop()
    return (isoViolations(df),elapsed)
    
def blockToExternalCoverViolations(bf,violations,dp=True):
    target = LocationPropertyPair(location=OUTGOING,property=[Clause(communities=[negate(BTE_Community)])])
    query = IsolationQuery(target=target,assumptions=list(map(trueAtLocation,violations)),compute_dp=dp)
    t = MyTimer()
    df = runIsolationVerificationQuestion(bf,query)
    elapsed = t.stop()
    return (counterexamplesCount(df),elapsed)

def run(batch):
    runtime_violations = 0
    runtime_no_violations = 0
    avg_iso_violation = 0
    violation_checksum = True
    no_violation_checksum = True
    iso_checksum = True
    violations = ["chic -> 207.75.164.233", "chic -> 128.223.51.108", "chic -> 128.223.51.102", 
    "chic -> 207.75.164.213", "losa -> 203.181.248.35", "newy-re0 -> 10.11.1.17"]
    bf = create(networkName,snapshotName,FULL_SNAPSHOT)
    for i in range(batch):
        (cex,time) = blockToExternal(bf)    
        runtime_violations += time
        violation_checksum = violation_checksum and (cex == 84)

        (cex,time) = blockToExternalCoverViolations(bf,violations)
        runtime_no_violations += time
        no_violation_checksum = no_violation_checksum and (cex == 0)

        (cex,time) = blockToExternalWithIsolation(bf)
        exp_violations = ", ".join([
            "(chic) 64.57.28.241 -> 207.75.164.213",
            "(chic) 64.57.28.241 -> 207.75.164.233",
            "(newy-re0) 64.57.28.242 -> 10.11.1.17",
            "(chic) 64.57.28.241 -> 128.223.51.108",
            "(losa) 64.57.28.248 -> 203.181.248.35",
            "(chic) 64.57.28.241 -> 128.223.51.102"])
        avg_iso_violation += time
        iso_checksum = iso_checksum and (cex == f"[ALL OTHER TARGETS INDEPENDENTLY VERIFY] INDEPENDENT VIOLATIONS AT: {exp_violations}")

    avg_violations = round(runtime_violations / batch,3)
    avg_no_violations = round(runtime_no_violations / batch,3)
    avg_iso_violation = round(avg_iso_violation / batch,3)
    return (avg_violations,violation_checksum,avg_no_violations,no_violation_checksum,avg_iso_violation,iso_checksum)

def run_no_strip(directory,node):
    path = f"{INDIVIDUAL_SNAPS}/{directory}"
    target = LocationPropertyPair(location=outgoingEdgesFrom(node),property=[Clause(communities=[BTE_Community])])
    assumptions = [LocationPropertyPair(location=incomingEdgesTo(node),property=[Clause(communities=[BTE_Community])])]
    query = IsolationQuery(target=target,assumptions=assumptions)
    t = MyTimer()
    df = runWhirlpoolQuery(networkName,snapshotName,path,query)
    elapsed = t.stop()

    noStrip = True
    for k in df.itertuples():
        if k.Counterexample.strip() != "":
            noStrip = False
            break
    return (elapsed,noStrip)

def run_no_strip_batched(batch):
    routers = [("atla","atla-re0"),("chic","chic"),("clev","clev-re0"),("hous","hous"),("kans","kans-re0"),
           ("losa","losa"),("newy32aoa","newy-re0"),("salt","salt-re0"),("seat","seat-re0"),("wash","wash")]
    overall = 0
    check = True
    for (directory,node) in routers:
        total = 0
        successes = True
        batch = 5
        for i in range(batch):
            (time,success) = run_no_strip(directory,node)
            successes = successes and success
            total += time
        avg = round(total / batch,3)
        overall += avg
        check = check and successes
    return (overall,check)
