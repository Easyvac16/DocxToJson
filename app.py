from flask import Flask, render_template, request, send_file
from docx import Document
import json
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def docx_to_json(docx_path, json_path):
    doc = Document(docx_path)
    table = doc.tables[0]  # Беремо першу таблицю
    data = []
    
    for row in table.rows:
        entry = {
            "name": row.cells[0].text.strip(),
            "task_code": row.cells[1].text.strip(),
            "description": row.cells[2].text.strip(),
            "quantity": row.cells[3].text.strip(),
            "hours": row.cells[4].text.strip() if row.cells[4].text.strip() else None,
            "total_hours": row.cells[5].text.strip(),
            "notes": row.cells[6].text.strip() if len(row.cells) > 6 else None
        }
        data.append(entry)
    
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    
    return json_path

@app.route("/")  # Додаємо маршрут для головної сторінки
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    json_filename = file.filename.rsplit(".", 1)[0] + ".json"
    json_path = os.path.join(OUTPUT_FOLDER, json_filename)
    
    try:
        output_path = docx_to_json(file_path, json_path)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
