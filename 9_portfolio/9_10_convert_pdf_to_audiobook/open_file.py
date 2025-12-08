import os
from typing import List, Optional, Tuple
import pdfplumber

def open_pdf_file(pdf_file_path: str) -> Optional[Tuple[List[str], int]]:
    if not os.path.exists(pdf_file_path):
        print(f"錯誤：找不到檔案 {pdf_file_path}")
        return None

    try:
        page_texts = []
        with pdfplumber.open(pdf_file_path) as pdf:
            num_pages = len(pdf.pages)
            print(f"PDF 總頁數: {num_pages}")

            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()

                text_to_speak = ""
                if text:
                    text_to_speak = text.replace('\n', ' ').strip()

                if not text_to_speak:
                    print(f" ⚠️ 第 {page_num + 1} 頁無法讀取文本，將使用空字串。")
                    page_texts.append("")
                else:
                    page_texts.append(text_to_speak)

            print("✅ PDF 文本讀取完成！")
            return (page_texts, num_pages)

    except Exception as e:
        print(f"發生錯誤: {e}")
        return None