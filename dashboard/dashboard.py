import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from func import DataAnalyzer, BrazilMapPlotter


sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("all_data.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv('geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    st.sidebar.header("Aurelly Joeandani")
    #st.sidebar.image("URL_GAMBAR_PROFIL", width=100, use_column_width='auto')  
    st.sidebar.write("Email: aurellyjoean@gmail.com")  
    st.sidebar.write("Linkedin: https://www.linkedin.com/in/aurelly/")

    

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

monthly_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()
bypayment_df = function.create_payment_type()

# Mendifinisikan Streamlit app
st.title("E-Commerce Public Data Analysis Dashboard")

# Add text or descriptions
st.write("**This is a dashboard for submission final project analyzing E-Commerce public data at Dicoding.**")

# Order Items
st.subheader("Best and Worst Performing Product")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Average Items: **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.head(5), palette="magma", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=80)
ax[0].set_title("Best Performing Products", loc="center", fontsize=90)
ax[0].tick_params(axis ='y', labelsize=55)
ax[0].tick_params(axis ='x', labelsize=50)

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5), palette="magma", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=80)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing products", loc="center", fontsize=90)
ax[1].tick_params(axis='y', labelsize=55)
ax[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig)

# Customer Demographic
st.subheader("Customer Demographic")
tab1, tab2 = st.tabs(["Geolocation", "State"])

with tab1:
    map_plot.plot()

    with st.expander("See Explanation"):
        st.write('It can be seen from the distribution of customers above that many customers come from the southern and southeastern parts of Brazil. Other information, there are more customers in cities that are capitals (São Paulo, Rio de Janeiro, Porto Alegre, and others).')

with tab2:
    most_common_state = state.customer_state.value_counts().index[0]
    st.markdown(f"Most Common State: **{most_common_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=state.customer_state.value_counts().index,
                y=state.customer_count.values, 
                data=state,
                palette="magma"
                    )

    plt.title("Number of customers by State", fontsize=15)
    plt.xlabel("State")
    plt.ylabel("Number of Customers")
    plt.xticks(fontsize=12)
    st.pyplot(fig)

# sales performance trends
st.subheader("Sales Performance Trends")

fig, ax = plt.subplots(figsize=(12, 6))
plt.plot(
    monthly_orders_df["order_approved_at"],
    monthly_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)

# Temukan indeks dari nilai tertinggi
max_index = monthly_orders_df["order_count"].idxmax()

# Tambahkan marker atau garis pada titik tertinggi
plt.scatter(
    monthly_orders_df["order_approved_at"].iloc[max_index],
    monthly_orders_df["order_count"].iloc[max_index],
    color='red',  # Warna markah peningkatan tertinggi
    s=100,  # Ukuran markah
    zorder=5,  # Layer tertinggi untuk menampilkan di atas plot
    linewidth=2,
    label='Highest Increase'
)

plt.title("Order Performance per Month (Sept 2016 - Aug 2018)", loc="center", fontsize=20)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)

# Menambahkan legenda
plt.legend()
st.pyplot(fig)

# Customer Spend Money
st.subheader("Customer Spend Money")
col1, col2 = st.columns(2)

with col1:
    total_spend = sum_spend_df["total_spend"].sum()
    st.markdown(f"Total Spend: **{total_spend}**")

with col2:
    avg_spend = sum_spend_df["total_spend"].mean()
    st.markdown(f"Average Spend: **{avg_spend}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=sum_spend_df,
    x="order_approved_at",
    y="total_spend",
    marker="o",
    linewidth=2,
    color="#90CAF9"
)

ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)


# Review Score
st.subheader("Review Score")
col1, col2 = st.columns(2)

with col1:
    avg_review_score = review_score.mean()
    st.markdown(f"Average Review Score: **{avg_review_score:.2f}**")

with col2:
    most_common_review_score = review_score.value_counts().idxmax()
    st.markdown(f"Most Common Review Score: **{most_common_review_score}**")

fig, ax = plt.subplots(figsize=(12, 6))
colors = sns.color_palette("viridis", len(review_score))

sns.barplot(x=review_score.index,
            y=review_score.values,
            order=review_score.index,
            palette=colors)

plt.title("Customer Review Scores for Service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Menambahkan label di atas setiap bar
for i, v in enumerate(review_score.values):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12, color='black')

st.pyplot(fig)

st.caption('Copyright (C) Aurelly Joeandani 2024')
