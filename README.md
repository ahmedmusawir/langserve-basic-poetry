# Langserve Example Setup

This repository contains an example setup for Langserve using Python 3.11.x. Follow the steps below to get started.

## Prerequisites

- Python 3.11.x

## Installation Steps

### Step 1: Create Project Directory

```
mkdir example-langserve
cd example-langserve
```

### Step 2: Create .env File

Create a .env file in the project root directory with your OpenAI API key:

`OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"`

### Step 3: Set Up Virtual Environment

Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate

```

### Step 4: Install Initial Dependencies

Upgrade pip and install the initial dependencies:

`pip install -U pip langchain-cli poetry langchain`

### Step 5: Create Langserve Application

Create a new Langserve application:

`langchain app new . `

### Step 6: Verify Project Structure

Verify the project structure:

`tree -L 2`

You should see something like this:

```
.
├── app/
│   ├── __init__.py
│   ├── __pycache__/
│   │   └── . . .
│   └── server.py
├── Dockerfile
├── packages/
│   └── README.md
├── pyproject.toml
├── README.md
└── venv/
    └── . . .
```

### Step 7: Update pyproject.toml

Add the following line under `[tool.poetry.dependencies]` in your pyproject.toml file:

`pydantic = ">=2.7.4,<3.0.0"`

### Step 8: Add Required Packages

Add the required packages using poetry:

`poetry add "langserve[all]" langchain-openai python-decouple`

### Step 9: Update `server.py`

Update the /app/server.py file with the following content:

```
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from decouple import config
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

app = FastAPI()

# CORS middleware configuration
origins = [
    "http://localhost:4001",  # Add your frontend URL here
    "http://127.0.0.1:4001",
    "http://localhost:8501",
    "http://127.0.0.1:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creating the Doc route
@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# ------------- DEFAULT AI ROUTE START ----------------

model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"))
prompt = ChatPromptTemplate.from_template("Give me a summary about {topic} in a paragraph or less.")
chain = prompt | model
add_routes(app, chain, path="/openai")

# ------------- DEFAULT AI ROUTE ENDS ----------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

### Step 10: Start the Server

Start the Langserve server:

`langchain serve`

### Successful Installation should look like this:

```
(venv) moose@cyberize1:/mnt/c/PYTHON/2-langserve-basic-poetry$ langchain serve
INFO:     Will watch for changes in these directories: ['/mnt/c/PYTHON/2-langserve-basic-poetry']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [17148] using StatReload
INFO:     Started server process [17152]
INFO:     Waiting for application startup.

 __          ___      .__   __.   _______      _______. _______ .______     ____    ____  _______
|  |        /   \     |  \ |  |  /  _____|    /       ||   ____||   _  \    \   \  /   / |   ____|
|  |       /  ^  \    |   \|  | |  |  __     |   (----`|  |__   |  |_)  |    \   \/   /  |  |__
|  |      /  /_\  \   |  . `  | |  | |_ |     \   \    |   __|  |      /      \      /   |   __|
|  `----./  _____  \  |  |\   | |  |__| | .----)   |   |  |____ |  |\  \----.  \    /    |  |____
|_______/__/     \__\ |__| \__|  \______| |_______/    |_______|| _| `._____|   \__/     |_______|

LANGSERVE: Playground for chain "/openai/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /openai/playground/
LANGSERVE:
LANGSERVE: See all available routes at /docs/

LANGSERVE: ⚠️ Using pydantic 2.8.2. OpenAPI docs for invoke, batch, stream, stream_log endpoints will not be generated. API endpoints and playground should work as expected. If you need to see the docs, you can downgrade to pydantic 1. For example, `pip install pydantic==1.10.13`. See https://github.com/tiangolo/fastapi/issues/10360 for details.

INFO:     Application startup complete.
```

## Important Endpoints

```
INFO:     127.0.0.1:49969 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:49969 - "GET /openapi/playground HTTP/1.1" 200 OK
INFO:     127.0.0.1:50092 - "POST /openai/invoke HTTP/1.1" 200 OK
INFO:     127.0.0.1:50226 - "POST /openai/stream HTTP/1.1" 200 OK
```
