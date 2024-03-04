class Modulku:
    def __init__(self, df):
        self.df = df

    def create_sum_order_items_df(self):
        sum_order_items_df = self.df.groupby("product_category_name_english")["product_id"].count().reset_index()
        sum_order_items_df.rename(columns={
            "product_id": "product_count"
        }, inplace=True)
        sum_order_items_df = sum_order_items_df.sort_values(by='product_count', ascending=False)

        return sum_order_items_df

    def create_monthly_orders_df(self):
        monthly_orders_df = self.df.resample(rule='M', on='order_purchase_timestamp').agg({
            "order_id": "nunique",
            "total_order": "sum"
        })
        monthly_orders_df = monthly_orders_df.reset_index()
        monthly_orders_df.rename(columns={
            "order_id": "order_count",
            "total_order": "Total Order"
        }, inplace=True)
        
        return monthly_orders_df
    
    def create_bystate_df(self):
        bystate_df = self.df.groupby(by="customer_state").customer_id.nunique().reset_index()
        bystate_df.rename(columns={
            "customer_id": "customer_count"
        }, inplace=True)
        most_common_state = bystate_df.loc[bystate_df['customer_count'].idxmax(), 'customer_state']
        bystate_df = bystate_df.sort_values(by='customer_count', ascending=False)

        return bystate_df, most_common_state
    
    def review_score_df(self):
        review_scores = self.df.groupby('product_category_name_english')['review_score'].mean().reset_index()

        return review_scores
    
    def create_payment_type_df(self):
        bypayment_df = self.df.groupby('payment_type')['total_order'].sum().reset_index()
        total_orders_all = bypayment_df['total_order'].sum()
        bypayment_df['percentage'] = round((bypayment_df['total_order'] / total_orders_all) * 100,1)

        return bypayment_df

class BrazilMapPlotter:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st

    def plot(self):
        brazil = self.mpimg.imread(self.urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'),'jpg')
        ax = self.data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(10,10), alpha=0.3,s=0.3,c='maroon')
        self.plt.axis('off')
        self.plt.imshow(brazil, extent=[-73.98283055, -33.8,-33.75116944,5.4])
        self.st.pyplot()
    
    