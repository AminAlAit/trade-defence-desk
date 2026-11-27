from trade_defence_desk.guards.number_guard import find_numbers


def test_quote_digits_allowed():
    q = "of a thickness exceeding 0,5 mm"
    assert find_numbers(f'The act says "{q}".', [q]) == []


def test_arabic_indic_digits_caught():
    assert find_numbers("\u0663 mm") == ["\u0663"]


def test_plain_text_passes():
    assert find_numbers("The description gives no thickness.") == []
