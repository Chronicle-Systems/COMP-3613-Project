class Singleton(type):
    """
    A metaclass that implements the Singleton pattern. Ensures that only a single
    instance of any class using this metaclass is created.

    Attributes:
        _instances (dict): A dictionary that stores instances of classes that use 
                           this metaclass, where the key is the class itself.

    Methods:
        __call__(cls, *args, **kwargs): Controls the instantiation of the class 
                                        to ensure only one instance is created.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Overrides the default `__call__` method to control class instantiation. 
        Checks if an instance of `cls` already exists in the `_instances` dictionary.
        If it does not, creates a new instance of `cls`, stores it in `_instances`, 
        and returns it. If it does exist, returns the existing instance.

        Args:
            *args: Positional arguments to be passed to the class constructor.
            **kwargs: Keyword arguments to be passed to the class constructor.

        Returns:
            The singleton instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
