class GenericResponse:
    def __init__(self, data, status_code) -> None:
        self.data = data
        self.status_code = status_code
