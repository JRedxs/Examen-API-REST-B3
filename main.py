from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from pydantic import BaseModel, utils
import sqlite3
from sqlite3 import Error
from typing import List

db = sqlite3.connect("testbdd.db", check_same_thread=False)

cursor = db.cursor()

app = FastAPI()

#Model Article
class ArticleTest(BaseModel):
    id: int
    name: str
    description: str
    quantity: int

#Model Commande
class Commande(BaseModel):
    id: int
    status: str

#Model Article Commande
class ArticleCommande(BaseModel):
    id: int
    id_articles: int
    id_commandes: int

#API pour ajouter un article 
@app.post("/article")
async def AddArticles(Articles: ArticleTest):

     cursor.execute("SELECT * FROM Articles WHERE id=?", (Articles.id,))
     if cursor.fetchone() is not None:
        raise HTTPException(status_code=409, detail="Article avec le même Id déjà existants")
   
     db.execute("INSERT into Articles VALUES(?,?,?,?)", (Articles.id,
                                                            Articles.name, Articles.description, Articles.quantity,))
     db.commit()
     return Articles
    
#API pour récupérer un article en fonction de son ID
@app.get("/articles/{articleId}")
async def getArticles(articleId: int):
    cursor.execute("SELECT * FROM Articles WHERE id=?", (articleId,))
    article = cursor.fetchone()
    if article:
        return {"article": article}
    else:
        raise HTTPException(status_code=404, detail="ID inexistant")

#API pour modifier un article 
@app.put("/articles")
async def putArticles(Articles: ArticleTest):
    cursor.execute("SELECT * FROM Articles WHERE id=?", (Articles.id,))
    if cursor.fetchone() is None:
        db.execute("INSERT into Articles VALUES(?,?,?,?)", (Articles.id,
                                                            Articles.name, Articles.description, Articles.quantity,))
        db.commit()
        return Articles
    else:
        db.execute("UPDATE Articles SET name=?, description=?, quantity=? WHERE id = ?", (Articles.name,Articles.description,Articles.quantity,Articles.id))
        db.commit()
        return Articles


#API pour récupérer tous les articles
@app.get("/articles")
def get_articles():
            sql = "SELECT * FROM Articles"
            cursor.execute(sql)
            result = cursor.fetchall()
            articles = []
            for row in result:
                articles.append({"id": row[0], "name": row[1], "description": row[2], "quantity": row[3]})
            return {"Article": articles}

#API pour récupérer la commande
@app.get("/commands")
async def getCommand():
        sql = """
        SELECT c.id, c.status, 
        group_concat(a.name) AS articles,
        group_concat(a.quantity) AS quantities,
        group_concat(a.description) AS descriptions
        FROM Commandes c
        JOIN ArticleCommande ac ON c.id = ac.id_commandes
        JOIN Articles a ON ac.id_articles = a.id
        GROUP BY c.id
            """
        cursor.execute(sql)
        
        result = cursor.fetchall()
            
        commands = []
        for row in result:
            articles = row[2].split(",")
            quantities = row[3].split(",")
            descriptions = row[4].split(",")
            articles_list = []
            for i in range(len(articles)):
                article = {"name": articles[i], "quantity": quantities[i], "description": descriptions[i]}
                articles_list.append(article)
            command = {"id": row[0], "articles": articles_list, "status": row[1]}
            commands.append(command)
        return commands

#API pour ajouter une commande
@app.post("/commandes")
async def post_commande(commande: Commande, articles: List[ArticleTest]):
    cursor.execute("INSERT INTO Commandes (status) VALUES (?)", (commande.status,))
    commande_id = cursor.lastrowid

    for article in articles:
        cursor.execute("SELECT * FROM Articles WHERE id = ?", (article.id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Article non trouvé par l'id {}".format(article.id))
        cursor.execute("INSERT INTO ArticleCommande (id_articles, id_commandes) VALUES (?, ?)", (article.id, commande_id))

    db.commit()
    return {"commande": commande, "articles": articles}

@app.put("/commandes")
async def put_commande(Commande: Commande, articles: List[ArticleTest]):
    cursor.execute("SELECT * FROM Commandes WHERE id=?", (Commande.id))
    if cursor.fetchone() is None:
        db.execute("INSERT into Commandes VALUES(?,?)", (Commande.id,Commande.status))
        db.commit()
        return Commande
    else:
        db.execute("UPDATE Commandes SET status=? WHERE id = ?", (Commande.status,Commande.id,articles))
        db.commit()
        return Commande