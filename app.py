from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Temporary in-memory storage
latest_handles = []
latest_keywords = []

@app.route('/', methods=['GET', 'POST'])
def home():
    global latest_handles, latest_keywords
    if request.method == 'POST':
        handles = request.form.get('handles', '')
        keywords = request.form.get('keywords', '')
        latest_handles = [h.strip() for h in handles.split(',') if h.strip()]
        latest_keywords = [k.strip() for k in keywords.split(',') if k.strip()]
    return render_template('index.html', handles=latest_handles, keywords=latest_keywords)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
