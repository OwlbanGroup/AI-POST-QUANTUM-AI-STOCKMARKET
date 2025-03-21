class UserManagement:
    def __init__(self):
        self.users = {}

    def create_user(self, username, initial_balance):
        if username in self.users:
            return "User already exists."
        self.users[username] = {
            "balance": initial_balance,
            "portfolio": {}
        }
        return f"User {username} created with balance {initial_balance}."

    def get_user(self, username):
        return self.users.get(username, "User not found.")

    def update_balance(self, username, amount):
        if username in self.users:
            self.users[username]["balance"] += amount
            return f"Updated balance for {username}: {self.users[username]['balance']}"
        return "User not found."
