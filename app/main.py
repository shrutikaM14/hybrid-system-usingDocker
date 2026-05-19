from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from pymongo import MongoClient
from neo4j import GraphDatabase

app = FastAPI()

mongo_client = MongoClient("mongodb://mongodb:27017")

mongo_db = mongo_client["hybriddb"]

product_collection = mongo_db["products"]


neo4j_driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=("neo4j", "password123")
)


class User(BaseModel):
    name: str
    age: int


class Product(BaseModel):
    name: str
    price: int

class Friendship(BaseModel):
    person1: str
    person2: str



def get_connection():
    return psycopg2.connect(
        host="postgres",
        database="hybriddb",
        user="shrutika",
        password="shrutika123",
        port="5432"
    )


@app.on_event("startup")
def startup():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT
        )
    """)

    conn.commit()

    cur.close()
    conn.close()


@app.get("/")
def home():
    return {"message": "Hybrid System Running"}


@app.post("/users")
def create_user(user: User):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, age) VALUES (%s, %s)",
        (user.name, user.age)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {"message": "User added successfully"}


@app.get("/users")
def get_users():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    cur.close()
    conn.close()

    return {"users": users}


@app.post("/products")
def create_product(product: Product):

    data = {
        "name": product.name,
        "price": product.price
    }

    product_collection.insert_one(data)

    return {"message": "Product added to MongoDB"}


@app.get("/products")
def get_products():

    products = []

    for product in product_collection.find():

        products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"]
        })

    return {"products": products}




@app.post("/friendship")
def create_friendship(friendship: Friendship):

    with neo4j_driver.session() as session:

        query = """
        MERGE (a:Person {name: $person1})
        MERGE (b:Person {name: $person2})
        MERGE (a)-[:FRIEND]->(b)
        """

        session.run(
            query,
            person1=friendship.person1,
            person2=friendship.person2
        )

    return {"message": "Friendship created in Neo4j"}

@app.get("/friendships")
def get_friendships():

    friendships = []

    with neo4j_driver.session() as session:

        query = """
        MATCH (a)-[:FRIEND]->(b)
        RETURN a.name AS person1, b.name AS person2
        """

        result = session.run(query)

        for record in result:

            friendships.append({
                "person1": record["person1"],
                "person2": record["person2"]
            })

    return {"friendships": friendships}
