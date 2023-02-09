from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from pydantic import BaseModel, utils
import sqlite3
from sqlite3 import Error

db = sqlite3.connect("services.db")

cursor = db.cursor()

app = FastAPI()


class Article(BaseModel):
    id: int
    name: str
    description: str
    quantity: int

class Commande(BaseModel):
    id: int
    listArticle: utils.List[Article]
    status: str


@app.post("/articles")
async def Articles(Articles: Article):
    db.execute("INSERT INTO Articles(?,?,?,?)", (Article.id,Article.name,Article.description,Article.quantity))
    db.commit()
    return Articles


@app.get("/articles/{articleId}")
async def getArticles(articleId: int):
    pass

@app.put("/articles")
async def putArticles(Articles: Article):
    pass



@app.post("/commands")
async def postCommand(Commandes: Commande):
    pass