class BaseLoader:
    registry = {}

    def __init__(self, source, *args, **kwargs):
        self.source = source

    @classmethod
    def register(cls, name):
        """
        Class method to register a subclass with a given name in the `registry` dictionary of the base class.

        Args:
            name (str): The name to register the subclass with.
        """
        def decorator(subclass):
            if name in cls.registry:
                raise ValueError(f"Class with name '{name}' is already registered.")
            if not issubclass(subclass, cls):
                raise TypeError(f"Registered class '{subclass.__name__}' must be a subclass of '{cls.__name__}'.")
            cls.registry[name] = subclass
            return subclass

        return decorator

    @classmethod
    def create(name, *args, **kwargs):
        """
        Create the loader instance based on the name provided in the `registry`.
        """
        if name not in BaseLoader.registry:
            raise ValueError(f"Unknown loader: '{name}'.")
        return BaseLoader.registry[name](*args, **kwargs)

    def load(self):
        """
        Load documents from the source and process them.
        This is the main method to be invoked by the user.
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

    def split(self, documents, chunk_size, **kwargs):
        """
        Split documents into smaller chunks.
        """
        chunks = []
        for doc in documents:
            chunks.extend([doc[i : i + chunk_size] for i in range(0, len(doc), chunk_size)])
        return chunks
