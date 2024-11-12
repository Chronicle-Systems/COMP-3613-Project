from abc import ABC, abstractmethod


class Builder(ABC):
    """
    Interface for defining a Builder, which enforces the implementation of 
    a 'build' method to construct and return complex objects.

    Classes implementing this interface should provide specific methods 
    to set up the necessary attributes and parameters for the target object.
    """

    @abstractmethod
    def build(self):
        """
        Constructs and returns the final object after all necessary parameters 
        have been set. The specific type of object to be returned depends on 
        the implementation of the Builder.

        Returns:
            The constructed object based on the set parameters, whose type 
            depends on the implementing class.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError
