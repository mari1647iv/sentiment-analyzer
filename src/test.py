# -*- coding: utf-8 -*-
from sentiment_analyzer import analyze_comments
import matplotlib.pyplot as plt

"""
Thesis Experiment #1.
Github comments sentiment anlysis via NLTK tool and GitHub API.

  Original file is located at
    https://colab.research.google.com/drive/1oa9_joAGwFQacIe9OJoBcgG1QiGTipA6

Import Pyhton API Requests library.
  Run via bash:

    pip install requests

"""

# Analysis of 500 comments from Ubuntu's $microk8s$ repository

total, pos, neg, neut = analyze_comments(
    "ubuntu", "microk8s", 500, False, True)

print('Total processed: '+str(total))
print('Positive comments: '+str(pos))
print('Negative comments: '+str(neg))
print('Neutral comments: '+str(neut))

maxc = max(pos, neg, neut)
if maxc == neut:
    print("Communication is mostly neutral.")
    print("In other cases:")
    maxc = max(pos, neg)
if maxc == pos:
    print("Communication is mostly positive.\n")
else:
    print("Communication is mostly negative. Some measures should be considered.\n")


labels = 'Positive\n'+str(pos), 'Negative\n'+str(neg), 'Neutral\n'+str(neut)
sizes = [pos, neg, neut]
explode = (0.025, 0.025, 0.025)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
