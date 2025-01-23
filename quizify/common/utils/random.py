import secrets
import string

string_punctuation = "!#$%&()*+,-.:;<=>?@[]^_~"


def remove_exclude_char(s, exclude_chars):
    for i in exclude_chars:
        s = s.replace(i, "")
    return s


def random_replace_char(seq, chars, length):
    using_index = set()

    while length > 0:
        index = secrets.randbelow(len(seq) - 1)
        if index in using_index or index == 0:
            continue
        seq[index] = secrets.choice(chars)
        using_index.add(index)
        length -= 1
    return seq


def random_string(
    length: int,
    lower=True,
    upper=True,
    digit=True,
    special_char=False,
    exclude_chars="",
    symbols=string_punctuation,
):
    if not any([lower, upper, digit]):
        msg = "At least one of `lower`, `upper`, `digit` must be `True`"
        raise ValueError(msg)
    if length < 4:
        msg = "The length of the string must be greater than 3"
        raise ValueError(msg)

    char_list = []
    if lower:
        lower_chars = remove_exclude_char(string.ascii_lowercase, exclude_chars)
        if not lower_chars:
            msg = "After excluding characters, no lowercase letters are available."
            raise ValueError(msg)
        char_list.append(lower_chars)

    if upper:
        upper_chars = remove_exclude_char(string.ascii_uppercase, exclude_chars)
        if not upper_chars:
            msg = "After excluding characters, no uppercase letters are available."
            raise ValueError(msg)
        char_list.append(upper_chars)

    if digit:
        digit_chars = remove_exclude_char(string.digits, exclude_chars)
        if not digit_chars:
            msg = "After excluding characters, no digits are available."
            raise ValueError(msg)
        char_list.append(digit_chars)

    secret_chars = [secrets.choice(chars) for chars in char_list]

    all_chars = "".join(char_list)

    remaining_length = length - len(secret_chars)
    seq = [secrets.choice(all_chars) for _ in range(remaining_length)]

    if special_char:
        special_chars = remove_exclude_char(symbols, exclude_chars)
        if not special_chars:
            msg = "After excluding characters, no special characters are available."
            raise ValueError(msg)
        symbol_num = length // 16 + 1
        seq = random_replace_char(seq, symbols, symbol_num)
    secret_chars += seq

    secrets.SystemRandom().shuffle(secret_chars)
    return "".join(secret_chars)
