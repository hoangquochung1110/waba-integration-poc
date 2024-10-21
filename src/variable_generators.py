import re


MERGE_FIELD_EXAMPLES = {
    'recipient_name': 'John',
    'customer_name': 'Bill',
    'customer_phone_number': '1234567890',
}


def generate_template_parameters(value):
    parameters = []

    pattern = re.compile(r'{{\s?(.*?)\s?}}')
    for match in pattern.finditer(value):
        if match:
            parameter = MERGE_FIELD_EXAMPLES[match.group(1)]
            parameters.append(parameter)
    
    return parameters
