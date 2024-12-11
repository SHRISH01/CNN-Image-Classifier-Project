class Box:
    def __init__(self, dictionary):
        """
        Custom Box implementation that allows dot notation access to dictionary items
        
        Args:
            dictionary (dict): Input dictionary to convert to a Box object
        """
        for key, value in dictionary.items():
            if isinstance(value, dict):
                # Recursively convert nested dictionaries
                setattr(self, key, Box(value))
            else:
                setattr(self, key, value)
    
    def __getattr__(self, key):
        """
        Fallback method to handle attribute access
        
        Args:
            key (str): Attribute name to access
        
        Raises:
            AttributeError: If attribute is not found
        """
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def get(self, key, default=None):
        """
        Safely get an attribute with an optional default value
        
        Args:
            key (str): Attribute name to access
            default (Any, optional): Default value if attribute is not found
        
        Returns:
            Value of the attribute or default
        """
        try:
            return getattr(self, key)
        except AttributeError:
            return default
    
    def to_dict(self):
        """
        Convert Box object back to a dictionary
        
        Returns:
            dict: Dictionary representation of the Box object
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Box):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result