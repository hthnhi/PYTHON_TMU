from modules.file_io import read_customers, write_customers

def add_customer(file_path, customer):
    data = read_customers(file_path)
    data.append(customer)
    write_customers(file_path, data)

def delete_customer(file_path, customer_id):
    data = read_customers(file_path)
    data = [c for c in data if c["id"] != customer_id]
    write_customers(file_path, data)

def update_customer(file_path, customer_id, new_data):
    data = read_customers(file_path)
    for customer in data:
        if customer["id"] == customer_id:
            customer.update({k: v for k, v in new_data.items() if v != ""})
    write_customers(file_path, data)

def search_customers(file_path, keyword):
    data = read_customers(file_path)
    keyword = keyword.lower()
    return [c for c in data if keyword in c["id"].lower() or keyword in c["name"].lower() or keyword in c["phone"]]

def list_customers(file_path):
    return read_customers(file_path)

def add_transaction(file_path, customer_id, transaction):
    """Thêm giao dịch mới cho khách hàng và cộng điểm nếu giao dịch ≥ 100,000."""
    data = read_customers(file_path)
    for customer in data:
        if customer["id"] == customer_id:
            customer["transactions"].append(transaction)
            if transaction.get("amount", 0) >= 100000:
                customer["points"] = customer.get("points", 0) + 1
            break
    write_customers(file_path, data)

def get_transactions(file_path, customer_id):
    data = read_customers(file_path)
    for customer in data:
        if customer["id"] == customer_id:
            return customer.get("transactions", [])
    return []