# Common imports
import sys
from common import minutesFromSeconds

# Experiment specific imports
from block_to_external import blockToExternal,blockToExternalCoverViolations
from reachability import noGoodPath,ingressNodeReachesWithInterference,ingressNodeReaches

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

def runIsolationWithViolations(layer,batch):
    print("[ISOLATION] Not Verified (with violations)")
    print(f" -- layer: {layer}")
    networkName = f"{layer}_layers_network"
    snapshotName = f"{layer}_layers_snapshot"
    snapshot = f"../scaling/{layer}_layers"
    runtime = 0
    checksum = True
    for i in range(batch):
        (cex,time) = blockToExternal(networkName,snapshotName,snapshot,dp=False)
        print(f"... block to external runtime {time} (checksum {cex})")
        runtime += time
        checksum = checksum and (cex == 66)
    avg = round(runtime / batch,3)
    return (avg,checksum)

def runIsolationWithoutViolations(layer,batch):
    print("[ISOLATION] Verified (no violations)")
    print(f" -- layer: {layer}")
    networkName = f"{layer}_layers_network"
    snapshotName = f"{layer}_layers_snapshot"
    snapshot = f"../scaling/{layer}_layers"
    runtime = 0
    checksum = True
    for i in range(batch):
        (cex,time) = blockToExternalCoverViolations(networkName,snapshotName,snapshot,getViolationsForOffset(layer),dp=False)
        print(f"... block to external runtime {time} (checksum {cex})")
        runtime += time
        checksum = checksum and (cex == 66)
    avg = round(runtime / batch,3)
    return (avg,checksum)

def runReachabilityNoGoodPath(layer,batch):
    print("[REACHABILITY] No Good Path")
    print(f" -- layer: {layer}")
    networkName = f"{layer}_layers_network"
    snapshotName = f"{layer}_layers_snapshot"
    snapshot = f"../scaling/{layer}_layers"
    target = "atla-re00"
    runtime = 0
    checksum = True
    for i in range(batch):
        (goodPath,hasInterference,time) = noGoodPath(networkName,snapshotName,snapshot,target,dp=False)
        cex = goodPath != None and not hasInterference
        print(f"... no good path runtime {time} (checksum {cex})")
        runtime += time
        checksum = checksum and cex
    avg = round(runtime / batch,3)
    return (avg,checksum)

def runReachabilityGoodPathWithInterference(layer,batch):
    print("[REACHABILITY] Good Path + Interference")
    print(f" -- layer: {layer}")
    networkName = f"{layer}_layers_network"
    snapshotName = f"{layer}_layers_snapshot"
    snapshot = f"../scaling/{layer}_layers"
    target = "atla-re00"
    ingress = f"64.57.28.251 -> seat-re0{layer-1}"
    runtime = 0
    checksum = True
    for i in range(batch):
        (goodPath,hasInterference,time) = ingressNodeReachesWithInterference(networkName,snapshotName,snapshot,target,ingress,dp=False)
        cex = goodPath != None and hasInterference
        print(f"... good path with interference runtime {time} (checksum {cex})")
        runtime += time
        checksum = checksum and cex
    avg = round(runtime / batch,3)
    return (avg,checksum)

def runReachabilityGoodPathNoInterference(layer,batch):
    print("[REACHABILITY] Good Path + No Interference")
    print(f" -- layer: {layer}")
    networkName = f"{layer}_layers_network"
    snapshotName = f"{layer}_layers_snapshot"
    snapshot = f"../scaling/{layer}_layers"
    target = "atla-re00"
    ingress = f"64.57.28.251 -> seat-re0{layer-1}"
    runtime = 0
    checksum = True
    for i in range(batch):
        (goodPath,hasInterference,time) = ingressNodeReaches(networkName,snapshotName,snapshot,target,ingress,dp=False)
        cex = goodPath != None and hasInterference
        print(f"... good path with interference runtime {time} (checksum {cex})")
        runtime += time
        checksum = checksum and cex
    avg = round(runtime / batch,3)
    return (avg,checksum)

def run (layers,batch,test):
    for layer in layers:
        # --------------------- Isolation ----------------------------
        if test == 0:
            (runtime,checksum) = runIsolationWithViolations(layer,batch)
        elif test == 1:
            (runtime,checksum) = runIsolationWithoutViolations(layer,batch)
        # --------------------- Reachability ----------------------------
        elif test == 2:
            (runtime,checksum) = runReachabilityNoGoodPath(layer,batch)
        elif test == 3:
            (runtime,checksum) = runReachabilityGoodPathWithInterference(layer,batch)
        elif test == 4:
            (runtime,checksum) = runReachabilityGoodPathNoInterference(layer,batch)
        # ----------------------------------------------------------
        # --------------------- Display ----------------------------
        # ----------------------------------------------------------
        (minutes,seconds) = minutesFromSeconds(runtime)
        print(f"- Avg Runtime (s): {runtime} s (checksum {checksum}) -- {minutes} mins, {seconds} seconds")

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# RUN: python3 individual.py {test number} {layer}

layers = [50,100,150,200,250,300,350]
print("Running with heap set to 16g in the ./tools/bazel_run.sh script (modified from 12)...\n")
test = int(sys.argv[1])
layer = int(sys.argv[2])

if layer in layers and 0 <= test < 5:
    run([layer],1,test)