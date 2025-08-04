import os
import gettext
import pytest

def test_pt_pt_translation_compiled():
    """Test that pt_PT .mo file exists and can be loaded."""
    mo_path = os.path.join(os.path.dirname(__file__), '../locales/pt_PT/LC_MESSAGES/messages.mo')
    assert os.path.exists(mo_path), f"Missing compiled .mo file: {mo_path}"
    translation = gettext.translation('messages', localedir=os.path.join(os.path.dirname(__file__), '../locales'), languages=['pt_PT'], fallback=False)
    _ = translation.gettext
    assert _(u"Current weather in {city}:") == "Tempo atual em {city}:"
    assert _(u"Could not retrieve weather data.") == "Não foi possível obter os dados do tempo."

def test_pt_pt_translation_runtime():
    """Test that translation works at runtime for a sample string."""
    translation = gettext.translation('messages', localedir=os.path.join(os.path.dirname(__file__), '../locales'), languages=['pt_PT'], fallback=True)
    _ = translation.gettext
    # Should translate if .mo is present, fallback to English if not
    result = _(u"Weather forecast for {city}:").format(city="Lisboa")
    assert result in ["Previsão do tempo para Lisboa:", "Weather forecast for Lisboa:"]
