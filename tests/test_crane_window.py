from cap_dcis_resection.crane import ContextWindow


def test_context_window_overlap():
    text = "one two three four five six"
    window = ContextWindow(window_size=3, overlap=1)
    chunks = window.generate(text)
    assert chunks == ["one two three", "three four five", "five six"]


def test_context_window_empty_text():
    window = ContextWindow(window_size=3)
    assert window.generate("") == []
