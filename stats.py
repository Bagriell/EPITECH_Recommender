"""
Statistics module
"""

from rich import print
from rich.panel import Panel
import pandas as pd
from pydantic import BaseModel
import pandas_profiling as pp
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


class ClientStats(BaseModel):
    # overall
    total_spent: float
    std_spent: float

    # By transactions
    nb_transaction: int
    average_spent_by_transaction: float
    max_spent_by_transaction: float
    min_spent_by_transaction: float

    # By products
    nb_product: int
    nb_distinct_product: int
    average_spent_by_product: float
    most_expansive_product: float
    less_expansive_product: float
    products_vcounts: dict
    spent_by_family: dict
    spent_by_maille: dict
    spent_by_univers: dict


def get_client_stats(client_id: int):
    """
    Statistical descrption of client.
    """
    print(Panel("📈 Statistics"))

    df = pd.read_csv("./data/KaDo.csv")
    client_transactions = df[df["CLI_ID"] == client_id]
    if client_transactions.empty:
        raise ValueError("Can't find client corresponding to this id.")

    stats = ClientStats(
        # overall
        total_spent=client_transactions["PRIX_NET"].sum(),
        std_spent=client_transactions["PRIX_NET"].std(),
        # transactions
        nb_transaction=client_transactions["TICKET_ID"].nunique(),
        average_spent_by_transaction=client_transactions.groupby(["TICKET_ID"])[
            "PRIX_NET"
        ].sum().mean(),
        max_spent_by_transaction=client_transactions.groupby(["TICKET_ID"])["PRIX_NET"]
        .sum()
        .max(),
        min_spent_by_transaction=client_transactions.groupby(["TICKET_ID"])["PRIX_NET"]
        .sum()
        .min(),
        # products
        nb_product=len(client_transactions),
        nb_distinct_product=client_transactions["LIBELLE"].nunique(),
        average_spent_by_product=client_transactions["PRIX_NET"].mean(),
        most_expansive_product=client_transactions["PRIX_NET"].max(),
        less_expansive_product=client_transactions["PRIX_NET"].min(),
        products_vcounts=client_transactions["LIBELLE"].value_counts().to_dict(),
        spent_by_family=client_transactions.groupby(["FAMILLE"])["PRIX_NET"]
        .sum()
        .to_dict(),
        spent_by_maille=client_transactions.groupby(["MAILLE"])["PRIX_NET"]
        .sum()
        .to_dict(),
        spent_by_univers=client_transactions.groupby(["UNIVERS"])["PRIX_NET"]
        .sum()
        .to_dict(),
    )

    # create profile report and save it as html
    profile = pp.ProfileReport(
        client_transactions,
        title=f"Client {client_id} statistical analysis.",
        dark_mode=True,
        progress_bar=False,
    )
    profile.to_file(f"{client_id}_eda.html")

    print(stats)
    return client_transactions
