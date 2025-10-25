from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

HTML = """
<!doctype html>
<title>CSV Data Processor</title>
<h2>Upload a CSV file to process</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value="Upload">
</form>
<hr>
{{ result|safe }}
"""

@app.route("/", methods=["GET", "POST"])
def upload_file():
    result = ""
    if request.method == "POST":
        file = request.files["file"]
        if file:
            df = pd.read_csv(file)
            summary = df.describe().to_html(classes='table table-striped', border=0)
            head = df.head().to_html(classes='table table-bordered', border=0)
            result = f"<h3>Summary:</h3>{summary}<h3>Top 5 Rows:</h3>{head}"
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
