class IPError(Exception):
    
    def __init__(self, message:str, *args) -> None:
        self.message = message
        super().__init__(*args)