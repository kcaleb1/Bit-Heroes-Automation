class EmptyBaitException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self):
        return "No bait left"

class NoRaidEnergyException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self):
        return "No raid energy left"

class ImageNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class MismatchConditionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnimplementedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
