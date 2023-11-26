"""
Recommender system module
"""

from rich import print
from rich.panel import Panel
import pandas as pd

LABELLED_DATA_FP = "./data/df_labelled_final_62702944-e436-420e-b43a-e7601c2e5f51.csv"


def get_recommended_product(customer_product: list, customers_products: dict) -> str:
    """return the most popular product not bought by customer"""

    for product in customer_product:
        if product in customers_products.keys():
            customers_products.pop(product, None)
    return next(iter(customers_products))


def get_products_by_popularity(df: pd.DataFrame) -> dict:
    """Return the different product and their popularity."""
    return df["LIBELLE"].value_counts().to_dict()


# get most famous product in the cluster that client not bought
def get_client_recommendations(cluster: int, cust_data: pd.DataFrame, client_id: int):
    print(Panel("Recommendation"))
    # get transactions labelled
    df_merged = pd.read_csv(LABELLED_DATA_FP)

    # get customer product list
    customer_product = get_products_by_popularity(cust_data)
    customer_product = list(customer_product.keys())
    # get customers products within cluster
    df_merged_cluster = df_merged.query(
        f"Cluster == {cluster} and CLI_ID != {client_id}"
    )
    cluster_customers_products = get_products_by_popularity(df_merged_cluster)
    recommended = get_recommended_product(customer_product, cluster_customers_products)
    print(
        f"""recommended 🎁 for client {client_id} is: [green1]{recommended}[/green1].
This is the most popular product from similar customer."""
    )
