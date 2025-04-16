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


# Query all Probes for Amazon Asns.
# Finds 61 Probes as Connected & Public. Only 1 is an Anchor. 
def get_amazon_probes():

    amazon_asns = [
        "14618", "135630", "10124", "8987", "38895", "9059", 
        "19047", "17493", "39111", "395343", "7224", "58588", "16509"
    ]

    all_probe_ids = []
    total_probe_count = 0

    for asn in amazon_asns:
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
