import json
from pprint import pprint

from decouple import config

from .converters import template_variable_converter
from .variable_generators import generate_template_parameters
from .waba_client import WabaClient

access_token = config('WABA_ACCESS_TOKEN')
phone_number_id = config('WABA_PHONE_NUMBER_ID')
waba_id = config('WABA_ID')

template_header = 'Hello {{recipient_name}}'
template_body = (
    'New user has registered on our site.\n'
    'Name: {{customer_name}}\n'
    'Phone number: {{customer_phone_number}}\n'
)


header_variable_converter = template_variable_converter(max_merge_fields=1)
body_variable_converter = template_variable_converter(max_merge_fields=2)


def create_message_template():
    """
    Sample response:
        '{"id":"1247690869761716","status":"PENDING","category":"MARKETING"}'
    """

    client = WabaClient(access_token, waba_id, phone_number_id)

    basic_template = {
      "name": "seasonal_promotion",
      "language": "en",
      "category": "MARKETING",
      "components": [
        {
          "type": "HEADER",
          "format": "TEXT",
          "text": header_variable_converter(template_header),
          "example": {
            "header_text": 
              generate_template_parameters(template_header),
          }
        },
        {
          "type": "BODY",
          "text": body_variable_converter(template_body),
          "example": {
            "body_text": [              
                generate_template_parameters(template_body)
            ]
          }
        },
      ]    
    }
    pprint(basic_template)

    response = client.create_message_template(json.dumps(basic_template))
    res = response.json()
    return res
  

def send_template_message():
    """
    Sample response:
        {'contacts': [{'input': '+84934099943', 'wa_id': '84934099943'}],
         'messages': [{'id': 'wamid.HBgLODQ5MzQwOTk5NDMVAgARGBJGRkU0RTJBMTk4NjA1ODFEODgA',
                       'message_status': 'accepted'}],
         'messaging_product': 'whatsapp'}
    """
    client = WabaClient(access_token, waba_id, phone_number_id)
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "+84934099943",
        "type": "template",
        "template": {
            "name": "seasonal_promotion",
            "language": {
                "code": "en",
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "text",
                            "text": "Hung Hoang",
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": "Lionel",
                        },
                        {
                            "type": "text",
                            "text": "84867867777",
                        }
                    ]
                }
            ]
        }
    }
    res = client.send_template_message(
        data=json.dumps(data),
    )
    return res


if __name__ == '__main__':
    ...
