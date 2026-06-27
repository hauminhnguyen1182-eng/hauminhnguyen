from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
import os

class DocReader:
    def read(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.docx':
            return self._read_word(file_path)
        elif ext == '.xlsx':
            return self._read_excel(file_path)
        elif ext == '.pptx':
            return self._read_pptx(file_path)
        return {"type": "unknown", "content": "", "metadata": {}}

    def _read_word(self, path):
        doc = Document(path)
        content = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return {"type": "word", "content": content, "metadata": {"paragraphs": len(doc.paragraphs)}}

    def _read_excel(self, path):
        wb = load_workbook(path)
        content = ""
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            content += f"Sheet: {sheet}\n"
            for row in ws.iter_rows(values_only=True):
                content += " | ".join([str(c) if c else "" for c in row]) + "\n"
        return {"type": "excel", "content": content, "metadata": {"sheets": wb.sheetnames}}

    def _read_pptx(self, path):
        prs = Presentation(path)
        content = ""
        for i, slide in enumerate(prs.slides):
            content += f"Slide {i+1}:\n"
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    content += shape.text + "\n"
        return {"type": "ppt", "content": content, "metadata": {"slides": len(prs.slides)}}

if __name__ == "__main__":
    reader = DocReader()
    print("✅ DocReader ready")
