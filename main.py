from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from pydantic import BaseModel, utils
import sqlite3
from sqlite3 import Error

db = sqlite3.connect("services.db", check_same_thread=False)

cursor = db.cursor()

app = FastAPI()


class ArticleTest(BaseModel):
    id_article: int
    name: str
    description: str
    quantity: int

class Commande(BaseModel):
    id: int
    listArticle: utils.List[ArticleTest]
    status: str


@app.post("/article")
async def AddArticles(Articles: ArticleTest):
    if Articles.id_article not in Articles:
        db.execute("INSERT into Article VALUES(?,?,?,?)", (Articles.id_article,
                                                            Articles.name, Articles.description, Articles.quantity,))
        db.commit()
    else:
        return{"ID deja existant"}
    return Articles
    

@app.get("/articles/{articleId}")
async def getArticles(articleId: int):
    cursor.execute("SELECT * FROM Article WHERE id=?", (articleId,))
    article = cursor.fetchone()

    if article:
        return {"article": article}
    else:
        return {"error": "Article not found"}

@app.put("/articles")
async def putArticles(Articles: ArticleTest):
    db.execute("UPDATE Article SET name=?, description=?, quantity=? WHERE id = ?", (Articles.name,Articles.description,Articles.quantity,Articles.id_article))
    db.commit()

    return Articles


@app.post("/commands")
async def postCommand(Commandes: Commande):
    pass

@app.get("/articles")
def get_articles():
            sql = "SELECT * FROM Article"
            cursor.execute(sql)
            result = cursor.fetchall()
            articles = []
            for row in result:
                articles.append({"id": row[0], "name": row[1], "description": row[2], "quantity": row[3]})
            return {"Article": articles}
