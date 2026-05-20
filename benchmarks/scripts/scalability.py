# Common imports
from common import minutesFromSeconds

# Experiment specific imports
from api.startup import create
from block_to_external import blockToExternal,blockToExternalCoverViolations
from reachability import ingressNodeReachesWithInterference,ingressNodeReaches

def getViolationsForOffset(offset):
    violations = []
    for i in range(offset):
        violations += [f"chic_{i} -> 207.75.164.233"]
        violations += [f"chic_{i} -> 128.223.51.108"]
        violations += [f"chic_{i} -> 128.223.51.102"]
        violations += [f"chic_{i} -> 207.75.164.213"]
        violations += [f"losa_{i} -> 203.181.248.35"]
        violations += [f"newy-re0{i} -> 10.11.1.17"]
    return violations

def runSafetyScalabilityLayer(layer,batch):
    networkName = f"{layer}_layers_network"
    snapshotName = f"{layer}_layers_snapshot"
    snapshot = f"../scaling/{layer}_layers"
    bf = create(networkName,snapshotName,snapshot)
    runtime_violations = 0
    violation_checksum = True
    runtime_no_violations = 0
    no_violation_checksum = True
    for i in range(batch):
        (cex,time) = blockToExternal(bf,dp=False)
        print(f"... block to external runtime {time} (checksum {cex})")
        runtime_violations += time
        violation_checksum = violation_checksum and (cex == 84)
        (cex,time) = blockToExternalCoverViolations(bf,getViolationsForOffset(layer),dp=False)
        print(f"... block to external no violations runtime {time} (checksum {cex})")
        runtime_no_violations += time
        no_violation_checksum = no_violation_checksum and (cex == 0)
    avg_violations = round(runtime_violations / batch,3)
    avg_no_violations = round(runtime_no_violations / batch,3)
    return (avg_violations,violation_checksum,avg_no_violations,no_violation_checksum)

def runSafetyScalability(layers,batch):
    for layer in layers:
        print(f"Running for [Layer {layer}] [averaged over {batch} runs]")
        (t1,c1,t2,c2) = runSafetyScalabilityLayer(layer,batch)
        (minutes,seconds) = minutesFromSeconds(t1)
        print(f"- Avg Runtime (s) with Violation: {t1} s (checksum {c1}) -- {minutes} mins, {seconds} seconds")
        (minutes,seconds) = minutesFromSeconds(t2)
        print(f"- Avg Runtime (s) without Violation: {t2} s (checksum {c2}) -- {minutes} mins, {seconds} seconds")
        print()

def runLivenessScalabilityLayer(layer,batch):
    networkName = f"{layer}_layers_network"
    snapshotName = f"{layer}_layers_snapshot"
    snapshot = f"../scaling/{layer}_layers"
    bf = create(networkName,snapshotName,snapshot)
    target = "atla-re00"
    ingress = f"64.57.28.251 -> seat-re0{layer-1}"
    goodPath_interference = 0
    goodPath_interference_checksum = True
    goodPath_noInterference = 0
    goodPath_noInterference_checksum = True
    noGoodPath_time = 0
    noGoodPath_checksum = True
    for i in range(batch):
        (goodPath,hasInterference,time) = ingressNodeReaches(bf,target,ingress,dp=False)
        cex = goodPath != None and not hasInterference
        print(f"... good path without interference runtime {time} (checksum {cex})")
        goodPath_noInterference += time
        goodPath_noInterference_checksum = goodPath_noInterference_checksum and cex
        (goodPath,hasInterference,time) = ingressNodeReachesWithInterference(bf,target,ingress,dp=False)
        cex = goodPath != None and hasInterference
        print(f"... good path with interference runtime {time} (checksum {cex})")
        goodPath_interference += time
        goodPath_interference_checksum = goodPath_interference_checksum and cex
        
        # (goodPath,hasInterference,time) = noGoodPath(networkName,snapshotName,snapshot,target,dp=False)
        # cex = goodPath == None and not hasInterference
        # print(f"... no good path runtime {time} (checksum {cex})")
        # noGoodPath_time += time
        # noGoodPath_checksum = noGoodPath_checksum and cex

    avg_goodPath_interference = round(goodPath_interference / batch,3)
    avg_goodPath_noInterference = round(goodPath_noInterference / batch,3)
    avg_noGoodPath_time = round(noGoodPath_time / batch,3)
    return (avg_goodPath_interference,goodPath_interference_checksum,avg_goodPath_noInterference,goodPath_noInterference_checksum,avg_noGoodPath_time,noGoodPath_checksum)

def runLivenessScalability(layers,batch):
    for layer in layers:
        print(f"Running for [Layer {layer}]")
        (t1,c1,t2,c2,t3,c3) = runLivenessScalabilityLayer(layer,batch)
        (minutes,seconds) = minutesFromSeconds(t1)
        print(f"- Avg Runtime (s) with Good Path + Interference: {t1} s (checksum {c1}) -- {minutes} mins, {seconds} seconds")
        (minutes,seconds) = minutesFromSeconds(t2)
        print(f"- Avg Runtime (s) with Good Path + Not Interference: {t2} s (checksum {c2}) -- {minutes} mins, {seconds} seconds")
        # (minutes,seconds) = minutesFromSeconds(t3)
        # print(f"- Avg Runtime (s) with No Good Path: {t3} s (checksum {c3}) -- {minutes} mins, {seconds} seconds")
        print()