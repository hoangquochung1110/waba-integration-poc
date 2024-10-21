from typing import Callable
import re


class WabaRenderError(Exception):
    ...


def template_variable_converter(max_merge_fields: int = 1) -> Callable:
    """
    To transform Oclass merge fields Meta variable parameter
    """

    pattern = re.compile(r'{{\s?(.*?)\s?}}')

    def render(text: str) -> str:
        match_count = 0
        for match in pattern.finditer(text):
            if match:
                text = text.replace(
                    match.group(1),
                    str(match_count + 1),
                )
            match_count += 1

            if match_count > max_merge_fields:
                raise WabaRenderError(
                    'At most {limit} merge fields are allowed'.format(
                        limit=max_merge_fields,
                    )
                )
        return text
    return render
