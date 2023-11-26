"""Scripts that extract analyze KaDo.csv transactional data and build transaction_items.csv and exploratory analysis report."""

# %% [markdown]
# # transaction items dataset builder
# 
# We want to build the dataset we will use in order to give people the recommended product.  
# We also analyse and clean data.

# %% [markdown]
# Read data

# %%
import pandas as pd
import numpy as np

import seaborn as sns
from pandas_profiling import ProfileReport
import plotly.express as px


df = pd.read_csv("../KaDo.csv")
df

# %% [markdown]
# Check the following:
# - amilly analysis
# - na values
# - null values

# %%
px.histogram(df, y="FAMILLE", title="before cleaning").update_yaxes(categoryorder="total ascending")

# %%
print(f"""
shape: {df.shape}
na: {df.isna().sum().sum()}
null: {df.isnull().sum().sum()}
dropped: {len(df[df["FAMILLE"].isin(["MULTI FAMILLES", "SANTE NATURELLE"])])}
""")

mask = ~df["FAMILLE"].isin(["MULTI FAMILLES","SANTE NATURELLE"])
df = df[mask]
px.histogram(df, y="FAMILLE", title="after cleaning").update_yaxes(categoryorder="total ascending")

# %% [markdown]
# g et each product as index and its associated FAMILLE/MAILLE/UNIVERS.

# %%
obj_df = df.groupby('LIBELLE').agg({
    'FAMILLE': lambda x: x.value_counts().index[0],
    'MAILLE': lambda x: x.value_counts().index[0],
    'UNIVERS': lambda x: x.value_counts().index[0]
}).reset_index()

obj_df.set_index('LIBELLE', inplace=True)
obj_df

# %% [markdown]
# get median price for each product because we have a lot of weird prices and hight variance.

# %%
obj_df['PRIX_NET_MEDIAN'] = df.groupby('LIBELLE')['PRIX_NET'].median()
obj_df

# %%
px.histogram(df, y="FAMILLE")

# %%
sns.histplot(obj_df['PRIX_NET_MEDIAN'], kde=True)

# %%
obj_df[["MAILLE", "UNIVERS", "FAMILLE"]].describe()

# %% [markdown]
# ## Profiling report
# 
# The idea is to analyse the variables and their relations through metrics.
# 

# %%
profile = ProfileReport(
    obj_df,
    orange_mode=True,
    sortby="PRIX_NET_MEDIAN",
    title="transaction items report"
)
profile.to_file("transaction_items_eda_report.html")
obj_df.to_csv("transaction_items.csv")


