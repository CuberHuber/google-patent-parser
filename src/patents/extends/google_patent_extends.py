from typing import override

import requests
from bs4 import BeautifulSoup

from decorators.only_once import only_once
from .abc_patent_extends import ABCPatentExtends


class GooglePatentExtends(ABCPatentExtends):
    """
    Структура:
    :abstract: Аннотация патента (на странице патента). Должна содержать только текст (тело) аннотации.
    :images: Список ссылок на изображения, которые встречаются на странице патента.
    :classifications: Список классификации патента. Должен содержать видимый текст (вместе с уникальным номером) классификации.
    :description: Описание, которое обычно находится ниже аннотации.
    :claims: То, что лежит рядом с описанием патента.
    :status: Статус патента (обычно `Active`).
    :inventor: Список с именами людей (если человек один, то список будет с одним элементом).
    :patent_citation_number: Число цитирований патента. Обычно находится в круглых скобочках справа от подзаголовка "Patent Citations".
    :cited_number: Аналогично с цитированием, просто число.
    :priority_applications_number: Аналогично, число ("Priority Applications").
    :apps_claiming_priority_number: Аналогично, число ("Apps Claiming Priority").
    """

    def __init__(self, uri: str):
        self._uri = uri

    @override
    @only_once
    def content(self) -> dict:
        """:returns patent meta data as dict type"""
        _out_dict = {}

        response = requests.get(self._uri)
        if response.status_code != 200:
            raise RuntimeError(f"Request {self._uri} failed with status code {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        # Извлечение данных
        abstract_element = soup.find('div', class_='abstract')
        # abstract = abstract_element.text.strip() if abstract_element else None
        _out_dict['abstract'] = abstract_element.text.strip() if abstract_element else None

        images = [img['src'] for img in soup.select('img[src*="patent"]')] or None
        _out_dict['images'] = images

        classifications_elements = soup.find_all('li', itemprop='classifications')
        classifications = [inv.text.strip() for inv in classifications_elements] if classifications_elements else None
        _out_dict['classifications'] = classifications

        description_element = soup.select_one('.description')
        description = description_element.text.strip() if description_element else None
        _out_dict['description'] = description

        claims_elements = soup.select('.claims .claim')
        claims = "\n".join(claim.text.strip() for claim in claims_elements) if claims_elements else None
        _out_dict['claims'] = claims

        inventor_elements = soup.select('dd[itemprop="inventor"]')
        inventors = [inv.text.strip() for inv in inventor_elements] if inventor_elements else None
        _out_dict['inventor'] = inventors

        family_cites_element = soup.find('h2', string=lambda x: x and 'Family Cites Families' in x)
        if family_cites_element:
            family_cites_text = family_cites_element.get_text(strip=True)
            _out_dict['patent_citation_number'] = int(family_cites_text.split('(')[-1].strip(')'))

        cited_number_element = soup.find('h2', string=lambda x: x and 'Families Citing this family' in x)
        if cited_number_element:
            cited_number_object = cited_number_element.get_text(strip=True)
            cited_number = int(cited_number_object.split('(')[-1].strip(')'))
            _out_dict['cited_number'] = cited_number

        priority_applications = soup.find('h2', string=lambda x: x and 'Applications Claiming Priority' in x)
        if priority_applications:
            priority_applications_text = priority_applications.get_text(strip=True)
            priority_applications_number = int(priority_applications_text.split('(')[-1].strip(')'))
            _out_dict['priority_applications_number'] = priority_applications_number

        apps_claiming_priority_number = int(soup.select_one('.apps-claiming-priority').text.strip()) if soup.select_one(
            '.apps-claiming-priority') else None
        _out_dict['apps_claiming_priority_number'] = apps_claiming_priority_number

        # TODO: dynamic status
        # _out_dict['status'] = "Active"

        return _out_dict
