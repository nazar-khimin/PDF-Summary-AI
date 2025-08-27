import pytest_check as check
from src.database.models import DimPrompts
from .fixtures import db_session


class TestDimPrompts:
    def test_create_prompt_record(self, db_session):
        """Test creating a prompt record"""
        prompt = self.create_test_prompt(
            db_session,
            "You are an expert summarizer.",
            "Please summarize the key points."
        )
        
        # Verify the record was created
        retrieved = db_session.query(DimPrompts).filter_by(user_prompt="Please summarize the key points.").first()
        check.is_not_none(retrieved, "Prompt record should be created")
        check.equal(retrieved.system_prompt, "You are an expert summarizer.", "System prompt should match expected value")
    
    def create_test_prompt(self, session, system_prompt, user_prompt):
        """Create a test prompt record"""
        prompt = DimPrompts(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
        session.add(prompt)
        session.commit()
        return prompt