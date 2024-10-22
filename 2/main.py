import requests
from bs4 import BeautifulSoup
import re
import nltk
from collections import Counter

# Step 1: Scrape the novel
url = 'https://www.gutenberg.org/files/2701/2701-h/2701-h.htm'  # Moby Dick
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text()

# Step 2: Clean the text
words = re.findall(r'\b\w+\b', text.lower())

# Step 3: Remove stop words
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))
filtered_words = [word for word in words if word not in stop_words]

# Step 4: Analyze word frequency
word_counts = Counter(filtered_words)
most_common_words = word_counts.most_common(10)
print(most_common_words)
