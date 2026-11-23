from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

client = MongoClient("mongodb://ISIS2304A30202620:twrFslnnxkTf@157.253.236.88:8087")
db = client["ISIS2304A30202620"]



def limpiar(docs):
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = limpiar(list(db["comentarios_bares"].find({"bar_id": bar_id})))
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    return limpiar(list(db["eventos"].find({"bar_id": bar_id})))

@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento guardado'}