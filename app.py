import streamlit as st
from modules.customer_ops import add_customer, delete_customer, update_customer, search_customers, list_customers, add_transaction, get_transactions
import os
from datetime import datetime

FILE_PATH = "data/customers.json"
os.makedirs("data", exist_ok=True)

st.set_page_config(page_title="Quản lý Khách hàng Vinmart", layout="centered")

st.title("🏪 Hệ thống Quản lý Khách hàng Vinmart")

menu = st.sidebar.radio("📋 Chọn chức năng", 
    ["Thêm khách hàng", "Xoá khách hàng", "Cập nhật", "Tìm kiếm", "Xem danh sách", "Quản lý giao dịch"])

# Thêm khách hàng
if menu == "Thêm khách hàng":
    st.subheader("➕ Thêm khách hàng mới")
    id_ = st.text_input("Mã KH")
    name = st.text_input("Tên KH")
    phone = st.text_input("Số điện thoại")
    email = st.text_input("Email")
    address = st.text_input("Địa chỉ")
    if st.button("Thêm"):
        if id_ and name:
            add_customer(FILE_PATH, {
                "id": id_, "name": name, "phone": phone, "email": email, "address": address, "transactions": []
            })
            st.success("✅ Thêm thành công!")
        else:
            st.warning("⚠️ Mã và Tên KH là bắt buộc!")

# Xoá khách hàng
elif menu == "Xoá khách hàng":
    st.subheader("🗑️ Xoá khách hàng")
    all_customers = list_customers(FILE_PATH)
    ids = [c["id"] for c in all_customers]
    id_to_delete = st.selectbox("Chọn mã KH để xoá", ids)
    if st.button("Xoá"):
        delete_customer(FILE_PATH, id_to_delete)
        st.success(f"✅ Đã xoá KH có mã {id_to_delete}")

# Cập nhật
elif menu == "Cập nhật":
    st.subheader("✏️ Cập nhật thông tin")
    customers = list_customers(FILE_PATH)
    ids = [c["id"] for c in customers]
    id_to_update = st.selectbox("Chọn mã KH cần cập nhật", ids)
    selected = next((c for c in customers if c["id"] == id_to_update), None)
    if selected:
        name = st.text_input("Tên KH", selected["name"])
        phone = st.text_input("SĐT", selected["phone"])
        email = st.text_input("Email", selected["email"])
        address = st.text_input("Địa chỉ", selected["address"])
        if st.button("Cập nhật"):
            update_customer(FILE_PATH, id_to_update, {
                "name": name,
                "phone": phone,
                "email": email,
                "address": address
            })
            st.success("✅ Cập nhật thành công!")

# Tìm kiếm
elif menu == "Tìm kiếm":
    st.subheader("🔍 Tìm kiếm khách hàng")
    keyword = st.text_input("Nhập mã / tên / SĐT cần tìm")
    if keyword:
        results = search_customers(FILE_PATH, keyword)
        if results:
            st.success(f"✅ Tìm thấy {len(results)} kết quả:")
            st.table(results)
        else:
            st.warning("❌ Không tìm thấy khách hàng nào.")

# Quản lý giao dịch
elif menu == "Quản lý giao dịch":
    st.subheader("💼 Quản lý giao dịch")
    all_customers = list_customers(FILE_PATH)
    ids = [c["id"] for c in all_customers]
    selected_id = st.selectbox("Chọn mã KH", ids)
    
    # Hiển thị danh sách giao dịch
    transactions = get_transactions(FILE_PATH, selected_id)
    if transactions:
        st.write(f"Danh sách giao dịch của KH {selected_id}:")
        for idx, trans in enumerate(transactions, 1):
            st.write(f"{idx}. Ngày: {trans['date']}, Số tiền: {trans['amount']} VNĐ, Mô tả: {trans['description']}")
    else:
        st.info("📭 Chưa có giao dịch nào.")
    
    # Thêm giao dịch mới
    st.subheader("Thêm giao dịch mới")
    trans_date = st.date_input("Ngày giao dịch", value=datetime.today())
    trans_amount = st.number_input("Số tiền (VNĐ)", min_value=0, step=1000)
    trans_desc = st.text_input("Mô tả giao dịch")
    if st.button("Thêm giao dịch"):
        if trans_amount > 0 and trans_desc:
            transaction = {
                "date": trans_date.strftime("%Y-%m-%d"),
                "amount": trans_amount,
                "description": trans_desc
            }
            add_transaction(FILE_PATH, selected_id, transaction)
            st.success(f"✅ Đã thêm giao dịch cho KH {selected_id}!")
        else:
            st.warning("⚠️ Vui lòng nhập số tiền và mô tả!")

# Danh sách
elif menu == "Xem danh sách":
    st.subheader("📖 Danh sách khách hàng hiện có")
    data = list_customers(FILE_PATH)
    if data:
        st.dataframe(data)
    else:
        st.info("📭 Chưa có khách hàng nào.")