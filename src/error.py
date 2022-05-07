class EmptyBaitException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self):
        return "No bait left"


class NoEnergyException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        self.feature = kwargs.get('feature', '')

    def __str__(self):
        return f"No energy for '{self.feature}'"


class ImageNotFoundException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        self.image_path = kwargs.get('image_path', '')

    def __str__(self):
        return f"Image {self.image_path} not found"


class MismatchConditionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self):
        return "Required condition unmatched"


class UnimplementedException(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.feature = kwargs.get('feature', '')

    def __str__(self):
        return f"Feature '{self.feature}' not implemented"
