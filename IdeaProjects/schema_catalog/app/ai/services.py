from .recommender import Recommender

# Module-level singleton — context is rebuilt lazily on first call
_recommender = Recommender()


class AIService:

    @staticmethod
    def ask(prompt: str) -> str:
        return _recommender.recommend(prompt)

    @staticmethod
    def refresh_context() -> None:
        """Force rebuild of the catalog context (call after catalog changes)."""
        _recommender.build_context()