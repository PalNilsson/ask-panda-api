# Streamlit UI for Ask PanDA

This directory contains a Streamlit-based web interface for Ask PanDA.

## Features

- Interactive chat interface for querying PanDA
- Experiment selection (ATLAS, Vera Rubin, ePIC)
- Query history and context
- Real-time streaming responses

## Running the UI

1. Install dependencies:
   ```bash
   pip install -e ".[streamlit]"
   ```

2. Start the Streamlit app:
   ```bash
   streamlit run streamlit-ui/app.py
   ```

3. Open your browser to http://localhost:8501

## Configuration

Set the following environment variables:

- `EXPERIMENT` - Default experiment (atlas, verarubin, epic)
- `OPENAI_API_KEY` - OpenAI API key for LLM queries
- `API_URL` - URL of the Ask PanDA API server (default: http://localhost:8000)

## Screenshots

The UI provides:
- A sidebar for experiment and model selection
- A main chat area for conversations
- Quick action buttons for common queries
