import pytest
import os
import json
from unittest.mock import patch, MagicMock
from src.ai.recommendation_engine import RetentionAgent

@pytest.fixture
def sample_profile():
    return {
        'tenure': 24,
        'MonthlyCharges': 85.50,
        'Contract': 'Month-to-month',
        'PaymentMethod': 'Electronic check',
        'numTechTickets': 4,
        'ChurnProbability': '85%',
        'TopRiskDriver': 'Numtechtickets'
    }

def test_fallback_behavior(sample_profile):
    # Ensure fallback works without API key
    with patch.dict(os.environ, {"GEMINI_API_KEY": ""}, clear=True):
        agent = RetentionAgent()
        assert agent.client is None
        
        result = agent.get_recommendation(sample_profile)
        assert result['recommended_action'] == "Proactive Tech Support Outreach"
        
        # Test contract fallback
        sample_profile['numTechTickets'] = 0
        result = agent.get_recommendation(sample_profile)
        assert result['recommended_action'] == "Contract Upgrade Incentive"
        
        # Test baseline fallback
        sample_profile['Contract'] = 'Two year'
        result = agent.get_recommendation(sample_profile)
        assert result['recommended_action'] == "VIP Loyalty Check-in"

@patch("src.ai.recommendation_engine.genai.Client")
def test_valid_llm_recommendation(mock_client_class, sample_profile):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.text = '{"recommended_action": "Proactive Tech Support Outreach", "reasoning": "High tickets", "communication_tone": "Empathic"}'
    mock_client.models.generate_content.return_value = mock_response
    
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
        agent = RetentionAgent()
        agent.client = mock_client
        
        result = agent.get_recommendation(sample_profile)
        assert result['recommended_action'] == "Proactive Tech Support Outreach"

@patch("src.ai.recommendation_engine.genai.Client")
def test_malformed_llm_json(mock_client_class, sample_profile):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    
    # Missing closing brace
    mock_response = MagicMock()
    mock_response.text = 'Here is the JSON: {"recommended_action": "Proactive Tech Support Outreach", "reasoning": "High tickets"'
    mock_client.models.generate_content.return_value = mock_response
    
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
        agent = RetentionAgent()
        agent.client = mock_client
        
        # Should gracefully fallback to "Proactive Tech Support Outreach" due to tickets=4
        result = agent.get_recommendation(sample_profile)
        assert result['recommended_action'] == "Proactive Tech Support Outreach"

@patch("src.ai.recommendation_engine.genai.Client")
def test_invalid_action_hallucination(mock_client_class, sample_profile):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.text = '{"recommended_action": "Give $100 Refund", "reasoning": "They are mad", "communication_tone": "Apologetic"}'
    mock_client.models.generate_content.return_value = mock_response
    
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
        agent = RetentionAgent()
        agent.client = mock_client
        
        # Should reject "Give $100 Refund" and trigger fallback
        sample_profile['numTechTickets'] = 0
        sample_profile['Contract'] = 'Month-to-month'
        result = agent.get_recommendation(sample_profile)
        assert result['recommended_action'] == "Contract Upgrade Incentive"
