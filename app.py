from flask import Flask, jsonify
import feedparser
from transformers import pipeline

app = Flask(__name__)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/news')
def get_news():
    url = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
    feed = feedparser.parse(url)
    data = []

    for entry in feed.entries[:5]:
        full_text = entry.summary
        summary = summarizer(full_text, max_length=60, min_length=40, do_sample=False)[0]['summary_text']
        data.append({
            "title": entry.title,
            "summary": summary,
            "link": entry.link
        })

    return jsonify(data)

app.run(host='0.0.0.0', port=3000)
