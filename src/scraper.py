import os
import re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from unidecode import unidecode
from logging import getLogger
import src.state

logger = getLogger("uvicorn.debug")

DATA_DIRECTORY = "./data"
WAIT_TIME = 1.5
BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?"
TABS = {
    "producao": 2,
    "processamento": 3,
    "comercializacao": 4,
    "importacao": 5,
    "exportacao": 6,
}


def format_text(text: str) -> str:
    """Format the text by removing accents, converting to lowercase, and replacing special characters.

    Args:
        text (str): The text to be formatted.

    Returns:
        str: The formatted text.
    """

    formatted_text = unidecode(text).lower()
    formatted_text = formatted_text.replace("us$", "usd").replace("r$", "brl")
    formatted_text = re.sub(r"[^\w\s]", "", formatted_text).replace(" ", "_")
    return formatted_text


def format_tag_list(tag_list: ResultSet[Tag]) -> list[str]:
    """Format a list of tags by removing accents, converting to lowercase, and replacing special characters.

    Args:
        tag_list (ResultSet[Tag]): A list of BeautifulSoup tags.

    Returns:
        list[str]: A list of formatted strings.
    """

    return [format_text(tag.get_text(strip=True)) for tag in tag_list]


def fetch_url(url: str) -> bytes:
    """Make a GET request to the provided URL and return the content of the response.

    Args:
        url (str): The URL to make the request to.

    Returns:
        bytes: The content of the response.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.HTTPError as e:
        print(f"Erro ao fazer a requisição para a url: {url}: {e}")
        raise


def generate_url(opt_id: int, sub_opt_id: int = 1, year: int | None = None) -> str:
    """Generate a URL based on the provided IDs.

    Args:
        opt_id (int): The ID of the option.
        sub_opt_id (int, optional): The ID of the sub-option. Defaults to 1.
        year (int, optional): The year. Defaults to None.

    Returns:
        str: The generated URL.
    """

    params = f"ano={year}&opcao=opt_0{opt_id}&subopcao=subopt_0{sub_opt_id}"
    return BASE_URL + params


def get_year_interval(soup: BeautifulSoup):
    """Get the start and end year for scraping.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object.

    Returns:
        tuple: A tuple containing the start year and end year.
    """

    year_label = soup.select_one(".lbl_pesq").get_text()
    match = re.search(r"Ano: \[(\d+)-(\d+)\]", year_label)
    if match:
        start_year, end_year = map(int, match.groups())
        return start_year, end_year
    return 0, 0


def get_sub_options(soup: BeautifulSoup):
    """Get the available sub-options on the page.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object.

    Returns:
        list: A list of sub-options.
    """

    sub_option_buttons = soup.find_all("button", {"class": "btn_sopt"})
    if not sub_option_buttons:
        return ["dados"]

    return format_tag_list(sub_option_buttons)


def scrape_page(
    soup: BeautifulSoup, tab_name: str, tab_id: int, start_year: int, end_year: int
):
    """Scrape a page.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the page.
        tab_name (str): The name of the tab.
        tab_id (int): The ID of the tab.
        start_year (int): The start year for scraping.
        end_year (int): The end year for scraping.
    """

    for opt_id, sub_option in enumerate(get_sub_options(soup)):
        file_path = f"{DATA_DIRECTORY}/{tab_name}_{sub_option}.csv"
        if os.path.exists(file_path):
            logger.info(
                f"Scraping in the '{tab_name} - {sub_option}' tab has already been done. "
                "Skipping to the next item."
            )
            continue

        logger.info(
            f"Getting data from {start_year} to {end_year} at '{tab_name} - {sub_option}'"
        )

        rows = []

        table_headers = soup.select_one(".tb_dados > thead > tr").find_all("th")
        col_name, col_quantity, *col_value = format_tag_list(table_headers)

        for year in range(start_year, end_year + 1):
            url = generate_url(tab_id, opt_id + 1, year)
            content = fetch_url(url)
            soup = BeautifulSoup(content, "html.parser")
            table_body = soup.select_one(".tb_dados > tbody")

            parent_id = ""
            for id, row in enumerate(table_body.find_all("tr")):
                columns = row.find_all("td")
                is_parent = (
                    columns[0].has_attr("class") and columns[0]["class"][0] == "tb_item"
                )

                if is_parent:
                    parent_id = id

                product, quantity, *value = [
                    column.get_text(strip=True) for column in columns
                ]

                row_data = {
                    "id": id,
                    "id_pai": "" if is_parent else parent_id,
                    col_name: product,
                    f"{str(year)}_{col_quantity}": quantity,
                }

                # some pages have two year columns: one for quantity other for value
                if value:
                    row_data[f"{str(year)}_{col_value[0]}"] = value[0]

                rows.append(row_data)

            totals = soup.select_one(".tb_dados > .tb_total > tr").find_all("td")
            _, total_quantity, *total_value = [
                total.get_text(strip=True) for total in totals
            ]
            row_data = {
                "id": id + 1,
                "id_pai": "",
                col_name: "TOTAL",
                f"{str(year)}_{col_quantity}": total_quantity,
            }

            if total_value:
                row_data[f"{str(year)}_{col_value[0]}"] = total_value[0]

            rows.append(row_data)

            time.sleep(WAIT_TIME)

        df = pd.DataFrame(rows)
        grouped_df = df.groupby("id").first().sort_values(by="id")
        grouped_df.reset_index(inplace=True)
        os.makedirs(DATA_DIRECTORY, exist_ok=True)
        grouped_df.to_csv(file_path, index=False)
        logger.info(
            f"File '{file_path}' created successfully. Access the data via API."
        )


def scrape_all_pages():
    """Scrape all pages."""

    logger.info("Web Scraping at http://vitibrasil.cnpuv.embrapa.br/ started")

    for tab_name, tab_id in TABS.items():
        url = generate_url(tab_id)
        content = fetch_url(url)
        soup = BeautifulSoup(content, "html.parser")
        start_year, end_year = get_year_interval(soup)
        logger.info(f"Scraping {tab_name}: {url}")
        scrape_page(soup, tab_name, tab_id, start_year, end_year)

    logger.info("Scraping completed. The API is 100% ready to use")
    src.state.is_scraping_completed = True


if __name__ == "__main__":
    scrape_all_pages()
