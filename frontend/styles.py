custom_css = """
<style>

/* Main app background */
[data-testid="stAppViewContainer"] {
    background-color: #121212 !important;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #1E1E1E !important;
}

/* Top spacing */
.block-container {
    padding-top: 1rem;
}

/* Metric cards */
[data-testid="metric-container"] {
    border: 1px solid #444;
    padding: 10px;
    border-radius: 10px;
    background-color: #121212;
}
input {
    border-radius: 10px !important;
}

</style>
"""