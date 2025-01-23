import os

from langchain_core.documents import Document

from .base_loader import BaseLoader

class TextbookLoader(BaseLoader):
    """
    Load a textbook file or files into Document objects.
    """

    def __init__(self, path: str, metadata: dict = None, chapter_splitter: str = None, min_doc_len: int = 10):
        super().__init__(path)
        self.chapter_splitter = chapter_splitter
        self.metadata = metadata or {}
        self.min_doc_len = min_doc_len

    def read(self):
        docs = []
        # Load all files in the directory
        if os.path.isdir(self.source):
            for root, _, files in os.walk(self.source):
                for file in files:
                    with open(os.path.join(root, file), "r") as f:
                        text = f.read()
                    self.metadata.update({"source": os.path.join(self.source, file)})
                    docs.append({"text": text, "metadata": self.metadata.copy()})
        # Load a single file
        elif os.path.isfile(self.source):
            with open(self.source, "r") as f:
                text = f.read()
            self.metadata.update({"source": self.source})
            docs.append({"text": text, "metadata": self.metadata.copy()})
        return docs

    def split(self, raw_documents):
        split_docs = []
        for doc in raw_documents:
            for chapter in doc["text"].split(self.chapter_splitter):
                if len(chapter) < self.min_doc_len:
                    continue
                split_docs.append({"text": chapter, "metadata": doc["metadata"]})
        return split_docs

    def process(self, raw_documents):
        processed_docs = []
        for doc in raw_documents:
            # Add your filtering, cleaning, etc. logic here
            processed_docs.append(Document(page_content=doc["text"], metadata=doc["metadata"]))
        return processed_docs