from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from decouple import config

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# ------------- DEFAULT ROUTE START ----------------                


model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"))
prompt = ChatPromptTemplate.from_template("Give me a summary about {topic} in a paragraph or less.")


chain = prompt | model


add_routes(app, chain, path="/openai")


# ------------- DEFAULT ROUTE ENDS ----------------  


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
