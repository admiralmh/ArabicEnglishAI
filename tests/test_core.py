import pytest
from core.arabic_analyzer import ArabicAnalyzer
from core.numerology import NumerologyCalculator

@pytest.fixture
def analyzer():
    return ArabicAnalyzer()

@pytest.fixture
def jummal_calculator():
    return NumerologyCalculator()

def test_arabic_analysis(analyzer):
    sample_text = "اللغة العربية لغة جميلة"
    result = analyzer.analyze_text(sample_text)
    
    assert len(result['tokens']) > 0
    assert len(result['lemmas']) == len(result['tokens'])
    
def test_jummal_calculation(jummal_calculator):
    assert jummal_calculator.calculate_jummal("أبجد") == 1 + 2 + 3 + 4
    assert jummal_calculator.calculate_jummal("محمد") == 40 + 8 + 40 + 4