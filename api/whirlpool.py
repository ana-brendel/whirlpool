# Python clauses useful for easily calling pybatfish API
class Clause:
    def __init__(self,communities:list[str]=[],as_path:list[str]=[],prefixes:list[str]=[],as_path_length:int=-1):
        self.communities = communities
        self.prefixes = prefixes
        self.as_path = as_path
        self.as_path_length = as_path_length

    def format(self) -> str:
        communityStrings = list(map(lambda c: f"comm = {c}",self.communities))
        asPathStrings = list(map(lambda c: f"asPath = {c}",self.as_path))
        prefixStrings = list(map(lambda p: f"prefix = {p}",self.prefixes))
        asPathLengthString = [f"asPathLength = {self.as_path_length}"] if 0 <= self.as_path_length else []
        joined = " & ".join(communityStrings+asPathStrings+prefixStrings+asPathLengthString)
        return f"~{joined}~"
    
class Property:
    def __init__(self,clauses:list[Clause]=[]):
        self.clauses = clauses

    def formatProperty(self) -> str:
        if self.clauses == []:
            return "~~"
        else:
            return "".join(map(lambda c: c.format(),self.clauses))

class LocationPropertyPair:
    # location should be either: ip -> ip for edge or ip for node (already formatted)
    # property should be a list of clauses
    def __init__(self,location:str,property:list[Clause]):
        self.location = location 
        self.property = property

    def formatProperty(self) -> str:
        if self.property == []:
            return "~~"
        else:
            return "".join(map(lambda c: c.format(),self.property))

class ReachabilityQuery:
    def __init__(self, 
            prefix:str, 
            target:LocationPropertyPair,
            assumptions:list[LocationPropertyPair]=[],
            default:Property=None,
            ingress:list[str]=[],
            exact_communities:bool=False,
            compute_dp:bool=False):
        self.prefix = prefix
        self.target = target
        self.assumptions = assumptions
        self.default = default
        self.ingress = ingress
        self.exact_communities = exact_communities
        self.compute_dp = compute_dp
    
    def getPrefix(self):
        return self.prefix
    
    def getIngress(self):
        return None if self.ingress == [] else ",".join(self.ingress)
    
    def defaultAssumption(self):
        return None if self.default == None else self.default.formatProperty()
    
    def getExactCommunities(self):
        return self.exact_communities
    
    def getComputeDP(self):
        return self.compute_dp
    
    def targetProperty(self):
        return self.target.formatProperty()
    
    def targetLocation(self):
        return self.target.location
    
    def assumptionLocations(self):
        return None if self.assumptions == None or self.assumptions == [] else ",".join(map(lambda a: a.location,self.assumptions))
    
    def assumptionProperties(self):
        return None if self.assumptions == None or self.assumptions == [] else ",".join(map(lambda a: a.formatProperty(),self.assumptions))
    
class IsolationQuery:
    def __init__(self, 
            target:LocationPropertyPair,
            assumptions:list[LocationPropertyPair]=[],
            default:Property=Property([]),
            exact_communities:bool=False,
            isolate_violations:bool=False,
            compute_dp:bool=False):
        self.target = target
        self.assumptions = assumptions
        self.default = default
        self.exact_communities = exact_communities
        self.isolate_violations = isolate_violations
        self.compute_dp = compute_dp

    def refines(self):
        return self.refine
    
    def defaultAssumption(self):
        return self.default.formatProperty()
    
    def targetProperty(self):
        return self.target.formatProperty()
    
    def targetLocation(self):
        return self.target.location
    
    def assumptionLocations(self):
        return ",".join(map(lambda a: a.location,self.assumptions))
    
    def assumptionProperties(self):
        return ",".join(map(lambda a: a.formatProperty(),self.assumptions))
    
    def getExactCommunities(self):
        return self.exact_communities
    
    def getComputeDP(self):
        return self.compute_dp
    
    def getIsolateViolations(self):
        return self.isolate_violations
    
# The functions below are some syntactic sugar to use for queries - in the future should probably directly include in API

def falseProperty() -> Property:
    # pretty hacky right now, can probably include some actual arguement to pybatfish
    return Property([Clause(prefixes=["10.0.0.0/8","!10.0.0.0/8"])])

def trueProperty() -> Property:
    return Property()

def trueAtLocation(location : str) -> LocationPropertyPair:
    return LocationPropertyPair(location=location,property=[])

def falseAtLocation(location :str) -> LocationPropertyPair:
    falses = falseProperty()
    return LocationPropertyPair(location=location,property=falses.clauses)

OUTGOING = "ALL-OUTGOING"

def negate(s):
    return f"!{s}"

def incomingEdgesTo(dst):
    return f"* -> {dst}"

def outgoingEdgesFrom(src):
    return f"{src} -> *"