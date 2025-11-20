# Applied-ML-LLM-Exercise

A project for query classification and reformulation using LLMs (OpenAI or Ollama).

## Installation

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- Make (usually pre-installed on Unix systems)

### Setup

1. Install Poetry if you haven't already:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:

   ```bash
   make install-dev
   ```

   Or using Poetry directly:

   ```bash
   poetry install
   ```

3. Activate the Poetry virtual environment (optional):

   ```bash
   poetry shell
   ```

## Configuration

1. Copy the example environment file to create your `.env` file:

   ```bash
   cp .env.example .env
   ```

2. Open the `.env` file and fill in your actual configuration values.

### For OpenAI:

Edit your `.env` file and set:

```bash
MODEL_TYPE=openai
OPENAI_API_KEY=your-actual-api-key-here
MODEL_NAME=gpt-4o-mini
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

### For Ollama:

1. First, pull the model you want to use by running in your terminal:

   ```bash
   ollama pull <model-name>
   ```

   For example:

   ```bash
   ollama pull gemma3:4b
   ```

2. Then, edit your `.env` file and set (use the same model name you pulled):

   ```bash
   MODEL_TYPE=ollama
   OLLAMA_URL=http://localhost:11434/v1
   OLLAMA_API_KEY=ollama
   MODEL_NAME=<model-name>
   ```

   Example:

   ```bash
   MODEL_TYPE=ollama
   OLLAMA_URL=http://localhost:11434/v1
   OLLAMA_API_KEY=ollama
   MODEL_NAME=gemma3:4b
   ```

   **Note:** Make sure Ollama is running on your local machine before using it.

See `.env.example` for a complete list of all available configuration options with detailed comments.

## Usage

### Quick Start with Make

The easiest way to run the app is using the Makefile:

```bash
make run
```

This will start the Streamlit web application. The app will open in your browser automatically.

### Available Make Commands

- `make run` - Run the Streamlit app
- `make install` - Install production dependencies
- `make install-dev` - Install all dependencies (including dev dependencies)
- `make clean` - Clean Poetry cache
- `make help` - Show all available commands

### Streamlit Web App (Recommended)

Run the Streamlit web application:

```bash
make run
```

Or using Poetry directly:

```bash
poetry run streamlit run main.py
```

The app will open in your browser. Features:

- View initial dataframe with queries and product titles
- Click "Evaluate" button to run classification on all rows
- View results with 4 columns: query, product_title, classification, reformulated_query
- Download results as CSV
- View classification statistics
- Progress bar at the top for better visibility during processing

### Command Line

Run the main script:

```bash
poetry run python main.py
```

### Jupyter Notebook

Use in a Jupyter notebook:

```bash
poetry run jupyter notebook
```

## Project Structure

```
.
├── data/                          # Data files (csv format)
├── llm_prompt/                    # LLM prompt templates
│   ├── classification_prompt.txt
│   └── query_modification_prompt.txt
├── utils/                         # Utility modules
│   ├── data_client.py            # Data loading and preprocessing
│   ├── llm_client.py             # LLM client wrapper
│   ├── openai_client.py          # OpenAI API client
│   └── model.py                  # Data models
├── .env.example                   # Example environment configuration file
├── main.py                        # Main Streamlit application
├── Makefile                       # Make commands for easy usage
├── pyproject.toml                # Poetry configuration
└── test.ipynb                     # Jupyter notebook for testing
```

## Dependencies

- `pandas`: Data manipulation
- `pyarrow`: Parquet file support
- `openai`: OpenAI API client
- `pydantic`: Data validation
- `python-dotenv`: Environment variable management
- `numpy`: Numerical operations
- `streamlit`: Web application framework

## Limitation

Reading the product parque file from github throws error. That is why the files were downloaded, merged, filtered to get the final working dataset. Finally, it is saved in the data folder, so that the application can read it from there.

## AI solution design

- The problem is divided into two parts. First part is to classify whether the labeling is accurate or not based on query and product title. The second part is to reqrite the query when it is not accurate.

- The reason of doing it in two different llm call is to improve the accuracy. The first call classify and provides the reasoning for the classification. The second call use that reasoning to reformulate the query. This way it increase the overall accuracy instead of doing it in one call.

- Agentic apporach is not used as the problem doesn't require tool calling approach.

- OpenAI api calling approach is used because it supports both the openai model and ollama model, as part of the requirement is also to use open source llm from the local machine. Ollama is compatiable to openai chat completion api but it doesn't support some of the capabilites such as structured output, temperature and max_token.

- Seperate system prompts are used for two different part of the problem to provide clear and concise directions to the llm.
- Prompts are tested using different size LLMs to optimize as much as possible.
- In LLM calls, no message history is passe becasue each row of the data is independent from other rows. In addition, the problem doesn't require a chat experience which require past information to make the chat experience more natural. This problem doesn't require that functionality.

## System Design

- There is light streamlit UI to display the result.
- The UI will show the default table with ids , query and product title
- Product title is used for product description becasue the other columns in the product table has high number of n/a values
- When user will click the evaluate button, the app will execute the llm calls for both calssification and reformulation task.
- The final output will be displayed when the LLM process is completed
- No backend api is designed to use from the frontend, just to keep the architecture simple for the case study.
- The application can use both openai's GPT models and also OLLAMA's open source model based on what user adds in the env file
