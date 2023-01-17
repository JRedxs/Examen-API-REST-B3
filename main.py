from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from pydantic import BaseModel, utils
import sqlite3
from sqlite3 import Error

app = FastAPI()