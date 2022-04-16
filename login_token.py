class LoginToken:

    def __init__(self, id_, name, user_role):
        self._id = id_  # filled with data: administrator_id, airline_id, customer_id(facade anonymous)
        self._name = name
        self._user_role = user_role

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def user_role(self):
        return self._user_role

    def __repr__(self):
        return f'\nID: {self._id}, Name: {self._name}, User_Role: {self._user_role}'

    def __str__(self):
        return f'\nID: {self._id}, Name: {self._name}, User_Role: {self._user_role}'
