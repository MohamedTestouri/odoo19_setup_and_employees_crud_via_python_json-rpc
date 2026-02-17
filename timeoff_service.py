class TimeOffService:
    LEAVE_MODEL = "hr.leave"
    LEAVE_ALLOCATION_MODEL = "hr.leave.allocation"
    LEAVE_TYPE_MODEL = "hr.leave.type"

    def __init__(self, rpc_client):
        self.rpc = rpc_client

    def get_leave_types(self):
        return self.rpc.execute(
            self.LEAVE_TYPE_MODEL,
            "search_read",
            [],
            ["id", "name"]
        )

    # Create allocation and approve it
    def create_allocation(self, employee_id, leave_type_id, number_of_days):
        allocation_id = self.rpc.execute(
            self.LEAVE_ALLOCATION_MODEL,
            "create",
            {
                "employee_id": employee_id,
                "holiday_status_id": leave_type_id,
                "number_of_days": number_of_days,
                "allocation_type": "regular",
                "name": f"Allocation for employee {employee_id}",
            }
        )
        self.rpc.execute(
            self.LEAVE_ALLOCATION_MODEL,
            "action_approve",
            [allocation_id]
        )
        return allocation_id

    # Create leave (requires allocation exists and is approved)
    def create_leave(self, employee_id, leave_type_id, date_from, date_to):
        allocations = self.rpc.execute(
            self.LEAVE_ALLOCATION_MODEL,
            "search_read",
            [
                ("employee_id", "=", employee_id),
                ("holiday_status_id", "=", leave_type_id)
            ],
            ["id"]
        )
        if not allocations:
            print(f"No allocation found for employee {employee_id}, creating one...")
            self.create_allocation(employee_id, leave_type_id, number_of_days=10)

        return self.rpc.execute(
            self.LEAVE_MODEL,
            "create",
            {
                "employee_id": employee_id,
                "holiday_status_id": leave_type_id,
                "request_date_from": date_from,
                "request_date_to": date_to,
                "name": f"Leave for employee {employee_id}",
            }
        )

    def approve_leave(self, leave_id):
        return self.rpc.execute(
            self.LEAVE_MODEL,
            "action_approve",
            [leave_id]
        )

    def refuse_leave(self, leave_id):
         return self.rpc.execute(
            self.LEAVE_MODEL,
            "action_refuse",
            [leave_id]
        )

    def list_leaves(self):
        return self.rpc.execute(
            self.LEAVE_MODEL,
            "search_read",
            [],
            ["id", "employee_id", "holiday_status_id", "state"]
        )