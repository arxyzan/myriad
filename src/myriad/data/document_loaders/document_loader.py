from ...config import Config


class DocumentLoader:
    registry = {}

    def __init__(self, config: Config, **kwargs):
        self.config = config.update(kwargs)

    @classmethod
    def register(cls, name, config_class: Config):
        """
        Class method to register a subclass with a given name in the `registry` dictionary of the base class.

        Args:
            name (str): The name to register the subclass with.
            config_class (Config): The config class to use with the subclass.
        """

        def decorator(subclass):
            if name in cls.registry:
                raise ValueError(f"Class with name '{name}' is already registered.")
            if not issubclass(subclass, cls):
                raise TypeError(f"Registered class '{subclass.__name__}' must be a subclass of '{cls.__name__}'.")
            cls.registry[name] = {"class": subclass, "config": config_class}
            return subclass

        return decorator

    @classmethod
    def build(name, config: Config = None, **kwargs):
        """
        Build the loader instance based on the name provided in the `registry` and config.
        """
        if name not in DocumentLoader.registry:
            raise ValueError(f"Unknown loader: '{name}'.")
        if config is None:
            config = DocumentLoader.registry[name]["config"]()
        return DocumentLoader.registry[name]["class"](config, **kwargs)

    def load(self):
        """
        Read, process and split the data. This is the main method to be invoked by the user.
        """
        raw_documents = self.read()
        documents = self.process(raw_documents)
        documents = self.split(documents)
        return documents

    def read(self):
        """
        Read raw documents from the source.
        This method should be overridden by subclasses to handle specific sources.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def process(self, raw_documents, **kwargs):
        """
        Process raw documents into a structured format.
        This method can be overridden by subclasses for custom processing.
        """
        return raw_documents

    def split(self, documents, **kwargs):
        """
        Split documents into smaller chunks.
        """
        chunk_size = kwargs.get("chunk_size", 1000)
        chunks = []
        for doc in documents:
            chunks.extend([doc[i : i + chunk_size] for i in range(0, len(doc), chunk_size)])
        return chunks
