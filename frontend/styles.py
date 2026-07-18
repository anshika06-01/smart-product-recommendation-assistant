custom_css = """
<style>

/* Main Background */
[data-testid="stAppViewContainer"] {
    background: #0F172A;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1E293B;
}

/* Main Content Padding */
.block-container {
    padding-top: 1rem;
}

/* Metric Cards */


[data-testid="metric-container"] {
    background: #1E293B;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #334155;
}

/* Product Cards */
div[data-testid="stVerticalBlock"] div:has(> div[data-testid="stVerticalBlock"]) {
    border-radius: 12px;
}

/* Input Boxes */
input {
    border-radius: 10px !important;
}

.stTextInput input {
    border: 2px solid #3B82F6;
    border-radius: 12px;
}

.card {
    background: #1E293B;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #334155;
}

</style>
"""