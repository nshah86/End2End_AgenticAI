# End2End AgenticAI

A Python project implementing end-to-end AI agent functionality using LangChain and related technologies.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy the `.env.example` file to a new file named `.env`
   - Add your API keys and configuration to the `.env` file
```bash
# Windows
copy .env.example .env

# Unix/MacOS
cp .env.example .env
```

## Running the Application

To start the application, run:
```bash
streamlit run src/langraphAgenticAI/main.py
```

## Project Structure

- `requirements.txt`: Project dependencies
- `.env`: Environment variables (API keys, configuration) - not committed to Git
- `venv/`: Python virtual environment (ignored by git)
- `src/langraphAgenticAI/`: Main application code
  - `LLMS/`: LLM providers (Groq, OpenAI, Anthropic)
  - `graph/`: LangGraph implementation
  - `nodes/`: Graph nodes for processing
  - `state/`: State management for the graph
  - `ui/`: User interface components
  - `utils/`: Utility functions
  - `main.py`: Application entry point

## Technologies Used

- LangChain
- LangGraph
- FAISS
- Streamlit
- Other dependencies as listed in requirements.txt