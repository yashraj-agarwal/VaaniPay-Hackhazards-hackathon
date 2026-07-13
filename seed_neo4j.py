import json
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def load_json(path):
    try:
        with open(path, 'r') as f: return json.load(f)
    except: return {}

def seed_database():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    users = load_json('data/users.json')
    accounts = load_json('data/accounts.json')
    transactions = load_json('data/transactions.json')
    
    with driver.session() as session:
        # Clear existing data
        print("Clearing existing data...")
        session.run("MATCH (n) DETACH DELETE n")
        
        print("Creating Users and Accounts...")
        for phone, user_data in users.items():
            acc_id = user_data.get('account_id')
            name = user_data.get('name', 'Unknown')
            pin = user_data.get('pin', '0000')
            lang = user_data.get('lang', 'en')
            
            # Create User node
            session.run("""
                CREATE (u:User {phone: $phone, name: $name, pin: $pin, lang: $lang, account_id: $acc_id})
            """, phone=phone, name=name, pin=pin, lang=lang, acc_id=acc_id)
            
            # Create Account node if it exists
            if acc_id and acc_id in accounts:
                acc_data = accounts[acc_id]
                balance = acc_data.get('balance', 0)
                pf = acc_data.get('pf', 0)
                nps = acc_data.get('nps', 0)
                
                session.run("""
                    MATCH (u:User {phone: $phone})
                    CREATE (a:Account {account_id: $acc_id, balance: $balance, pf: $pf, nps: $nps})
                    CREATE (u)-[:OWNS]->(a)
                """, phone=phone, acc_id=acc_id, balance=balance, pf=pf, nps=nps)
                
                # Add transactions
                if acc_id in transactions:
                    for txn in transactions[acc_id]:
                        txn_type = txn.get('type', 'unknown')
                        amount = txn.get('amount', 0)
                        desc = txn.get('desc', '')
                        
                        session.run("""
                            MATCH (a:Account {account_id: $acc_id})
                            CREATE (t:Transaction {id: randomUUID(), type: $type, amount: $amount, desc: $desc, timestamp: timestamp()})
                            CREATE (a)-[:HAS_TRANSACTION]->(t)
                        """, acc_id=acc_id, type=txn_type, amount=amount, desc=desc)
                        
    driver.close()
    print("Neo4j Seed Complete!")

if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"Error seeding Neo4j: {e}")
        print("Make sure Neo4j is running and NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD are set in .env")
