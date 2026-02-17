from config import ODOO_URL, DB_NAME, USERNAME, PASSWORD
from rpc_client import OdooRPCClient
from employee_service import EmployeeService
from timeoff_service import TimeOffService

def main():
    rpc = OdooRPCClient(ODOO_URL, DB_NAME, USERNAME, PASSWORD)
    rpc.authenticate()
    print("Authenticated to Odoo")

    employees = EmployeeService(rpc)
    timeoff = TimeOffService(rpc)

    #Employees
    emp_id = employees.create("John Doe", "Software Engineer")
    print(f"Employee created: ID={emp_id}")

    emp = employees.get(emp_id)
    print("Get employee:", emp)

    employees.update(emp_id, {"job_title": "Senior Software Engineer"})
    print("Employee updated")

    all_emps = employees.list()
    print("All employees:", all_emps)
    # employees.delete(emp_id)
    # print("Deleted")
    new_hires = employees.get_new_hire(days=30)
    for e in new_hires:
        print(e["name"], e["job_title"], e["create_date"])

    # Leave Workflow
    leave_types = timeoff.get_leave_types()
    print("Leave Types:", leave_types)
    if not leave_types:
        print("No leave types found. Create one in Odoo first.")
        return

    leave_type_id = leave_types[0]["id"]

    # Create allocation first (mandatory in Odoo 19)
    allocation_id = timeoff.create_allocation(emp_id, leave_type_id, number_of_days=10)
    print(f"Allocation created: ID={allocation_id} (10 days)")

    leave_id = timeoff.create_leave(
        employee_id=emp_id,
        leave_type_id=leave_type_id,
        date_from="2026-02-15",
        date_to="2026-02-18"
    )
    print(f"Leave request created: ID={leave_id}")

    # timeoff.approve_leave(leave_id)
    # print("Leave approved")

    timeoff.refuse_leave(leave_id)
    print("Leave refused")

    leaves = timeoff.list_leaves()
    print("All Leaves:", leaves)

if __name__ == "__main__":
    main()