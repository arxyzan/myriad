class BaseLoader:
    def __init__(self, source):
        self.source = source
        self.documents = []

    def load(self):
        """
        Load documents from the source and process them.
        This is the main method to be invoked by the user.
        """
        raw_documents = self.read()
        self.documents = self.process(raw_documents)
        return self.documents

    def read(self):
        """
        Read raw documents from the source.
        This method should be overridden by subclasses to handle specific sources.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def process(self, raw_documents):
        """
        Process raw documents into a structured format.
        This method can be overridden by subclasses for custom processing.
        """
        # Default processing logic (can be customized)
        return raw_documents

    def split(self, documents, chunk_size):
        """
        Split documents into smaller chunks.
        """
        chunks = []
        for doc in documents:
            chunks.extend([doc[i:i + chunk_size] for i in range(0, len(doc), chunk_size)])
        return chunks
