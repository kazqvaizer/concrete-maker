from faker import Faker


class CycleFactory:
    def __init__(self, factory: "Factory", count: int):
        self.factory = factory
        self.count = count

    def __getattr__(self, name):
        if hasattr(self.factory, name):
            return lambda *args, **kwargs: [
                getattr(self.factory, name)(*args, **kwargs) for _ in range(self.count)
            ]


class Factory:
    faker = Faker()

    @classmethod
    def cycle(cls, count):
        return CycleFactory(cls, count)
