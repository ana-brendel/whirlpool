import os

def src(config):
    return os.path.join(os.path.join(os.getcwd(),"sources"),f"{config}.conf")

def read(file):
    with open(file, 'r') as f:
        return f.read()

def write(file,content):
    with open(file, 'w') as f:
        f.write(content)

ADD_NEIGHBOR = "<<ADD NEW BGP NEIGHBOR>>"

original = {
    "chic" : "64.57.28.241",
    "newy32aoa" : "64.57.28.242",
    "atla" : "64.57.28.243",
    "hous" : "64.57.28.244",
    "kans" : "64.57.28.245",
    "salt" : "64.57.28.246",
    "seat" : "64.57.28.247",
    "losa" : "64.57.28.248",
    "wash" : "64.57.28.249",
    "clev" : "64.57.28.250"
}

def offset_ip(conf,offset):
    vals = list(map(lambda v: int(v),original[conf].split(".")))
    vals[0] += offset
    vals[0] = vals[0] % 255
    if offset >= 255:
        vals[1] += 1
    return ".".join(list(map(lambda v: str(v),vals)))

def offset_ips(offset):
    result = []
    for k in original:
        result += [(original[k],offset_ip(k,offset))]
    return result

names = [
    "ATLA-re0","ATLA-re1",
    "CHIC-re0","CHIC-re1",
    "CLEV-re0","CLEV-re1",
    "HOUS-re0","HOUS-re1",
    "KANS-re0","KANS-re1",
    "LOSA-re0","LOSA-re1",
    "NEWY-re0","NEWY-re1",
    "salt-re0","salt-re1",
    "SEAT-re0","SEAT-re1",
    "WASH-re0","WASH-re1"
]

def offset_names(offset):
    return list(map(lambda name: (name,f"{name}{offset}"),names))

def offset_new_neighbors(conf,offset):
    less = offset_ip(conf,offset-1) if offset > 0 else ""
    under = "" if less == "" else f"neighbor {less}"+"{\n\t\tdescription UNDER;\n}"
    more = offset_ip(conf,offset+1)
    over = f"neighbor {more}"+"{\n\t\tdescription OVER;\n}"
    return under + "\n" + over

def rep(config,offset,dst):
    file = f"{config}_{offset}.conf"
    new_config = os.path.join(dst,file)
    new_names = offset_names(offset)
    new_ips = offset_ips(offset)
    new_neighbors = offset_new_neighbors(config,offset)
    original_file = src(config)
    contents = read(original_file)
    replacements = new_names + new_ips + [(ADD_NEIGHBOR,new_neighbors)]
    for (term,replacement) in replacements:
        if term != replacement:
            contents = contents.replace(term,replacement)
    write(new_config,contents)

def create(layers,destination):
    for layer in range(layers):
        for config in original:
            rep(config,layer,destination)

def make_for_layers(layers):
    new_directory = os.path.join(os.getcwd(),f"{layers}_layers")
    print(new_directory)
    os.mkdir(new_directory)
    new_directory = os.path.join(new_directory,"configs")
    os.mkdir(new_directory)
    create(layers,new_directory)

def construct():
    for layer in [50,75,100,125,150,175,200,250,300]:
        make_for_layers(layer)

construct()
