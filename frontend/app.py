import streamlit as st
import pandas as pd
import time
from components import product_card
from styles import custom_css

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛒",
    layout="wide"
)
st.markdown(
    custom_css,
    unsafe_allow_html=True
)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []



# ---------------------------------
# LOAD DATA
# ---------------------------------

df = pd.read_csv(
    r"C:\Users\Dell\Downloads\ecommerce_products_killer.csv"
)

# ---------------------------------
# SESSION STATE
# ---------------------------------

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

# ---------------------------------
# TITLE
# ---------------------------------

st.title("🛒 ShopSense AI")
st.info("""
👋 Welcome to ShopSense AI

Try asking:
• Best phone under ₹30000
• Running shoes for men
• Smartwatch with fitness tracking
• Budget laptop for coding
""")
st.caption(
    "Your Intelligent Shopping Companion"
)

# ---------------------------------
# CHAT INTERFACE
# ---------------------------------

st.subheader("💬 AI Shopping Assistant")

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# User input
user_query = st.chat_input(
    "Describe what you're looking for..."
)

if user_query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.spinner(
        "Searching products..."
    ):

        time.sleep(2)

        ai_response = f"""
Based on your requirements:

**{user_query}**

I found some products that may match your needs.

(Temporary response - backend integration pending)
"""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

    st.rerun()

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.header("Filters")

# Category

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["category"].unique())
)

if category != "All":
    df = df[df["category"] == category]

# Brand

brand = st.sidebar.selectbox(
    "Brand",
    ["All"] + sorted(df["brand"].unique())
)

if brand != "All":
    df = df[df["brand"] == brand]

# Price

min_price = int(df["price"].min())
max_price = int(df["price"].max())

price_range = st.sidebar.slider(
    "Price Range",
    min_price,
    max_price,
    (min_price, max_price)
)

df = df[
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]

# Rating

rating = st.sidebar.slider(
    "Minimum Rating",
    0.0,
    5.0,
    3.0
)

df = df[df["rating"] >= rating]

# ---------------------------------
# SEARCH
# ---------------------------------

query = st.text_input(
    "🔍 Search Products"
)

if query:

    df = df[
        df["product_name"]
        .str.contains(
            query,
            case=False,
            na=False
        )
    ]

# ---------------------------------
# WISHLIST
# ---------------------------------

st.sidebar.subheader("❤️ Wishlist")

for item in st.session_state.wishlist:
    st.sidebar.write(item)

# ---------------------------------
# METRICS
# ---------------------------------

if len(df) > 0:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Products Found",
        len(df)
    )

    col2.metric(
        "Average Rating",
        round(df["rating"].mean(), 2)
    )

    col3.metric(
        "Average Price",
        f"₹{int(df['price'].mean())}"
    )

# ---------------------------------
# EMPTY RESULT
# ---------------------------------

if len(df) == 0:

    st.warning(
        "No products found. Try different filters."
    )

    st.stop()

# ---------------------------------
# TABS
# ---------------------------------
st.subheader("🤖 AI Recommendation Center")

st.success(
    "Ask natural language queries and receive personalized product recommendations."
)

tab1, tab2, tab3 = st.tabs(
    [
        "🛍 Products",
        "⚖ Compare",
        "🔥 Recommendations"
    ]
)

# =================================
# PRODUCTS TAB
# =================================

with tab1:

    st.subheader(
        f"Showing {len(df)} Products"
    )

    products = df.head(12)

    for i in range(0, len(products), 3):

        cols = st.columns(3)

        for j in range(3):

            if i + j < len(products):

                product = products.iloc[i + j]

                with cols[j]:

                    with st.container(border=True):

                        st.subheader(
                            product["product_name"]
                        )

                        st.caption(
                            product["brand"]
                        )

                        st.write(
                            f"📂 Category: {product['category']}"
                        )

                        st.write(
                            f"💰 Price: ₹{product['price']}"
                        )

                        st.write(
                            f"⭐ Rating: {product['rating']}"
                        )

                        st.write(
                            f"📦 {product['stock_status']}"
                        )

                        if st.button(
                            "❤️ Add to Wishlist",
                            key=f"wish_{i}_{j}"
                        ):

                            if product["product_name"] not in st.session_state.wishlist:

                                st.session_state.wishlist.append(
                                    product["product_name"]
                                )

                        with st.expander(
                            "View Details"
                        ):

                            st.write(
                                product["description"]
                            )

# =================================
# COMPARE TAB
# =================================

with tab2:

    st.subheader(
        "Compare Products"
    )

    compare_products = st.multiselect(
        "Select Products",
        df["product_name"].unique()
    )

    if len(compare_products) >= 2:

        comparison_df = df[
            df["product_name"]
            .isin(compare_products)
        ][
            [
                "product_name",
                "brand",
                "category",
                "price",
                "rating",
                "stock_status"
            ]
        ]

        st.dataframe(
            comparison_df,
            use_container_width=True
        )

        csv = comparison_df.to_csv(
            index=False
        )

        st.download_button(
            "📥 Download Comparison",
            csv,
            "comparison.csv",
            "text/csv"
        )

    else:

        st.info(
            "Select at least 2 products."
        )

# =================================
# RECOMMENDATIONS TAB
# =================================

with tab3:

    st.subheader("🔥 Recommended For You")

    recommended = (
        df.sort_values(
            by=["rating", "reviews_count"],
            ascending=False
        )
        .head(6)
    )

    cols = st.columns(3)

    for idx, (_, product) in enumerate(
        recommended.iterrows()
    ):

        with cols[idx % 3]:

            with st.container(border=True):

                st.subheader(
                    product["product_name"]
                )

                st.write(
                    f"🏷️ {product['brand']}"
                )

                st.write(
                    f"💰 ₹{product['price']}"
                )

                st.write(
                    f"⭐ {product['rating']}"
                )

                st.write(
                    f"📂 {product['category']}"
                )