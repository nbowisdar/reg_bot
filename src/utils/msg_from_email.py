from bs4 import BeautifulSoup


def _get_uber_code(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(class_="p1b").text


def _get_lyft_recover_link(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('center').a.get("href")

# def _get_lyft_confirm_link(html: str) -> str:
#     soup = BeautifulSoup(html, 'html.parser')
#     return soup.find(class_="p1b").text


def extract_data_from_email(html: str) -> str:
    l = "please verify this is the correct email address for your Lyft account,"
    lyft_recover = "To continue recovering your account, enter your new phone number."
    if "Welcome to Uber" in html:
        return _get_uber_code(html)
    elif lyft_recover in html:
        return _get_lyft_recover_link(html)
    # elif l in html:
    #     return _get_lyft_confirm_link()