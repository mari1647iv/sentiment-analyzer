# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/1oa9_joAGwFQacIe9OJoBcgG1QiGTipA6

Import Pyhton API Requests library.
  Run via bash:

    pip install requests

"""

import requests


def analyze_comments_page(username, repo, per_page, page, print_comments, print_stage_results):
    """
    Analyzes one page of GitHub comments. Helping function.

    Parameters
    ----------

    username : str
        The GitHub alias of the repository owner
    repo : str
        The GitHub repository name
    per_page : int
        The number of comments on the page (from 0 to 100)
    page : int
        The page number of the results to fetch
    print_comments : bool
        If True, each fetched comment and its analysis will be printed
    print_stage_results : bool
        If True, final statistics of the analyzed comments will be printend in the end

    Returns
    -------
    total : int
        The number of comments fetched (if number of comments on the page is less than per_page parameter all the available comments will be processed and their number will be returned. Else, equal to per_page)
    pos : int
        The number of positive comments fetched
    neg : int
        The number of negative comments fetched
    neut : int
        The number of neutral comments fetched
    """

    total = 0
    pos = 0
    neg = 0
    neut = 0

    print("Processing page #"+str(page)+"...\n")
    query = {'per_page': per_page, 'page': page}
    resp = requests.get("https://api.github.com/repos/" +
                        username+"/"+repo+"/issues/comments", params=query)
    comments = resp.json()

    for comment in comments:
        total = total+1
        if print_comments:
            print(str(total) + '. ' + comment.get("body"))

        query = {'text': comment.get("body")}
        response = requests.post(
            "http://text-processing.com/api/sentiment/", data=query)
        if print_comments:
            print(response.json())
            print('\n')

        sentiment = response.json().get("label")
        if sentiment == 'pos':
            pos = pos+1
        elif sentiment == 'neg':
            neg = neg+1
        else:
            neut = neut+1

    if print_stage_results:
        print('Processed: '+str(total))
        print('Positive comments: '+str(pos))
        print('Negative comments: '+str(neg))
        print('Neutral comments: '+str(neut))

    return total, pos, neg, neut


# the final function to be used
def analyze_comments(username, repo, comments_to_process, print_comments, print_stage_results):
    """
    Analyzes the given number of comments in the given repository.

    Parameters
    ----------

    username : str
        The GitHub alias of the repository owner
    repo : str
        The GitHub repository name
    comments_to_process : int
        The number of comments to be fetched
    print_comments : bool
        If True, each fetched comment and its analysis will be printed
    print_stage_results : bool
        If True, statistics of the analyzed comments on each stage(for each fetched page) will be printend

    Returns
    -------
    total : int
        The number of comments fetched (if number of comments in repo is less than comments_to_process parameter all the available comments will be processed and their number will be returned. Else, equal to comments_to_process)
    pos : int
        The number of positive comments fetched
    neg : int
        The number of negative comments fetched
    neut : int
        The number of neutral comments fetched
    """

    total = 0
    pos = 0
    neg = 0
    neut = 0
    page = 1
    temp = comments_to_process

    while True:
        if comments_to_process <= 0:
            print("Finishing...\n")
            break
        if comments_to_process <= 100:
            total, pos, neg, neut = map(lambda x: x[0]+x[1], zip((total, pos, neg, neut), analyze_comments_page(
                username, repo, comments_to_process, page, print_comments, print_stage_results)))
            print("Processed in total: "+str(total)+"/"+str(temp)+"\n")
            break
        else:
            total, pos, neg, neut = map(lambda x: x[0]+x[1], zip((total, pos, neg, neut), analyze_comments_page(
                username, repo, 100, page, print_comments, print_stage_results)))
            print("Currently processed: "+str(total)+"/"+str(temp)+"\n")
            page += 1
            comments_to_process -= 100

    return total, pos, neg, neut
