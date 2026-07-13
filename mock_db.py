import os
import json
from dotenv import load_dotenv

load_dotenv()

# Check for Neo4j credentials
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = None
if NEO4J_URI and NEO4J_USER and NEO4J_PASSWORD:
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        print("Neo4j AuraDB Connected successfully!")
    except Exception as e:
        print(f"Neo4j connection failed: {e}")
        driver = None
else:
    print("Neo4j credentials not found. Falling back to JSON mock DB.")

def load_json(path):
    try:
        with open(path, 'r') as f: return json.load(f)
    except: return {}

def get_user(phone):
    if driver:
        try:
            with driver.session() as session:
                result = session.run("MATCH (u:User {phone: $phone}) RETURN u", phone=phone)
                record = result.single()
                if record:
                    return dict(record['u'])
                return None
        except Exception as e:
            print(f"Neo4j error in get_user: {e}. Falling back to JSON.")
    
    # Fallback to JSON
    users = load_json('data/users.json')
    return users.get(phone)

def get_account(acc_id):
    if driver:
        try:
            with driver.session() as session:
                result = session.run("MATCH (a:Account {account_id: $acc_id}) RETURN a", acc_id=acc_id)
                record = result.single()
                if record:
                    return dict(record['a'])
                return None
        except Exception as e:
            print(f"Neo4j error in get_account: {e}. Falling back to JSON.")
            
    # Fallback to JSON
    accounts = load_json('data/accounts.json')
    return accounts.get(acc_id)

def get_transactions(acc_id):
    if driver:
        try:
            with driver.session() as session:
                result = session.run("MATCH (a:Account {account_id: $acc_id})-[:HAS_TRANSACTION]->(t:Transaction) RETURN t ORDER BY t.timestamp DESC", acc_id=acc_id)
                txns = []
                for record in result:
                    txns.append(dict(record['t']))
                return txns
        except Exception as e:
            print(f"Neo4j error in get_transactions: {e}. Falling back to JSON.")
            
    # Fallback to JSON
    transactions = load_json('data/transactions.json')
    return transactions.get(acc_id, [])