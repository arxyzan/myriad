import os

from langchain.document_loaders.base import BaseLoader
from langchain_core.documents import Document


class TextbookLoader(BaseLoader):
    """
    Load a textbook file or files into Document objects.
    """

    def __init__(self, path: str, metadata: dict = None, chapter_splitter: str = None, min_doc_len: int = 10):
        self.path = path
        self.chapter_splitter = chapter_splitter
        self.metadata = metadata or {}
        self.min_doc_len = min_doc_len

    def lazy_load(self):
        docs = []
        # Load all files in the directory
        if os.path.isdir(self.path):
            for root, _, files in os.walk(self.path):
                for file in files:
                    with open(os.path.join(root, file), "r") as f:
                        text = f.read()
                    self.metadata.update({"source": os.path.join(self.path, file)})
                    docs.append(Document(page_content=text, metadata=self.metadata))
        # Load a single file
        elif os.path.isfile(self.path):
            with open(self.path, "r") as f:
                text = f.read()
            self.metadata.update({"source": self.path})
            docs.append(Document(page_content=text, metadata=self.metadata))
        
        # Chunk the documents by chapter
        for doc in docs:
            for chapter in doc.page_content.split(self.chapter_splitter):
                if len(chapter) < self.min_doc_len:
                    continue
                yield Document(page_content=chapter, metadata=self.metadata)