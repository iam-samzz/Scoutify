import phonenumbers


def get_numbers(text, region=None):

    numbers = set()

    # International / identifiable numbers
    for match in phonenumbers.PhoneNumberMatcher(text, region):

        number = match.number

        if phonenumbers.is_valid_number(number):

            formatted = phonenumbers.format_number(
                number,
                phonenumbers.PhoneNumberFormat.E164
            )

            numbers.add(formatted)

    return numbers