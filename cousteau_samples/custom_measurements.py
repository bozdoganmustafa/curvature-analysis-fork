from ripe.atlas.cousteau import *
from datetime import datetime

# Owned key with all permissions related to Probes and Measurements. 
# Credit transfer and API Key operations are not permissioned.
RIPE_ATLAS_API_KEY_MUSTAFA = "e30d5008-41d8-4483-87c8-93c7245e2855"


# Fails due to lack of Credits.
def create_atlas_measurement():
    ping = Ping(af=4, target="www.google.gr", description="testing new wrapper")

    traceroute = Traceroute(
        af=4,
        target="www.ripe.net",
        description="testing",
        protocol="ICMP",
    )

    source = AtlasSource(
        type="area",
        value="WW",
        requested=5,
        tags={"include": ["system-ipv4-works"]}
    )

    source1 = AtlasSource(
        type="country",
        value="NL",
        requested=50,
        tags={"exclude": ["system-anchor"]}
    )

    atlas_request = AtlasCreateRequest(
        start_time=datetime.utcnow(),
        key=RIPE_ATLAS_API_KEY_MUSTAFA,
        measurements=[ping, traceroute],
        sources=[source, source1],
        is_oneoff=True
    )

    return atlas_request.create()


# Query all Probes for Amazon Web Service Asns.
# Finds 61 Probes as Connected & Public. Only 1 is an Anchor. 
def get_amazon_probes():

    amazon_asns = [
        "14618", "135630", "10124", "8987", "38895", "9059", 
        "19047", "17493", "39111", "395343", "7224", "58588", "16509"
    ]

    return get_probes(amazon_asns)

# Query all Probes for Google Cloud Platform Asns.
# Finds 37 Probes as Connected & Public. None is an Anchor. 
def get_google_cloud_probes():

    google_cloud_asns = [
        "19527", "36492", "55023", "139070", "36039", "394639", "139190",
        "13949", "396982", "395973", "26910", "394699", "22859", "40873",
        "43515", "394507", "6432", "36987", "15169", "22577", "36384",
        "45566", "19425", "36040", "19448", "16550", "16591", "26684",
        "41264", "36385"
    ]

    return get_probes(google_cloud_asns)

# Query all Probes for Microsoft Azure Asns.
# Finds 47 Probes as Connected & Public. None is an Anchor. 
def get_azure_probes():

    azure_asns = [
        "23468", "30575", "35106", "6291", "396463", "58862", "8068", 
        "398661", "395851", "8074", "8069", "59067", "397996", "17345", 
        "32476", "8075", "398658", "31792", "6194", "8073", "13399", 
        "398657", "398575", "63314", "25796", "395524", "398660", "398656", 
        "398961", "40066", "14719", "45139", "30135", "36006", "3598", 
        "5761", "12076", "8812", "8070", "13811", "26222", "8071", 
        "200517", "6182", "8072", "398659", "22692", "397466", "20046", 
        "6584", "395496"
    ]

    return get_probes(azure_asns)

# Query all Probes for Yahoo Asns.
# Finds 0 Probes as Connected & Public. 
def get_yahoo_probes():
    yahoo_asns = [
        "45501", "131898", "24296", "24572", "58720", "134706", "43428",
        "17457", "23926", "38032", "42173", "24236", "55417", "23816",
        "24031", "15896", "38045", "203070", "58721", "55898", "24506",
        "15635", "40986", "45915", "10229", "10228", "24376", "55416",
        "55517", "38072", "58525", "18293", "23879", "203220", "56173",
        "34082", "38033", "23880", "18140", "34010", "265584", "24018",
        "203219", "10230", "204000", "7233", "45502", "45863", "55418",
        "23663"
    ]

    return get_probes(yahoo_asns)

def get_probes(asn_list):
    all_probe_ids = []
    total_probe_count = 0

    for asn in asn_list:
        filters = {
            "asn_v4": asn,
            "is_public": "true",
            #"is_anchor": "true",
            "status": 1
        }
        probes = ProbeRequest(**filters)
        probe_ids = [probe["id"] for probe in probes]

        all_probe_ids.extend(probe_ids)
        total_probe_count += probes.total_count

    return all_probe_ids, total_probe_count