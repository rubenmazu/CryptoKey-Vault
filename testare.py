from database.crud import *
import datetime

print(" TESTARE CRUD \n")

print("1. Insert Algorithm")
insert_algorithm("AES-256", "symmetric", 256, "OpenSSL")
alg = get_algorithm_by_id(1)
print("   Algorithm inserted:", alg)

print("2. Update Algorithm")
update_algorithm_name(1, "AES-256-Updated")
alg = get_algorithm_by_id(1)
print("   Algorithm updated:", alg)

print("3. Delete Algorithm")
delete_algorithm(1)
alg = get_algorithm_by_id(1)
print("   Algorithm deleted:", alg, "\n")


# ============================
# 2. TEST KEYTABLE CRUD
# ============================

print("4. Insert Key")
insert_algorithm("AES-128", "symmetric", 128, "OpenSSL")  # recreate algorithm
insert_key(1, "ABC123KEY", "2025-01-01")
key = get_key_by_id(1)
print("   Key inserted:", key)

print("5. Update Key")
update_key_value(1, "NEWKEYVALUE")
key = get_key_by_id(1)
print("   Key updated:", key)

print("6. Delete Key")
delete_key(1)
key = get_key_by_id(1)
print("   Key deleted:", key, "\n")


# ============================
# 3. TEST FILE CRUD
# ============================

print("7. Insert File")
insert_file("test.txt", "test.txt", 123)
file_row = get_file_by_id(1)
print("   File inserted:", file_row)

print("8. Update File")
update_file_name(1, "updated_test.txt")
file_row = get_file_by_id(1)
print("   File updated:", file_row)

print("9. Delete File")
delete_file(1)
file_row = get_file_by_id(1)
print("   File deleted:", file_row, "\n")


# ============================
# 4. TEST OPERATION CRUD
# ============================

print("10. Insert Operation")
# recreate dependencies
insert_file("file2.txt", "file2.txt", 200)
insert_key(1, "XYZKEY", "2025-01-02")

insert_operation(
    file_id=2,
    key_id=2,
    algorithm_id=1,
    op_type="encrypt",
    framework="OpenSSL",
    time=0.123,
    memory=512,
    file_hash="ABCDEF123456",
    date=str(datetime.datetime.now())
)

op = get_operation_by_id(1)
print("   Operation inserted:", op)

print("11. Update Operation")
update_operation_time(1, 0.999)
op = get_operation_by_id(1)
print("   Operation updated:", op)

print("12. Delete Operation")
delete_operation(1)
op = get_operation_by_id(1)
print("   Operation deleted:", op, "\n")

print(" TESTARE FINALIZATA ")
