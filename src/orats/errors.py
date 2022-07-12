class OratsError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Oh, rats! {message}")


class InsufficientPermissionsError(OratsError):
    def __init__(self):
        super().__init__("User does not have access to this resource.")
