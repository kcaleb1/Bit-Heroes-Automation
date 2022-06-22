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
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.txt = kwargs.get('txt', '')

    def __str__(self):
        return f"{self.txt}"


class UnableJoinException(Exception):
    '''This exception will put farm back in queue instead of done'''

    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)

    def __str__(self):
        return f"Unable to join"


class InvalidValueValidateException(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.farm = kwargs.get('farm')
        self.key = kwargs.get('key')
        self.value = kwargs.get('value')
        self.expect = kwargs.get('expect')

    def __str__(self):
        return (f"{self.farm}:\n"
                f"invalid value '{self.key}'='{self.value}'\n"
                f"reason: {self.expect}"
                )


class CannotRerunException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
