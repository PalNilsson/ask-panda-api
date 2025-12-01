"""Tests for tools."""


from ask_panda.tools.context_memory import ContextMemory
from ask_panda.tools.vector_store import VectorStore


class TestVectorStore:
    """Tests for VectorStore."""

    def test_add_document(self) -> None:
        """Test adding a document."""
        store = VectorStore()
        idx = store.add_document("Test document")
        assert idx == 0
        assert store.count == 1

    def test_add_documents(self) -> None:
        """Test adding multiple documents."""
        store = VectorStore()
        indices = store.add_documents(["Doc 1", "Doc 2", "Doc 3"])
        assert indices == [0, 1, 2]
        assert store.count == 3

    def test_get_document(self) -> None:
        """Test retrieving a document."""
        store = VectorStore()
        store.add_document("Test document", metadata={"key": "value"})
        doc = store.get_document(0)
        assert doc is not None
        assert doc["content"] == "Test document"
        assert doc["metadata"]["key"] == "value"

    def test_get_document_not_found(self) -> None:
        """Test retrieving non-existent document."""
        store = VectorStore()
        assert store.get_document(0) is None
        assert store.get_document(-1) is None

    def test_search(self) -> None:
        """Test searching documents."""
        store = VectorStore()
        store.add_documents(["Doc about Python", "Doc about Java", "Doc about Go"])
        results = store.search("Python", top_k=2)
        assert len(results) == 2

    def test_clear(self) -> None:
        """Test clearing the store."""
        store = VectorStore()
        store.add_documents(["Doc 1", "Doc 2"])
        store.clear()
        assert store.count == 0


class TestContextMemory:
    """Tests for ContextMemory."""

    def test_add_message(self) -> None:
        """Test adding a message."""
        memory = ContextMemory()
        memory.add_message("user", "Hello")
        assert memory.message_count == 1

    def test_add_user_message(self) -> None:
        """Test adding a user message."""
        memory = ContextMemory()
        memory.add_user_message("Hello")
        messages = memory.get_messages()
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "Hello"

    def test_add_assistant_message(self) -> None:
        """Test adding an assistant message."""
        memory = ContextMemory()
        memory.add_assistant_message("Hi there!")
        messages = memory.get_messages()
        assert messages[0]["role"] == "assistant"

    def test_add_system_message(self) -> None:
        """Test adding a system message."""
        memory = ContextMemory()
        memory.add_system_message("You are helpful")
        messages = memory.get_messages()
        assert messages[0]["role"] == "system"

    def test_get_messages_with_count(self) -> None:
        """Test getting limited messages."""
        memory = ContextMemory()
        for i in range(5):
            memory.add_user_message(f"Message {i}")
        messages = memory.get_messages(count=2)
        assert len(messages) == 2

    def test_to_chat_format(self) -> None:
        """Test converting to chat format."""
        memory = ContextMemory()
        memory.add_system_message("System")
        memory.add_user_message("User")
        memory.add_assistant_message("Assistant")
        chat_format = memory.to_chat_format()
        assert len(chat_format) == 3
        assert chat_format[0] == {"role": "system", "content": "System"}
        assert chat_format[1] == {"role": "user", "content": "User"}
        assert chat_format[2] == {"role": "assistant", "content": "Assistant"}

    def test_context(self) -> None:
        """Test context management."""
        memory = ContextMemory()
        memory.set_context("key", "value")
        context = memory.get_context()
        assert context["key"] == "value"

    def test_clear(self) -> None:
        """Test clearing memory."""
        memory = ContextMemory()
        memory.add_user_message("Hello")
        memory.set_context("key", "value")
        memory.clear()
        assert memory.message_count == 0
        assert memory.get_context() == {}

    def test_max_messages(self) -> None:
        """Test maximum message limit."""
        memory = ContextMemory(max_messages=3)
        for i in range(5):
            memory.add_user_message(f"Message {i}")
        assert memory.message_count == 3
