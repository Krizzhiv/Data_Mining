from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']

    # --- Your scraping code ---
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        data = {
            "url": url,
            "title": soup.title.string if soup.title else "No Title Found",
            "content_snippet": soup.get_text()[0:] + "..." # Display a snippet
        }

        # For now, we'll just display the data. We can still save it to a file if we want.
        # with open("website_data.json", "w", encoding="utf-8") as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)

        return render_template('results.html', data=data)

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)