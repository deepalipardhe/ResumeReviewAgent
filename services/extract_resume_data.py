import fitz
import docx


def extract_text_from_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = ""

        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text

def extract_text_from_resume(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")
    
if __name__ == "__main__":
    file_path = r"C:\Users\Star\Desktop\AI_ML Practice\GenAI\ResumeReviewAgent\input_data\Deepali_GenAI_28042026.pdf"
    resume_text = extract_text_from_resume(file_path)
    print(resume_text)