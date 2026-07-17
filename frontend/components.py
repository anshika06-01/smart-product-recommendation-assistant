import streamlit as st

def product_card(product):

    with st.container(border=True):

        st.subheader(
            product["product_name"]
        )

        st.caption(
            product["brand"]
        )

        st.write(
            f"💰 ₹{product['price']}"
        )

        st.write(
            f"⭐ {product['rating']}"
        )

        st.write(
            f"📦 {product['stock_status']}"
        )