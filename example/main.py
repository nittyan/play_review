# -*- coding: utf-8 -*-
from play import PlayReview


def main():
    play_review = PlayReview('<your app id>')

    for i in range(2):
        reviews = play_review.get_reviews(i)
        for r in reviews:
            print(r.comment)


if __name__ == '__main__':
    main()