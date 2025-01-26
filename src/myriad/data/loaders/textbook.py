from dataclasses import dataclass
import os

from langchain_core.documents import Document

from ...config import Config
from .document_loader import DocumentLoader


@dataclass
class TextbookLoaderConfig(Config):
    source: str = None
    metadata: dict = None
    chapter_splitter: str = None
    min_doc_len: int = 10

@DocumentLoader.register("textbook", config_class=TextbookLoaderConfig)
class TextbookLoader(DocumentLoader):
    """
    Load a textbook file or files into Document objects.
    """

    def __init__(self, config: TextbookLoaderConfig, **kwargs):
        super().__init__(config=config, **kwargs)

    def read(self):
        docs = []
        # Load all files in the directory
        if os.path.isdir(self.config.source):
            for root, _, files in os.walk(self.config.source):
                for file in files:
                    with open(os.path.join(root, file), "r") as f:
                        text = f.read()
                    self.config.metadata.update({"source": os.path.join(self.config.source, file)})
                    docs.append({"text": text, "metadata": self.config.metadata.copy()})
        # Load a single file
        elif os.path.isfile(self.config.source):
            with open(self.config.source, "r") as f:
                text = f.read()
            self.config.metadata.update({"source": self.config.source})
            docs.append({"text": text, "metadata": self.config.metadata.copy()})
        return docs

    def split(self, documents):
        split_docs = []
        for doc in documents:
            for chapter in doc["text"].split(self.config.chapter_splitter):
                if len(chapter) < self.config.min_doc_len:
                    continue
                split_docs.append({"text": chapter, "metadata": doc["metadata"]})
        return split_docs

    def process(self, raw_documents):
        processed_docs = []
        for doc in raw_documents:
            # Add your filtering, cleaning, etc. logic here
            processed_docs.append(Document(page_content=doc["text"], metadata=doc["metadata"]))
        return processed_docs
