from open_file import open_pdf_file
import os
from gtts import gTTS


class ConvertPdfToAudiobook:
    """
    Write a Python script that takes a PDF file and converts it into speech.
    """
    def __init__(self):
        print("[Converter] 開始使用 gTTS 進行語音合成...")

    def convert_pdf_to_audiobook(
        self,
        page_texts: list[str],
        num_pages: int,
        output_dir: str = "audiobook_output",
        language: str = "zh-TW"
):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"已創建輸出資料夾：{output_dir}")

        for page_num, text_to_speak in enumerate(page_texts):
            current_page = page_num + 1

            if not text_to_speak:
                print(f"[Converter] 跳過第 {current_page} 頁，因為沒有有效文本。")
                continue

            try:
                # 3. 初始化 gTTS
                tts = gTTS(text=text_to_speak, lang=language)

                # 4. 儲存音訊檔案
                output_filename = os.path.join(output_dir, f"page_{current_page}.mp3")
                tts.save(output_filename)

                print(f"[Converter] ✅ 成功轉換第 {current_page}/{num_pages} 頁，保存為 {output_filename}")

            except Exception as gtts_e:
                print(f"[Converter] ⚠️ gTTS 轉換第 {current_page} 頁時發生錯誤（可能網路連線問題）：{gtts_e}")
                continue

        print("\n--- 轉換音檔結束 ---")


if __name__ == "__main__":
    pdf_file_path = "dog_story.pdf"
    # 設定輸出語言
    audio_language = "en"
    output_dir = "audiobook_output"

    print("--- 步驟一：讀取文本 ---")
    extraction_result = open_pdf_file(pdf_file_path)

    if extraction_result:
        page_texts, total_pages = extraction_result

        print("\n--- 步驟二：轉換音訊 ---")
        # 2. 執行音訊轉換
        converter = ConvertPdfToAudiobook()
        converter.convert_pdf_to_audiobook(
            page_texts=page_texts,
            num_pages=total_pages,
            output_dir=output_dir,
            language=audio_language
        )
    else:
        print("❌ 由於 PDF 文本讀取失敗，無法進行音訊轉換。")