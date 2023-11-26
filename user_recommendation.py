"""
Software entrypoint

This programm takes a client id and gives
1. statistical description of the client
2. client segmentation analysis
3. a recommended gift product

Usage: `python main.py client_id`
"""

import argparse

from customer_segmentation import get_client_profile
from recommender import get_client_recommendations
from stats import get_client_stats


def main(client_id: int):
    customer_data = get_client_stats(client_id=client_id)
    clustered = get_client_profile(customer_data=customer_data)
    get_client_recommendations(cluster=clustered["Cluster"].values[0], cust_data=customer_data, client_id=client_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="the client id we want to analyze.", type=int)
    args = parser.parse_args()

    main(args.client_id)
