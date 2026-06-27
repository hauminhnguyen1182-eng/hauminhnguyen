from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from doc_reader import DocReader
from doc_writer import DocWriter
from ai_engine import AIEngine
import os
import uuid

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "/workspace/uploads"
GENERATED_FOLDER = "/workspace/generated"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

reader = DocReader()
writer = DocWriter()
ai = AIEngine()

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    file_id = str(uuid.uuid4())[:8]
    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}{ext}")
    file.save(file_path)

    content = reader.read(file_path)

    return jsonify({
        "file_id": file_id,
        "filename": file.filename,
        "type": content["type"],
        "content_preview": content["content"][:500],
        "metadata": content["metadata"]
    })

@app.route("/api/generate", methods=["POST"])
def generate_document():
    data = request.json
    file_id = data.get("file_id")
    task = data.get("task", "summarize")
    output_type = data.get("output_type", "docx")

    upload_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.startswith(file_id)]
    if not upload_files:
        return jsonify({"error": "File not found"}), 404

    file_path = os.path.join(UPLOAD_FOLDER, upload_files[0])
    content = reader.read(file_path)
    generated = ai.generate(content["content"], task)

    output_path = os.path.join(GENERATED_FOLDER, f"{file_id}.{output_type}")

    if output_type == "docx":
        writer.create_word(generated, output_path, title=data.get("title", "Generated Document"))
    elif output_type == "pptx":
        writer.create_pptx(generated, output_path, title=data.get("title", "Presentation"))
    elif output_type == "xlsx":
        writer.create_excel(generated, output_path)

    return jsonify({
        "file_id": file_id,
        "output_type": output_type,
        "download_url": f"/api/download/{file_id}"
    })

@app.route("/api/download/<file_id>", methods=["GET"])
def download_file(file_id):
    for ext in [".docx", ".pptx", ".xlsx"]:
        path = os.path.join(GENERATED_FOLDER, f"{file_id}{ext}")
        if os.path.exists(path):
            return send_file(path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
