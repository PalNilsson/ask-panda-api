"""Streamlit UI for Ask PanDA."""

import os

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Ask PanDA",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "experiment" not in st.session_state:
    st.session_state.experiment = os.getenv("EXPERIMENT", "atlas")


def main() -> None:
    """Main Streamlit application."""
    # Sidebar
    with st.sidebar:
        st.title("🐼 Ask PanDA")
        st.markdown("---")

        # Experiment selection
        experiment = st.selectbox(
            "Select Experiment",
            options=["atlas", "verarubin", "epic"],
            index=["atlas", "verarubin", "epic"].index(st.session_state.experiment),
            format_func=lambda x: {
                "atlas": "ATLAS (CERN LHC)",
                "verarubin": "Vera C. Rubin Observatory",
                "epic": "ePIC (EIC)",
            }[x],
        )
        st.session_state.experiment = experiment

        st.markdown("---")

        # Model settings
        st.subheader("Model Settings")
        model_provider = st.selectbox(
            "Provider",
            options=["openai", "ollama"],
            index=0,
        )

        if model_provider == "openai":
            model_name = st.selectbox(
                "Model",
                options=["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
                index=0,
            )
        else:
            model_name = st.text_input("Model Name", value="llama2")

        st.markdown("---")

        # Quick actions
        st.subheader("Quick Actions")
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        if st.button("📊 Show Job Status"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Show me the status of recent jobs",
            })
            st.rerun()

        if st.button("📚 Search Documentation"):
            st.session_state.messages.append({
                "role": "user",
                "content": "How do I submit a job to PanDA?",
            })
            st.rerun()

    # Main content area
    st.title(f"Ask PanDA - {experiment.upper()}")
    st.markdown(
        f"Ask questions about PanDA workflows for the **{experiment.upper()}** experiment."
    )

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about PanDA..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response (placeholder)
        with st.chat_message("assistant"):
            response = f"I understand you're asking about: **{prompt}**\n\n"
            response += f"This is a placeholder response for the **{experiment.upper()}** experiment. "
            response += "In a full implementation, this would query the Ask PanDA API and provide real information."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
