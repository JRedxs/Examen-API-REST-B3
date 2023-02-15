from fastapi import FastAPI, status, HTTPException
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
    id_articles : int
    listArticle: utils.List[ArticleTest]
    status: str


@app.post("/article")
async def AddArticles(Articles: ArticleTest):

     cursor.execute("SELECT * FROM Article WHERE id=?", (Articles.id_article,))
     if cursor.fetchone() is not None:
        raise HTTPException(status_code=409, detail="Article avec le même Id déjà existants")
   
     db.execute("INSERT into Articles VALUES(?,?,?,?)", (Articles.id_article,
                                                            Articles.name, Articles.description, Articles.quantity,))
     db.commit()
     return Articles
    

@app.get("/articles/{articleId}")
async def getArticles(articleId: int):
    cursor.execute("SELECT * FROM Article WHERE id=?", (articleId,))
    article = cursor.fetchone()
    if article:
        return {"article": article}
    else:
        raise HTTPException(status_code=404, detail="ID inexistant")

@app.put("/articles")
async def putArticles(Articles: ArticleTest):
    db.execute("UPDATE Article SET name=?, description=?, quantity=? WHERE id = ?", (Articles.name,Articles.description,Articles.quantity,Articles.id_article))
    db.commit()

    return Articles



@app.get("/articles")
def get_articles():
            sql = "SELECT * FROM Article"
            cursor.execute(sql)
            result = cursor.fetchall()
            articles = []
            for row in result:
                articles.append({"id": row[0], "name": row[1], "description": row[2], "quantity": row[3]})
            return {"Article": articles}

@app.post("/commands")
async def postCommand(Commandes: Commande):
            db.execute("INSERT INTO Commande VALUES(?,?,?)", (Commandes.id,Commandes.listArticle,Commandes.status))
            db.commit() #on doit ajouter une relation entre Commande et articles foreign key je pense 
            return Commandes

@app.get("/commands")

async def getCommand(Commandes: Commande):
            sql = "SELECT * FROM Commande"
            cursor.execute(sql)
            result = cursor.fetchall()
            commande = []
            for row in result:
                commande.append({"id": row[0], "listArticle": row[1], "status": row[2]})
            return {"Commande": commande}
 