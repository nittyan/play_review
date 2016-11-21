# -*- coding:utf-8 -*-
import datetime
import json
import re
import requests
from typing import Dict
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag


GET_REVIEW_URL = 'https://play.google.com/store/getreviews?authuser=0'
REVIEW_PER_PAGE = 40


class Review:

    def __init__(self, data_review_id: str, review_id: str, author: str, date: datetime.date, title: str, comment: str, rating: int):
        self._data_review_id = data_review_id
        self._review_id = review_id
        self._author = author
        self._date = date
        self._title = title
        self._comment = comment
        self._rating = rating

    @property
    def date_review_id(self):
        return self._data_review_id

    @property
    def review_id(self):
        return self._review_id

    @property
    def author(self):
        return self._author

    @property
    def date(self):
        return self._date

    @property
    def title(self):
        return self._title

    @property
    def comment(self):
        return self._comment

    @property
    def rating(self):
        return self._rating


class PlayReview:

    def __init__(self, app_id: str):
        self._app_id = app_id

    def get_reviews(self, page_num: int) -> List[Review]:
        response = requests.post(GET_REVIEW_URL, data=self._request_params(page_num))
        # Delete because the beginning of the string is useless.
        response_obj = json.loads(response.text[4:])
        html = response_obj[0][2]
        soup = BeautifulSoup(html)

        single_reviews = soup.find_all(class_='single-review')

        return [self._create_review(review) for review in single_reviews]

    def _request_params(self, page_num: int):

        # reviewSortOrder:
        #     0: date desc
        #     1: unknown
        #     2: unknown
        #     3: unknown
        #     4: unknown
        return {
          'reviewType': '0',
          'pageNum': str(page_num),
          'id': self._app_id,
          'reviewSortOrder': '0',
          'xhr': '1',
          'hl': 'ja'
        }

    def _create_review(self, review: Tag) -> Review:
        div_review_header = self._extract_by_class(review, 'review-header')
        review_info = self._review_header_info(div_review_header)

        div_review_body = self._extract_by_class(review, 'review-body')
        review_body = self._review_body_info(div_review_body)

        return Review(
            data_review_id=review_info['data_review_id'],
            review_id=review_info['review_id'],
            author=review_info['author'],
            date=review_info['date'],
            title=review_body['title'],
            comment=review_body['comment'],
            rating=min(map(int, re.findall(r'[1-5]', review_info['rating']))))

    def _review_header_info(self, review_header: Tag) -> Dict[str, object]:
        data_review_id = review_header['data-reviewid']
        review_id = self._extract_by_class(review_header, 'reviews-permalink')['href'].split('reviewId=')[1]
        author = self._extract_by_class(review_header, 'author-name').text
        rating = self._extract_by_class(review_header, 'tiny-star star-rating-non-editable-container')['aria-label']
        date_ja = self._extract_by_class(review_header, 'review-date').text
        date = self._normalize_date(date_ja)

        return {
            'data_review_id': data_review_id,
            'review_id': review_id,
            'author': author,
            'rating': rating,
            'date': date
        }

    @classmethod
    def _normalize_date(cls, date_ja: str) -> datetime.date:
        split = date_ja.split('年')
        year = split[0]
        split = split[1].split('月')
        month = split[0]
        split = split[1].split('日')
        day = split[0]
        return datetime.date(int(year), int(month), int(day))

    @classmethod
    def _review_body_info(cls, review_body: Tag) -> Dict[str, str]:
        split = review_body.text.split(' ')
        title = split[1]
        comment = split[2]

        return {
            'title': title,
            'comment': comment
        }

    @classmethod
    def _extract_by_class(cls, review: Tag, class_name: str) -> Tag:
        return review.find(class_=class_name)

