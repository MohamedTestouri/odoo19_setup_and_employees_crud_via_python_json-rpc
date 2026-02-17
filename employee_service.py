class EmployeeService:
    MODEL = "hr.employee"

    def __init__(self, rpc_client):
        self.rpc = rpc_client

    def create(self, name, job_title):
        return self.rpc.execute(
            self.MODEL,
            "create",
            {
                "name": name,
                "job_title": job_title
            }
        )

    def get(self, employee_id):
        return self.rpc.execute(
            self.MODEL,
            "read",
            [employee_id],
            ["name", "job_title"]  # fields positional
        )

    def update(self, employee_id, values):
        return self.rpc.execute(
            self.MODEL,
            "write",
            [employee_id],
            values
        )

    def delete(self, employee_id):
        return self.rpc.execute(
            self.MODEL,
            "unlink",
            [employee_id]
        )

    def list(self, limit=10):
        return self.rpc._call(
            "object",
            "execute_kw",
            [
                self.rpc.db,
                self.rpc.uid,
                self.rpc.password,
                "hr.employee",
                "search_read",
                [[]],
                {"fields": ["name", "job_title"], "limit": limit}
            ]
        )
