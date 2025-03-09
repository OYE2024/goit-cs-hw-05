import requests
import re
from collections import defaultdict
from html.parser import HTMLParser
import matplotlib.pyplot as plt


class MyHTMLParser(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data + " "


def fetch_text(url: str) -> str:
    """The function gets the text from the link and returns it as a cleaned string."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        parser = MyHTMLParser()
        parser.feed(response.text)
        # видаляємо непотрібні символи
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', parser.text.lower())
        return cleaned_text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def map_function(text: str) -> list:
    """The function splits the text into words."""
    words = text.split()
    return [(word, 1) for word in words]


def shuffle_function(mapped_values: list) -> dict:
    """The function sorts and groups data based on a key."""
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(shuffled_values: dict) -> dict:
    """The function performs aggregation of values ​​for each key."""
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced


def map_reduce(text: str) -> dict:
    """The function manages the process of map and reduce"""
    mapped_values = map_function(text)
    shuffled_values = shuffle_function(mapped_values)
    reduced_values = reduce_function(shuffled_values)
    return reduced_values


def visualize_top_words(word_counts: dict) -> None:
    """The function visualizes the top 10 words that are most frequently repeated."""
    sorted_words = sorted(word_counts.items(),
                          key=lambda x: x[1], reverse=True)[:10]
    words, counts = zip(*sorted_words)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('TOP-10 words that are most frequently repeated')
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    url = input("Enter any URL: ")
    text = fetch_text(url)
    print(text[:100])
    result = map_reduce(text)
    visualize_top_words(result)
