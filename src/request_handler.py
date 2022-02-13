import requests
import time


def get_data(url, proxy=None, treat_info_as_error=True, headers=None):
    if headers is None:
        headers = {}

    response = requests.get(url, proxies=proxy, headers=headers)
    json_response = response.json()

    if not json_response:
        raise ValueError('Error getting data from the api, no return was given.')
    elif "Error Message" in json_response:
        raise ValueError(json_response["Error Message"])
    elif "Information" in json_response and treat_info_as_error:
        raise ValueError(json_response["Information"])
    elif "Note" in json_response and treat_info_as_error:
        raise ValueError(json_response["Note"])
    return json_response


def load_webpage(webpage, retries: int = 5):
    if webpage is not None:

        for retry in range(0, retries):
            time_to_sleep = retry * .5 + 1

            src = requests.get(webpage)

            status_code = src.status_code

            # headers = result.headers
            # print(headers)

            if status_code == 200:
                print("webpage: {0} loaded successfully, Retry: {1}".format(webpage, retry))
                return src

            else:
                print("webpage: {0} not loaded with Status Code: {1} sleeping: {2}".format(webpage, status_code,
                                                                                           time_to_sleep))
                time.sleep(time_to_sleep)

        raise TimeoutError
    else:
        #  Set error and return
        raise Exception("Error Error")
