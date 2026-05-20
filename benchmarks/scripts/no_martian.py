from common import counterexamplesCount,MyTimer,MARTIANS,FULL_SNAPSHOT,ROUTERS
from api.startup import runIsolationVerificationQuestion,create
from api.whirlpool import LocationPropertyPair, IsolationQuery, Clause, negate, outgoingEdgesFrom

networkName = "NoMartians_Check_net"
snapshotName = "NoMartians_Check_snapshot"

def no_martians_at(l):
    return LocationPropertyPair(location=l,property=[Clause(prefixes=list(map(negate,MARTIANS)))])

def noMartian(bf):
    target = no_martians_at(ROUTERS[0])
    enforced = list(map(no_martians_at,ROUTERS[1:]))
    internal_assumptions = list(map(no_martians_at,[outgoingEdgesFrom("64.57.28.251"), outgoingEdgesFrom("64.57.28.252")]))
    query = IsolationQuery(target=target,assumptions=enforced + internal_assumptions)
    t = MyTimer()
    df = runIsolationVerificationQuestion(bf,query)
    elapsed = t.stop()
    return (counterexamplesCount(df),elapsed)

def run(batch):
    runtime = 0
    checksum = True
    bf = create(networkName,snapshotName,FULL_SNAPSHOT)
    for i in range(batch):
        (cex,time) = noMartian(bf)
        runtime += time
        checksum = checksum and (cex == 0)
    avg_runtime = round(runtime / batch,3)
    return (avg_runtime,checksum)