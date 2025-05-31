import pytest
from app import init_session

def test_main_execution():
    """Тест, что main функция выполняется без ошибок"""
    try:
        from app import main
        main()
        assert True
    except Exception as e:
        pytest.fail(f"main() raised exception: {e}")