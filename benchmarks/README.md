# Benchmarks
This directory contains the benchmarks that we used to evaluate `whirlpool`. There are two sets of experiments: (1) verifying properties of the _Internet2_ benchmark used for evaluation in prior works to see how our tool performs and (2) scalability tests that run both isolation and reachability queries on modifications of the _Internet2_ configurations in order to see how the tool scales. In our paper, we additionally cited an evaluation performed on regional data centers for a large cloud service provider, but these are private networks so we cannot share those benchmarks/evaluations. They are described in the paper.

### Getting Started
You should follow the instructions in this repo's main [README](../README.md) to install, build and run Batfish with `whirlpool`. Before running the different benchmarks, you should have Batfish with `whirlpool` running in its own terminal/shell. To do so, as stated in the README, in a fresh terminal run:
```
directory % cd whirlpool/batfish
directory/whirlpool/batfish % ./tools/bazel_run.sh
```

### Internet2 Benchmarks
There are two properties which prior work verifies for the _Internet2_ benchmarks.
* The _No Martians_ property verifies that no routers in the network accept any martain prefixes (a predetermined set of bad prefixes).
* The _Block to External_ property verifies that no router advertises routes with a particular commmunity to neighbors outside the network.

To run the _Internet2_ benchmarks, you should run the following command from the _scripts_ directory:
`% python3 run.py internet2 n` where _n_ is the number of times each test is ran to be averaged

The results should print out to the terminal and look something like the following. These results came from just running once (no need to average).
```
Running with heap set to 16g in the ./tools/bazel_run.sh script (modified from 12)...

NO MARTIANS
- Avg Runtime (s) with Violation: 57.68 s (checksum True) -- 0.0 mins, 57.68 seconds

BLOCK TO EXTERNAL
- Avg Runtime (s) with Violation: 83.78 s (checksum True) -- 1.0 mins, 23.78 seconds
- Avg Runtime (s) without Violation: 100.24 s (checksum True) -- 1.0 mins, 40.239999999999995 seconds
- Avg Runtime (s) Isolating Violations: 186.62 s (checksum True) -- 3.0 mins, 6.6200000000000045 seconds
- Avg Runtime to Verify No Node Strips BTE: 12.498 s (checksum True) -- 0.0 mins, 12.498 seconds
```

### Scalability Tests
There are two scalability tests that we used to evaluate `whirlpool`; one for isolation properties and one for reachability properties. Both sets of tests were ran on modified versions of the _Internet2_ network. We layered the network to increase the number of edges and nodes in the network. Each layer in the modified network is the same as the original _Internet2_ network and each node in a given layer is connected to that same node on the layers above and below the one it is on.

To run the scalability tests for the **isolation** property, you should run the following command in the _scripts_ directory:
`% python3 run.py isolationScale n` where _n_ is the number of times each test is ran to be averaged

The results print out to the terminal and look like the following.  This output came from running a version of the script which doesn't include all layers, for example in this case it just ran tests with 50 and 75 layers (each test ran once). The command was: `% python3 run.py isolationScale 1 50 75`. The possible layers for the scalability tests for isolation are: 50,75,100,125,150,175.

**time is off because of computer issues -- NEED TO RERUN**
```
Running with heap set to 16g in the ./tools/bazel_run.sh script (modified from 12)...

Running for [Layer 50] [averaged over 1 runs]
... block to external runtime 216.52 (checksum 84)
... block to external no violations runtime 186.8 (checksum 0)
- Avg Runtime (s) with Violation: 216.52 s (checksum False) -- 3.0 mins, 36.52000000000001 seconds
- Avg Runtime (s) without Violation: 186.8 s (checksum True) -- 3.0 mins, 6.800000000000011 seconds

Running for [Layer 75] [averaged over 1 runs]
... block to external runtime 281.25 (checksum 83)
... block to external no violations runtime 232.88 (checksum 0)
- Avg Runtime (s) with Violation: 281.25 s (checksum False) -- 4.0 mins, 41.25 seconds
- Avg Runtime (s) without Violation: 232.88 s (checksum True) -- 3.0 mins, 52.879999999999995 seconds
```

To run the scalability tests for the **reachability** property, you should run the following command in the _scripts_ directory:
`% python3 run.py reachabilityScale n` where _n_ is the number of times each test is ran to be averaged

The results print out to the terminal and look like the following.  This output came from running a version of the script which doesn't include all layers, for example in this case it just ran tests with 50 and 75 layers (each test ran once). The command was: `% python3 run.py reachabilityScale 1 50 100`. The possible layers for the scalability tests for isolation are: 50,100,150,200,250,300.

**time is off because of computer issues -- NEED TO RERUN**
```
Running with heap set to 16g in the ./tools/bazel_run.sh script (modified from 12)...

Running for [Layer 50]
... good path without interference runtime 131.28 (checksum True)
... good path with interference runtime 136.6 (checksum True)
- Avg Runtime (s) with Good Path + Interference: 136.6 s (checksum True) -- 2.0 mins, 16.599999999999994 seconds
- Avg Runtime (s) with Good Path + Not Interference: 131.28 s (checksum True) -- 2.0 mins, 11.280000000000001 seconds

Running for [Layer 100]
... good path without interference runtime 226.96 (checksum True)
... good path with interference runtime 226.4 (checksum True)
- Avg Runtime (s) with Good Path + Interference: 226.4 s (checksum True) -- 3.0 mins, 46.400000000000006 seconds
- Avg Runtime (s) with Good Path + Not Interference: 226.96 s (checksum True) -- 3.0 mins, 46.96000000000001 seconds
```