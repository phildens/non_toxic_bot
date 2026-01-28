import pytest
from unittest.mock import patch
from bot import check_toxicity

@pytest.mark.asyncio
@patch("requests.post")
async def test_check_toxicity_helper(mock_post):
    """Проверяем, что функция-помощник корректно обрабатывает ответ от API"""
    # Имитируем успешный ответ от FastAPI
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "toxic_probability": 0.95,
        "is_toxic": True
    }
    
    result = await check_toxicity("плохой текст")
    
    assert result["is_toxic"] is True
    assert result["toxic_probability"] == 0.95
    mock_post.assert_called_once()

@pytest.mark.asyncio
@patch("requests.post")
async def test_check_toxicity_error(mock_post):
    """Проверяем поведение при ошибке сервера"""
    mock_post.return_value.status_code = 500
    
    result = await check_toxicity("текст")
    assert result is None
