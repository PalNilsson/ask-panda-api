"""Vector store for document embeddings and similarity search."""

from typing import Any


class VectorStore:
    """Simple in-memory vector store for document embeddings."""

    def __init__(self, embedding_dim: int = 1536) -> None:
        """Initialize the vector store.

        Args:
            embedding_dim: Dimension of the embeddings.
        """
        self.embedding_dim = embedding_dim
        self._documents: list[dict[str, Any]] = []
        self._embeddings: list[list[float]] = []

    def add_document(self, document: str, metadata: dict[str, Any] | None = None) -> int:
        """Add a document to the store.

        Args:
            document: The document text.
            metadata: Optional metadata for the document.

        Returns:
            The index of the added document.
        """
        doc_entry = {
            "content": document,
            "metadata": metadata or {},
        }
        self._documents.append(doc_entry)
        # Placeholder: In real implementation, would compute embedding
        self._embeddings.append([0.0] * self.embedding_dim)
        return len(self._documents) - 1

    def add_documents(self, documents: list[str], metadata_list: list[dict[str, Any]] | None = None) -> list[int]:
        """Add multiple documents to the store.

        Args:
            documents: List of document texts.
            metadata_list: Optional list of metadata for each document.

        Returns:
            List of indices of the added documents.
        """
        metadata_list = metadata_list or [{}] * len(documents)
        indices = []
        for doc, metadata in zip(documents, metadata_list, strict=True):
            idx = self.add_document(doc, metadata)
            indices.append(idx)
        return indices

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Search for similar documents.

        Args:
            query: The search query.
            top_k: Number of results to return.

        Returns:
            List of matching documents with scores.
        """
        # Placeholder: In real implementation, would compute query embedding
        # and perform similarity search
        results = []
        for i, doc in enumerate(self._documents[:top_k]):
            results.append({
                "index": i,
                "content": doc["content"],
                "metadata": doc["metadata"],
                "score": 0.5,  # Placeholder score
            })
        return results

    def get_document(self, index: int) -> dict[str, Any] | None:
        """Get a document by index.

        Args:
            index: The document index.

        Returns:
            The document entry or None if not found.
        """
        if 0 <= index < len(self._documents):
            return self._documents[index]
        return None

    def clear(self) -> None:
        """Clear all documents from the store."""
        self._documents.clear()
        self._embeddings.clear()

    @property
    def count(self) -> int:
        """Get the number of documents in the store."""
        return len(self._documents)
