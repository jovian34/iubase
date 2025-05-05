import re


def get_and_clean_content_from_response(response):
    output = str(response.content)
    output = output.replace("\\n", "")
    output = re.sub(" +", " ", output)
    return output