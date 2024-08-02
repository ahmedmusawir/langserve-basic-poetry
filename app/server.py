from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from decouple import config
import os

# Import the function from contact.py
from contact import get_contacts
from ghl_contacts import get_ghl_contacts

# Enable tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = config("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = config("LANGCHAIN_PROJECT")


app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# New endpoint to get contacts
@app.get("/contacts")
async def get_all_contacts():
    contacts = await get_contacts()
    return {"contacts": contacts}

# New endpoint to get contacts
@app.get("/ghl-contacts")
async def get_all_ghl_contacts():
    contacts = await get_ghl_contacts()
    return {"contacts": contacts}

@app.get("/test")
async def get_contacts():
    # Your logic to get contacts
    contacts = [
        {"name": "Jeff Bezos", "email": "jeff.bezos@email.com"},
        {"name": "Elon Musk", "email": "elon.musk@email.com"}
    ]
    return contacts


# ------------- DEFAULT ROUTE START ----------------                

model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"))
prompt = ChatPromptTemplate.from_template("Give me a summary about {topic} in a paragraph or less.")

chain = prompt | model

add_routes(app, chain, path="/openai")

# ------------- DEFAULT ROUTE ENDS ----------------  


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
