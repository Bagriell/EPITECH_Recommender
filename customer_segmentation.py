"""Client segmentation"""

from rich import print
from rich.panel import Panel

import pandas as pd
import pandas_profiling as pp
import pickle

# MODEL_FP = "./clustering/clustering_model_6_5_final.pkl"
MODEL_FP = (
    "./clustering/sample_clustering_model_6_29_62702944-e436-420e-b43a-e7601c2e5f51.pkl"
)
FAMILIES = [
    "HYGIENE",
    "MAQUILLAGE",
    "SOINS DU VISAGE",
    "SOINS DU CORPS",
    "PARFUMAGE",
    "CAPILLAIRES",
    "SOLAIRES",
]

ORDERED_COLS = [
    "% CAPILLAIRES",
    "% HYGIENE",
    "% MAQUILLAGE",
    "% PARFUMAGE",
    "% SOINS DU CORPS",
    "% SOINS DU VISAGE",
    "% SOLAIRES",
]

CLUSTER_DESC = {
    "0": """- hight interest in 'soin-corps' products
- no interest in 'capillaire' and 'parfum'
- average total sales
""",
    "1": """- hight interest in 'maquillage' and 'solaire' products
- no interest in 'capillaire' and 'parfum'
- average total sales
""",
    "2": """- hight interest in 'hygiene' products
- moderated interest on 'solaire' products
- no interest for the rest
- total sales very low
""",
    "3": """- hight interest in 'soin visage' products
- moderate interest for 'solaire'
- no interest for the rest
- slightly above average total sales
""",
    "4": """- hight interest in 'capillaire' products
- moderate interest for 'solaire' products
- no interest for the rest
- below average total sales
""",
    "5": """- hight interest in 'parfum' products
- no interest in 'capillaire'
- very low interest for the rest
- total sales very hight 
""",
}

model = pickle.load(open(MODEL_FP, "rb"))


def clean():
    """Remove MULTI FAMILLE and SANTE NATRUELLE"""
    # mask = ~df["FAMILLE"].isin(["MULTI FAMILLES","SANTE NATURELLE"])
    ...


def get_cluster_description(cluster_id):
    return CLUSTER_DESC[str(cluster_id)]


def pipeline(df_cli: pd.DataFrame) -> pd.DataFrame:
    """Normalize user transaction data to feature data usable by our clustering model.

    Args:
        data (pd.DataFrame): the user transactions.

    Returns:
        pd.DataFrame: user normalized data.
    """
    df_grouped = df_cli.groupby(["CLI_ID", "FAMILLE"])
    df_sales = df_grouped["PRIX_NET"].sum().reset_index()
    df_pivot = df_sales.pivot(index="CLI_ID", columns="FAMILLE", values="PRIX_NET")
    df_pct = df_pivot.div(df_pivot.sum(axis=1), axis=0).mul(100)
    df_pct.fillna(0, inplace=True)
    df_pct.columns = [f"% {col_name}" for col_name in df_pct.columns]

    for family in FAMILIES:
        if family not in [column_name[2:] for column_name in df_pct.columns.to_list()]:
            df_pct[f"% {family}"] = 0
    df_pct = df_pct[ORDERED_COLS]
    return df_pct


def get_client_profile(customer_data: pd.DataFrame) -> pd.DataFrame:
    print(Panel("Client profile"))

    # print("""
    # profile:
    #     - highest values tendency, exceptionnally hight spentin family ...
    # type of client:
    #     - way of buying things
    # Behaviour:
    #     - occurences
    # """)
    if customer_data.empty:
        raise ValueError("Customer data is empty.")
    features = pipeline(customer_data)
    label = model.predict(features)
    features["Cluster"] = pd.Series(label, index=features.index)
    print(f"Cluster: {label[0]}")
    print(f"Profile: {get_cluster_description(label[0])}")
    return features
