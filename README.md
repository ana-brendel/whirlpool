# whirlpool
`whirlpool` is a _property-directed_ control plane verifier. It is implemented as a [Batfish](https://batfish.org/) question, and as such is accessible via the [_pybatfish_](https://github.com/batfish/pybatfish) Python client.

This repo includes a fork of Batfish which includes the implementation of `whirlpool` and instructions for running `whirlpool`. Additionally, the _notebooks_ directory contains Jupyter notebooks which show examples of using `whirlpool`. The _benchmarks_ directory contains instructions and source code for running the benchmarks which we used to evaluate `whirlpool` in the paper which is currently under submission.

### Getting Started
In order to install, build and run the version of Batfish which contains `whirlpool, do the following:
1. Follow these [instructions](https://github.com/ana-brendel/batfish/blob/master/docs/building_and_running/README.md) from the Batfish repo to download support for building with Bazel (which is the framework used to build and run Batfish). Specifically, the prerequistes are: Java 17 JDK, Python 3.10 or later, git, and [bazelisk](https://github.com/bazelbuild/bazelisk#installation).
2. You should create a virtual python environment. You will have to install any dependencies including `pybatfish`. The `pybatfish` instructions might be helpful if you get stuff; they're located [here](https://github.com/batfish/pybatfish/blob/master/README.md). To do this and install dependencies, run the following commands:
```
directory % cd .../batfish/verification
directory/batfish/verification % python3 -m venv .
directory/batfish/verification % source ./bin/activate
directory/batfish/verification % pip install pandas 
directory/batfish/verification % pip install jinja2 
directory/batfish/verification % pip install jupyter 
directory/batfish/verification % python3 -m pip install --upgrade pip
directory/batfish/verification % python3 -m pip install --upgrade pybatfish
```

### Running Verification with Batfish on Examples
_**To run Batfish with `whirlpool`, execute the following commands:**_
```
directory % cd whirlpool/batfish
directory/whirlpool/batfish % ./tools/bazel_run.sh
```
This command will not terminate, but it will start the Batfish process so that the `pybatfish` client can query. It should tell you `Build completed successfully` and then continue running the program in the page waiting for the `pybatfish` client to query.

The jupyter notebooks (`SafetyExamples.ipynb` and `LivenessExamples.ipynb`) within the _notebooks_ directory contain descriptions of the API and examples of how `whirlpool` can be used. These notebooks include how to make safety property verification queries and liveness property verification queries respectively.

### Running Benchmarks
To run the (publicly available) benchmarks which we used to evaluate `whirlpool`, please refer to the README in the _benchmarks_ repo.