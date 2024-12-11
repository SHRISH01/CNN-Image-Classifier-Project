class Box:
    def __init__(self, dictionary):
        """
        Initializes the Box object, which dynamically converts a dictionary
        into an object-like structure.
        Recursively processes nested dictionaries into Box objects.

        :param dictionary: A dictionary to convert to a Box object
        """
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, Box(value))  # Recursively create Box for nested dictionaries
            else:
                setattr(self, key, value)  # Set simple values as attributes

    def __getattr__(self, key):
        """
        This method is called when an attribute is accessed that doesn't exist.
        Instead of calling get() again, we return None (or a default value).

        :param key: The attribute name being accessed
        :return: None (or default value) if the attribute is missing
        """
        return None  # Return None if the attribute is not found
    
    def get(self, key, default=None):
        """
        This method attempts to retrieve an attribute. If it doesn't exist,
        it returns a default value instead of raising an error.

        :param key: The attribute to retrieve
        :param default: The default value to return if the attribute doesn't exist
        :return: The attribute value or the default value
        """
        if hasattr(self, key):
            return getattr(self, key)  # Return the value of the attribute if it exists
        else:
            return default  # Return the default if the attribute does not exist

    def to_dict(self):
        """
        Converts the Box object back into a dictionary, recursively handling nested Box objects.
        
        :return: A dictionary representation of the Box object
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Box):
                result[key] = value.to_dict()  # Recursively convert nested Box objects to dicts
            else:
                result[key] = value  # Copy the value directly for non-Box attributes
        return result
    def get_prepare_base_model_config(self):
        # Ensure 'prepare_base_model' is available in the config
        prepare_base_model_config = self.config.get('prepare_base_model', None)
        
        if prepare_base_model_config is None:
            raise ValueError("Configuration for 'prepare_base_model' is missing.")
        
        return prepare_base_model_config
