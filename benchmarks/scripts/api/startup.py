# COPIED FROM PYBATFISH REPO

# Importing required libraries, setting up logging, and loading questions
import logging
import random  # noqa: F401
from typing import List, Optional  # noqa: F401

import pandas as pd
from IPython.display import display
from pandas.io.formats.style import Styler

from pybatfish.client.session import Session  # noqa: F401

# noinspection PyUnresolvedReferences
from pybatfish.datamodel import Edge, Interface  # noqa: F401
from pybatfish.datamodel.answer import TableAnswer
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints  # noqa: F401
from pybatfish.datamodel.route import BgpRoute  # noqa: F401
from pybatfish.util import get_html

# Whirlpool specific queries
from api.whirlpool import ReachabilityQuery,IsolationQuery

# Configure all pybatfish loggers to use WARN level
logging.getLogger("pybatfish").setLevel(logging.WARN)

pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", None)
# Prevent rendering text between '$' as MathJax expressions
pd.set_option("display.html.use_mathjax", False)

# UUID for CSS styles used by pandas styler.
# Keeps our notebook HTML deterministic when displaying dataframes
_STYLE_UUID = "pybfstyle"


class MyStyler(Styler):
    """A custom styler for displaying DataFrames in HTML"""

    def __repr__(self):
        return repr(self.data)


def show(df):
    """
    Displays a dataframe as HTML table.

    Replaces newlines and double-spaces in the input with HTML markup, and
    left-aligns the text.
    """
    if isinstance(df, TableAnswer):
        df = df.frame()

    # workaround for Pandas bug in Python 2.7 for empty frames
    if not isinstance(df, pd.DataFrame) or df.size == 0:
        display(df)
        return
    display(
        MyStyler(df)
        .set_uuid(_STYLE_UUID)
        .format(get_html)
        .set_properties(**{"text-align": "left", "vertical-align": "top"})
    )

# Help functions to run tests and examples easier
def create(networkName:str,snapshotName:str,snapshotPath:str):
    '''Creates a batfish session for the snapshot located at `snapshotPath` and is given the provided `networkName` and `snapshotName`.'''
    bf = Session(host="localhost")
    bf.set_network(networkName)
    bf.init_snapshot(snapshotPath, name=snapshotName, overwrite=True)
    return bf

# This function is what includes the call to the pybatfish isolation property verification question
def runIsolationVerificationQuestion(bf,query:IsolationQuery):
    if query == None:
        return bf.q.whirlpoolIsolation().answer().frame()
    assumptionLocations = query.assumptionLocations()
    defaultAssumption = query.defaultAssumption()
    if assumptionLocations == "":
        if defaultAssumption == "":
            result = bf.q.whirlpoolIsolation(
                target=query.targetProperty(),
                location=query.targetLocation(),
                exact_communities=query.getExactCommunities(),
                isolate_violations=query.getIsolateViolations(),
                compute_data_plane=query.getComputeDP()).answer()
        else:
            result = bf.q.whirlpoolIsolation(
                target=query.targetProperty(),
                location=query.targetLocation(),
                default_assumption = defaultAssumption,
                exact_communities=query.getExactCommunities(),
                isolate_violations=query.getIsolateViolations(),
                compute_data_plane=query.getComputeDP()).answer()
    elif defaultAssumption == "":
        result = bf.q.whirlpoolIsolation(
            target=query.targetProperty(),
            location=query.targetLocation(),
            assumption_locations=assumptionLocations,
            assumptions=query.assumptionProperties(),
            exact_communities=query.getExactCommunities(),
            isolate_violations=query.getIsolateViolations(),
            compute_data_plane=query.getComputeDP()).answer()
    else:
        result = bf.q.whirlpoolIsolation(
            target=query.targetProperty(),
            location=query.targetLocation(),
            assumption_locations=assumptionLocations,
            assumptions=query.assumptionProperties(),
            default_assumption = defaultAssumption,
            exact_communities=query.getExactCommunities(),
            isolate_violations=query.getIsolateViolations(),
            compute_data_plane=query.getComputeDP()).answer()
    return result.frame()

# This function is what includes the call to the pybatfish reachability property verification question
def runReachabilityVerificationQuestion(bf,query:ReachabilityQuery):
    if query == None:
        return bf.q.whirlpoolReachability().answer().frame()
    assumptionLocations = query.assumptionLocations()
    defaultAssumption = query.defaultAssumption()
    ingressEdge = query.getIngress()
    if ingressEdge == None:
        if assumptionLocations == None:
            if defaultAssumption == None:
                result = bf.q.whirlpoolReachability(
                    prefix=query.getPrefix(),
                    target=query.targetProperty(),
                    location=query.targetLocation(),
                    exact_communities=query.getExactCommunities(),
                    compute_data_plane=query.getComputeDP()).answer()
            else:
                result = bf.q.whirlpoolReachability(
                    prefix=query.getPrefix(),
                    target=query.targetProperty(),
                    location=query.targetLocation(),
                    default_assumption = defaultAssumption,
                    exact_communities=query.getExactCommunities(),
                    compute_data_plane=query.getComputeDP()).answer()
        elif defaultAssumption == None:
            result = bf.q.whirlpoolReachability(
                prefix=query.getPrefix(),
                target=query.targetProperty(),
                location=query.targetLocation(),
                assumption_locations=assumptionLocations,
                assumptions=query.assumptionProperties(),
                exact_communities=query.getExactCommunities(),
                compute_data_plane=query.getComputeDP()).answer()
        else:
            result = bf.q.whirlpoolReachability(
                prefix=query.getPrefix(),
                target=query.targetProperty(),
                location=query.targetLocation(),
                assumption_locations=assumptionLocations,
                assumptions=query.assumptionProperties(),
                default_assumption = defaultAssumption,
                exact_communities=query.getExactCommunities(),
                compute_data_plane=query.getComputeDP()).answer()
    else: 
        if assumptionLocations == None:
            if defaultAssumption == None:
                result = bf.q.whirlpoolReachability(
                    prefix=query.getPrefix(),
                    target=query.targetProperty(),
                    location=query.targetLocation(),
                    ingress=ingressEdge,
                    exact_communities=query.getExactCommunities(),
                    compute_data_plane=query.getComputeDP()).answer()
            else:
                result = bf.q.whirlpoolReachability(
                    prefix=query.getPrefix(),
                    target=query.targetProperty(),
                    location=query.targetLocation(),
                    default_assumption = defaultAssumption,
                    ingress=ingressEdge,
                    exact_communities=query.getExactCommunities(),
                    compute_data_plane=query.getComputeDP()).answer()
        elif defaultAssumption == None:
            result = bf.q.whirlpoolReachability(
                prefix=query.getPrefix(),
                target=query.targetProperty(),
                location=query.targetLocation(),
                assumption_locations=assumptionLocations,
                assumptions=query.assumptionProperties(),
                ingress=ingressEdge,
                exact_communities=query.getExactCommunities(),
                compute_data_plane=query.getComputeDP()).answer()
        else:
            result = bf.q.whirlpoolReachability(
                prefix=query.getPrefix(),
                target=query.targetProperty(),
                location=query.targetLocation(),
                assumption_locations=assumptionLocations,
                assumptions=query.assumptionProperties(),
                default_assumption = defaultAssumption,
                ingress=ingressEdge,
                exact_communities=query.getExactCommunities(),
                compute_data_plane=query.getComputeDP()).answer()
    return result.frame()

def runWhirlpoolQuery(networkName:str,snapshotName:str,snapshotPath:str,query,display:bool=False):
    bf = create(networkName,snapshotName,snapshotPath)
    if query == None:
        result = bf.q.whirlpoolIsolation().answer().frame()
    elif type(query) == ReachabilityQuery:
        result = runReachabilityVerificationQuestion(bf,query)
    elif type(query) == IsolationQuery:
        result = runIsolationVerificationQuestion(bf,query)
    if display:
        show(result)
    return result