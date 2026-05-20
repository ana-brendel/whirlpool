# Common imports
import sys
from common import minutesFromSeconds

# Experiment specific imports
from no_martian import run as run_no_martian_batched
from block_to_external import run_no_strip_batched
from block_to_external import run as run_bte_batched
from scalability import runSafetyScalability,runLivenessScalability

def comparisons(batch):
    print("NO MARTIANS")
    (avg_runtime,checksum) = run_no_martian_batched(batch)
    (minutes,seconds) = minutesFromSeconds(avg_runtime)
    print(f"- Avg Runtime (s) with Violation: {avg_runtime} s (checksum {checksum}) -- {minutes} mins, {seconds} seconds")
    print()
    print("BLOCK TO EXTERNAL")
    (a1,a2,b1,b2,c1,c2) = run_bte_batched(batch)
    for (label,runtime,checksum) in [("with Violation",a1,a2),("without Violation",b1,b2),("Isolating Violations",c1,c2)]:
        (minutes,seconds) = minutesFromSeconds(runtime)
        print(f"- Avg Runtime (s) {label}: {runtime} s (checksum {checksum}) -- {minutes} mins, {seconds} seconds")
    (avg_runtime,checksum) = run_no_strip_batched(batch)
    (minutes,seconds) = minutesFromSeconds(avg_runtime)
    print(f"- Avg Runtime to Verify No Node Strips BTE: {avg_runtime} s (checksum {checksum}) -- {minutes} mins, {seconds} seconds")
    print()

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 5:
        print("Expects 2 command line arguments. The first should be the type of benchmark to run (internet2 or isolationScale or reachabilityScale). The second should be the number of times the test should run and be averaged.")
    TEST_TYPE = sys.argv[1]
    BATCH_SIZE = int(sys.argv[2])
    print("Running with heap set to 16g in the ./tools/bazel_run.sh script (modified from 12)...\n")
    if TEST_TYPE == "internet2" and len(sys.argv) == 3:
        comparisons(BATCH_SIZE)
    elif TEST_TYPE == "isolationScale":
        tests = [50,75,100,125,150,175]
        if len(sys.argv) == 3:
            runSafetyScalability(tests,BATCH_SIZE)
        elif len(sys.argv) == 5:
            lowest = int(sys.argv[3])
            highest = int(sys.argv[4])
            assert lowest in tests and highest in tests, "Ranges provided not in the set of tests (50,75,100,125,150,175)"
            restricted = list(filter(lambda l: lowest <= l and l <= highest,tests))
            runSafetyScalability(restricted,BATCH_SIZE)
        else:
            print("Either no range is provided, or user provides the smallest (inclusive) and largest (inclusive) test to run (out of 50,75,100,125,150,175).")
    elif TEST_TYPE == "reachabilityScale":
        tests = [50,100,150,200,250,300]
        if len(sys.argv) == 3:
            runLivenessScalability(tests,BATCH_SIZE)
        elif len(sys.argv) == 5:
            lowest = int(sys.argv[3])
            highest = int(sys.argv[4])
            assert lowest in tests and highest in tests, "Ranges provided not in the set of tests (50,100,150,200,250,300)"
            restricted = list(filter(lambda l: lowest <= l and l <= highest,tests))
            runLivenessScalability(restricted,BATCH_SIZE)
        else:
            print("Invalid arguments: Either no range should be provided, or user should provide the smallest (inclusive) and largest (inclusive) test to run (out of 50,100,150,200,250,300).")
    else:
        print("The first argument should be either \'internet2\' or \'isolationScale\' or \'reachabilityScale\'.")

