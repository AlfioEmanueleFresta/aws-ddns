#!/usr/bin/env python3

from datetime import datetime
from dns import resolver
from pathlib import Path

import boto3
import configparser
import requests


DNS_RESOLVERS = ["1.1.1.1", "8.8.8.8"]
CHECKIP4_URL = "https://checkip.amazonaws.com"


def get_a(hostname):
    r = resolver.Resolver()
    r.nameservers = DNS_RESOLVERS
    try:
        names = r.resolve(hostname, "A")
        return str(names[0]).strip()
    except resolver.NXDOMAIN:
        return None


def get_ipv4():
    r = requests.get(CHECKIP4_URL)
    if r.status_code != requests.codes.ok:
        raise ValueError("Unexpected response code: %s" % (r.status_code,))
    return r.text.strip()


def update(hostname, profile, zone_id, ttl, new_ipv4):
    session = boto3.Session(profile_name=profile)
    client = session.client("route53")
    response = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Comment': "Updating %s to %s" % (hostname, new_ipv4),
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': hostname,
                        'Type': 'A',
                        'TTL': ttl,
                        'ResourceRecords': [
                            {
                                'Value': new_ipv4,
                            }
                        ]
                    }
                }
            ]
        }
    )
    return response


def main():
    print("Started at:", datetime.now().isoformat())

    new_ipv4 = get_ipv4()
    print("IPv4:", new_ipv4)
    print("", flush=True)

    config_path = Path(__file__).parent / "config.ini"
    config = configparser.ConfigParser()
    config.read(config_path)

    for hostname in config.sections():
        profile = config[hostname]["Profile"]
        zone_id = config[hostname]["HostedZoneID"]
        ttl = int(config[hostname]["TTL"])

        current_ipv4 = get_a(hostname)
        is_updated = current_ipv4 == new_ipv4
        print(hostname, "has IPv4", current_ipv4)

        if is_updated:
            print(hostname, "is up-to-date.")

        else:
            print(hostname, "Updating to new IPv4:", new_ipv4)
            response = update(hostname, profile, zone_id, ttl, new_ipv4)
            print(hostname, "Response:", response)

        print("", flush=True)


if __name__ == "__main__":
    main()
