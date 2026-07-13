import json
import time
from mock_db import driver

def load_json(path):
    try:
        with open(path, 'r') as f: return json.load(f)
    except: return {}

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_behavioral_score(user_phone):
    if driver:
        try:
            with driver.session() as session:
                # Complex Graph Query for Credit Score
                query = """
                MATCH (u:User {phone: $phone})-[:OWNS]->(a:Account)
                OPTIONAL MATCH (a)-[:HAS_TRANSACTION]->(t:Transaction)
                RETURN a.balance AS balance, a.pf AS pf, count(t) AS tx_count
                """
                result = session.run(query, phone=user_phone)
                record = result.single()
                if not record:
                    return 300, ["No data"]
                
                savings_bal = record["balance"] or 0
                pf_bal = record["pf"] or 0
                tx_count = record["tx_count"] or 0
                
                score = 300
                factors = []
                
                if tx_count > 5:
                    score += 150
                    factors.append("High transaction volume")
                elif tx_count > 0:
                    score += 50
                    factors.append("Active transaction history")
                    
                if savings_bal > 10000:
                    score += 200
                    factors.append("Strong savings balance")
                elif savings_bal > 2000:
                    score += 100
                    factors.append("Moderate savings balance")
                    
                if pf_bal > 0:
                    score += 150
                    factors.append("Formal employment & PF contribution")
                    
                score = min(score, 900)
                return score, factors
        except Exception as e:
            print(f"Neo4j error in calculate_behavioral_score: {e}. Falling back to JSON.")

    # Fallback to JSON
    users = load_json('data/users.json')
    accounts = load_json('data/accounts.json')
    transactions = load_json('data/transactions.json')
    
    user = users.get(user_phone)
    if not user: return 300, ["No data"]
    
    acc_id = user.get('account_id')
    txns = transactions.get(acc_id, [])
    acc = accounts.get(acc_id, {})
    
    score = 300
    factors = []
    
    if len(txns) > 5:
        score += 150
        factors.append("High transaction volume")
    elif len(txns) > 0:
        score += 50
        factors.append("Active transaction history")
        
    savings_bal = acc.get('balance', 0)
    if savings_bal > 10000:
        score += 200
        factors.append("Strong savings balance")
    elif savings_bal > 2000:
        score += 100
        factors.append("Moderate savings balance")
        
    pf_bal = acc.get('pf', 0)
    if pf_bal > 0:
        score += 150
        factors.append("Formal employment & PF contribution")
        
    score = min(score, 900)
    return score, factors

def perform_upi_transaction(user_phone, amount):
    amount = float(amount)
    
    if driver:
        try:
            with driver.session() as session:
                # Transaction query
                query = """
                MATCH (u:User {phone: $phone})-[:OWNS]->(a:Account)
                WHERE a.balance >= $amount
                SET a.balance = a.balance - $amount
                CREATE (a)-[:HAS_TRANSACTION]->(t:Transaction {id: randomUUID(), type: 'debit', amount: $amount, desc: 'UPI Payment', timestamp: timestamp()})
                RETURN a.balance AS new_balance
                """
                result = session.run(query, phone=user_phone, amount=amount)
                record = result.single()
                if record:
                    return True, record["new_balance"]
                
                # Failed transaction (insufficient funds)
                # Let's get current balance
                bal_result = session.run("MATCH (u:User {phone: $phone})-[:OWNS]->(a:Account) RETURN a.balance AS balance", phone=user_phone)
                bal_record = bal_result.single()
                curr_balance = bal_record["balance"] if bal_record else 0
                return False, curr_balance
        except Exception as e:
            print(f"Neo4j error in perform_upi_transaction: {e}. Falling back to JSON.")

    # Fallback to JSON
    users = load_json('data/users.json')
    accounts = load_json('data/accounts.json')
    txns = load_json('data/transactions.json')
    
    user = users.get(user_phone)
    acc_id = user.get('account_id')
    
    if accounts[acc_id]['balance'] >= amount:
        accounts[acc_id]['balance'] -= amount
        
        if acc_id not in txns:
            txns[acc_id] = []
            
        txns[acc_id].append({"type": "debit", "amount": amount, "desc": "UPI Payment", "timestamp": int(time.time() * 1000)})
        
        save_json('data/accounts.json', accounts)
        save_json('data/transactions.json', txns)
        return True, accounts[acc_id]['balance']
    return False, accounts[acc_id]['balance']

