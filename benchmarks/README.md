# Benchmarks
This directory contains the benchmarks that we used to evaluate `whirlpool`. There are two sets of experiments: (1) verifying properties of the _Internet2_ benchmark used for evaluation in prior works to see how our tool performs and (2) scalability tests that run both isolation and reachability queries on modifications of the _Internet2_ configurations in order to see how the tool scales. In our paper, we additionally cited an evaluation performed on regional data centers for a large cloud service provider, but these are private networks so we cannot share those benchmarks/evaluations. They are described in the paper.

### Getting Started
You should follow the instructions in this repo's main [README](../README.md) to install, build and run Batfish with `whirlpool`. Before running the different benchmarks, you should have Batfish with `whirlpool` running in its own terminal/shell. To do so, as stated in the README, in a fresh terminal run:
```
directory % cd whirlpool/batfish
directory/whirlpool/batfish % ./tools/bazel_run.sh
```

The following benchmarks should be ran in a separate terminal window. In order to guarantee that all of the correct dependencies are downloaded, be sure to run them from the Python environment which was set up in this repo's main [README](../README.md). This is done by just calling `% source ./bin/activate`.

### Internet2 Benchmarks
There are two properties which prior work verifies for the _Internet2_ benchmarks.
* The _No Martians_ property verifies that no routers in the network accept any martain prefixes (a predetermined set of bad prefixes).
* The _Block to External_ property verifies that no router advertises routes with a particular commmunity to neighbors outside the network.

To run the _Internet2_ benchmarks, you should run the following command from the _scripts_ directory:
`% python3 run.py internet2 n` where _n_ is the number of times each test is ran to be averaged.

The results should print out to the terminal and look something like the following. These results came from averaging _three_ runs.
```
Running with heap set to 16g in the ./tools/bazel_run.sh script (modified from 12)...

NO MARTIANS
- Avg Runtime (s) with Violation: 53.41 s (checksum True) -- 0.0 mins, 53.41 seconds

BLOCK TO EXTERNAL
- Avg Runtime (s) with Violation: 48.06 s (checksum True) -- 0.0 mins, 48.06 seconds
- Avg Runtime (s) without Violation: 40.39 s (checksum True) -- 0.0 mins, 40.39 seconds
- Avg Runtime (s) Isolating Violations: 88.36 s (checksum True) -- 1.0 mins, 28.36 seconds
- Avg Runtime to Verify No Node Strips BTE: 8.346 s (checksum True) -- 0.0 mins, 8.346 seconds
```

In order to see the queries and results that are taking place in the scripts cited above, you can look at the Jupyter notebook [scripts/internet2tests.ipynb](scripts/internet2tests.ipynb).

### Scalability Tests
There are two scalability tests that we used to evaluate `whirlpool`; one for isolation properties and one for reachability properties. Both sets of tests were ran on modified versions of the _Internet2_ network. We layered the network to increase the number of edges and nodes in the network. Each layer in the modified network is the same as the original _Internet2_ network and each node in a given layer is connected to that same node on the layers above and below the one it is on.

Before running the scalability tests, you'll need to generate all of the configs for each layer. You can do so by running the following commands:
```
whirlpool/batfish/benchmarks % cd scaling
whirlpool/batfish/benchmarks/scaling % python3 replicate.py
```

To run the scalability tests for the **isolation** property, you should run the following command in the _benchmarks/scripts_ directory:
`% python3 run.py isolationScale n` where _n_ is the number of times each test is ran to be averaged

The results print out to the terminal and look like the following.  This output came from running a version of the script which doesn't include all layers, for example in this case it just ran tests with 50 and 75 layers (each test ran once). The command was: `% python3 run.py isolationScale 1 50 75`. The possible layers for the scalability tests for isolation are: 50,75,100,125,150,175.

```
Running with heap set to 16g in the ./tools/bazel_run.sh script (modified from 12)...

Running for [Layer 50] [averaged over 1 runs]
... block to external runtime 63.62 (checksum 84)
... block to external no violations runtime 48.43 (checksum 0)
- Avg Runtime (s) with Violation: 63.62 s (checksum True) -- 1.0 mins, 3.6199999999999974 seconds
- Avg Runtime (s) without Violation: 48.43 s (checksum True) -- 0.0 mins, 48.43 seconds

Running for [Layer 75] [averaged over 1 runs]
... block to external runtime 84.71 (checksum 83)
... block to external no violations runtime 57.47 (checksum 0)
- Avg Runtime (s) with Violation: 84.71 s (checksum True) -- 1.0 mins, 24.709999999999994 seconds
- Avg Runtime (s) without Violation: 57.47 s (checksum True) -- 0.0 mins, 57.47 seconds
```

To run the scalability tests for the **reachability** property, you should run the following command in the _scripts_ directory:
`% python3 run.py reachabilityScale n` where _n_ is the number of times each test is ran to be averaged

The results print out to the terminal and look like the following.  This output came from running a version of the script which doesn't include all layers, for example in this case it just ran tests with 50 and 75 layers (each test ran once). The command was: `% python3 run.py reachabilityScale 1 50 100`. The possible layers for the scalability tests for isolation are: 50,100,150,200,250,300.

```
Running with heap set to 16g in the ./tools/bazel_run.sh script (modified from 12)...

Running for [Layer 50]
... good path without interference runtime 50.52 (checksum True)
... good path with interference runtime 48.47 (checksum True)
- Avg Runtime (s) with Good Path + Interference: 48.47 s (checksum True) -- 0.0 mins, 48.47 seconds
- Avg Runtime (s) with Good Path + Not Interference: 50.52 s (checksum True) -- 0.0 mins, 50.52 seconds

Running for [Layer 100]
... good path without interference runtime 120.48 (checksum True)
... good path with interference runtime 128.0 (checksum True)
- Avg Runtime (s) with Good Path + Interference: 128.0 s (checksum True) -- 2.0 mins, 8.0 seconds
- Avg Runtime (s) with Good Path + Not Interference: 120.48 s (checksum True) -- 2.0 mins, 0.480000000000004 seconds
```