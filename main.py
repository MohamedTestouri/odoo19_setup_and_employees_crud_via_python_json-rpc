from config import ODOO_URL, DB_NAME, USERNAME, PASSWORD
from rpc_client import OdooRPCClient
from employee_service import EmployeeService

def main():
    rpc = OdooRPCClient(
        ODOO_URL,
        DB_NAME,
        USERNAME,
        PASSWORD
    )

    rpc.authenticate()

    employees = EmployeeService(rpc)

    # CREATE
    emp_id = employees.create("John Doe", "Software Engineer")
    print("Created:", emp_id)

    # READ
    emp = employees.get(emp_id)
    print("Read:", emp)

    # UPDATE
    employees.update(emp_id, {"job_title": "Senior Software Engineer"})
    print("Updated")

    # LIST
    all_emps = employees.list()
    print("All employees:", all_emps)

    # DELETE
    employees.delete(emp_id)
    print("Deleted")

if __name__ == "__main__":
    main()
