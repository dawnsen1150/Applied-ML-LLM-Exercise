import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from utils.data_client import preprocess_data
from utils.llm_client import LLMClient

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Label Classification and Query Reformulation App",
    page_icon="🔍",
    layout="wide",
)

# Initialize session state
if "df_results" not in st.session_state:
    st.session_state.df_results = None
if "is_evaluated" not in st.session_state:
    st.session_state.is_evaluated = False

# Title
st.title("Label Classification and Query Reformulation App")
st.markdown(
    "Classify queries as Accurate or Inaccurate, and reformulate inaccurate queries based on product titles"
)

# Progress bar placeholders at the top for better visibility
progress_placeholder = st.empty()
status_placeholder = st.empty()


# Load data
@st.cache_data
def load_initial_data():
    """Load and cache the initial preprocessed data"""
    return preprocess_data()


# Load initial dataframe
df_initial = load_initial_data()

# Sidebar
with st.sidebar:
    st.header("Data Info")
    st.write(f"**Total rows:** {len(df_initial)}")
    st.write(f"**Columns:** {', '.join(df_initial.columns.tolist())}")

    st.header("Actions")
    evaluate_button = st.button("Evaluate", type="primary", use_container_width=True)

    if st.button("Reset", use_container_width=True):
        st.session_state.df_results = None
        st.session_state.is_evaluated = False
        st.rerun()

# Main content area
if not st.session_state.is_evaluated:
    # Show initial dataframe
    st.header("Initial Data")
    st.dataframe(df_initial, use_container_width=True, hide_index=True)

    st.info(
        "Click the **Evaluate** button in the sidebar to run classification on all rows."
    )

    # Run classification when button is clicked
    if evaluate_button:
        # Display progress bar at the top for better visibility
        with progress_placeholder.container():
            st.info("🔄 Running classification... This may take a while.")
            progress_bar = st.progress(0)

        llm_client = LLMClient()

        # Initialize results dataframe
        df_results = df_initial.copy()
        df_results["classification"] = ""
        df_results["reasoning"] = ""
        df_results["reformulated_query"] = ""

        # Process each row
        total_rows = len(df_results)
        for idx, row in df_results.iterrows():
            try:
                classification, reasoning = llm_client.classify(
                    row["query"], row["product_title"]
                )
                df_results.at[idx, "classification"] = classification
                df_results.at[idx, "reasoning"] = reasoning
                if classification == "Inaccurate":
                    df_results.at[idx, "reformulated_query"] = llm_client.reformulation(
                        row["query"], row["product_title"], reasoning
                    )
            except Exception as e:
                st.error(f"Error processing row {idx + 1}: {str(e)}")
                df_results.at[idx, "classification"] = "Error"
                df_results.at[idx, "reasoning"] = str(e)
                df_results.at[idx, "reformulated_query"] = ""
                continue

            # Update progress
            progress = (idx + 1) / total_rows
            progress_bar.progress(progress)
            status_placeholder.text(f"Processing row {idx + 1} of {total_rows}...")

        # Store results in session state
        st.session_state.df_results = df_results
        st.session_state.is_evaluated = True

        # Clear progress indicators
        progress_placeholder.empty()
        status_placeholder.empty()

        st.rerun()

else:
    # Show results
    st.header("Classification Results")

    df_results = st.session_state.df_results

    # Display the full results with 4 columns
    st.dataframe(
        df_results[["query", "product_title", "classification", "reformulated_query"]],
        use_container_width=True,
        hide_index=True,
    )

    # Show statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", len(df_results))

    with col2:
        accurate_count = len(df_results[df_results["classification"] == "Accurate"])
        st.metric("Accurate", accurate_count)

    with col3:
        inaccurate_count = len(df_results[df_results["classification"] == "Inaccurate"])
        st.metric("Inaccurate", inaccurate_count)

    # Download button
    csv = df_results.to_csv(index=False)
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="classification_results.csv",
        mime="text/csv",
    )
