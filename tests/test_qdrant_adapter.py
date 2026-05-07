import unittest

try:
    from app.adapters.vector_db.qdrant_adapter import QdrantAdapter
except ModuleNotFoundError as e:
    QdrantAdapter = None  # type: ignore[assignment]
    _IMPORT_ERROR = e
else:
    _IMPORT_ERROR = None


class _Collection:
    def __init__(self, name: str):
        self.name = name


class _CollectionsResponse:
    def __init__(self, names: list[str]):
        self.collections = [_Collection(n) for n in names]


class _FakeQdrantClient:
    def __init__(self, existing_collections: list[str]):
        self._existing = list(existing_collections)
        self.create_calls: list[str] = []

    async def get_collections(self):
        return _CollectionsResponse(self._existing)

    async def create_collection(self, *, collection_name: str, vectors_config):
        self.create_calls.append(collection_name)
        if collection_name not in self._existing:
            self._existing.append(collection_name)


class TestQdrantAdapterEnsureCollection(unittest.IsolatedAsyncioTestCase):
    async def test_ensure_collection_does_not_iterate_bool(self):
        if QdrantAdapter is None:
            raise unittest.SkipTest(
                f"Optional dependency missing while importing QdrantAdapter: {_IMPORT_ERROR}"
            )

        adapter = QdrantAdapter(url="http://example.invalid:6333", vector_size=384)
        adapter.client = _FakeQdrantClient(existing_collections=[])

        await adapter.ensure_collection("my_collection")
        self.assertIn("my_collection", adapter._collection_ready)
        self.assertEqual(adapter.client.create_calls, ["my_collection"])

        # Second call should be a no-op (no extra create).
        await adapter.ensure_collection("my_collection")
        self.assertEqual(adapter.client.create_calls, ["my_collection"])


if __name__ == "__main__":
    unittest.main()
