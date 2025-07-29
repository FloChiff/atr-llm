import openai
import sys
import re
from pathlib import Path

# CONFIGURATION
openai.api_key = "sk-..."
openai.api_base = "https://openrouter.ai/api/v1"
model_id = "mistralai/mixtral-8x7b-instruct"

class EnhancedOCRCorrector:
    def __init__(self):
        print("✅ OCR Corrector initialized")

    def preprocess_text(self, text):
        text = re.sub(r'\s+([,.;:!?])', r'\1', text)
        text = re.sub(r'([,.;:!?])([A-Za-zÀ-ÿ])', r'\1 \2', text)
        return text.strip()

    def enhanced_prompt(self, original_text):
        has_dates = bool(re.search(r'\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4}', original_text))
        has_numbers = bool(re.search(r'\d+', original_text))
        has_proper_nouns = bool(re.search(r'\b[A-Z][a-z]+\b', original_text))
        has_old_french = bool(re.search(r'\b(sy|cy|ſ|œ|æ)\b', original_text))

        base_prompt = (
            "You are an OCR correction assistant specialized in multilingual documents, including historical and modern texts.\n"
            "The input may be in French, English, or other European languages. You must detect the language implicitly from the input.\n\n"
            "Your job is to carefully correct ONLY clear OCR mistakes such as:\n"
            "- Misrecognized letters or diacritics (e.g., 'l' instead of 'i', 'rn' instead of 'm', 'é' replaced with 'e')\n"
            "- Fused or broken words\n"
            "- Obvious spacing errors (e.g., 't h e' → 'the', 'd e s' → 'des')\n"
            "- Missing punctuation or obvious OCR artifacts\n\n"
            "STRICT RULES:\n"
            "1. NEVER correct grammar, style, or vocabulary.\n"
            "2. NEVER modernize historical spellings, archaic forms, or regional variations.\n"
            "3. NEVER modify or expand abbreviations, contractions, or symbols.\n"
            "4. NEVER change any word that is written entirely in UPPERCASE.\n"
            "5. If you are unsure about a correction, KEEP the original.\n"
            "6. Preserve the original layout: line breaks, punctuation, and paragraph structure must remain intact.\n"
            "7. Do NOT add or remove any content beyond correcting OCR errors.\n"
            "8. Proper nouns, place names, and personal names must be preserved unless an OCR mistake is obvious.\n\n"
            "Your response MUST contain ONLY the corrected text, with NO explanation, NO formatting changes, and NO comments."
        )

        if has_dates:
            base_prompt += "- Pay special attention to dates and preserve their exact format\n"
        if has_numbers:
            base_prompt += "- Be very careful with numbers (years, quantities, references)\n"
        if has_proper_nouns:
            base_prompt += "- Preserve proper nouns even if they seem unusual\n"
        if has_old_french:
            base_prompt += "- This text contains old French, preserve archaic forms\n"

        return base_prompt

    def process_file(self, input_file, output_file):
        with open(input_file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        if len(raw_text.strip()) == 0:
            print(f"   ⚪ Empty file - skipped")
            return None

        preprocessed_text = self.preprocess_text(raw_text)

        if len(preprocessed_text) > 7000:
            print(f"   📊 Large file detected ({len(preprocessed_text)} characters) - splitting into chunks")
            return self.process_large_file(preprocessed_text, input_file, output_file)

        try:
            response = openai.ChatCompletion.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": self.enhanced_prompt(preprocessed_text)},
                    {"role": "user", "content": preprocessed_text}
                ],
                temperature=0.1
            )
            ai_corrected = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"   ❌ AI error: {str(e)}")
            return None

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(ai_corrected)

        return True

    def process_large_file(self, text, input_file, output_file):
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk + paragraph) > 6000:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph

        if current_chunk:
            chunks.append(current_chunk.strip())

        print(f"   📦 Split into {len(chunks)} chunks")

        corrected_chunks = []

        for i, chunk in enumerate(chunks):
            print(f"   📝 Chunk {i+1}/{len(chunks)}")

            try:
                response = openai.ChatCompletion.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": self.enhanced_prompt(chunk)},
                        {"role": "user", "content": chunk}
                    ],
                    temperature=0.1
                )
                ai_chunk = response["choices"][0]["message"]["content"].strip()
                corrected_chunks.append(ai_chunk)
            except Exception as e:
                print(f"      ❌ Error on chunk {i+1}: {str(e)}")
                corrected_chunks.append(chunk)

        final_text = '\n\n'.join(corrected_chunks)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_text)

        return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 correction_llm.py <input_folder> <output_folder>")
        sys.exit(1)

    text_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not text_dir.exists():
        print(f"❌ Input folder not found: {text_dir}")
        sys.exit(1)

    output_dir.mkdir(exist_ok=True)

    corrector = EnhancedOCRCorrector()

    txt_files = sorted(text_dir.glob("*.txt"))
    if not txt_files:
        print(f"❌ No .txt files found in {text_dir}")
        sys.exit(1)

    success_count = 0
    error_count = 0

    for txt_file in txt_files:
        try:
            result = corrector.process_file(txt_file, output_dir / txt_file.name)
            if result:
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            print(f"❌ Critical error on {txt_file.name}: {str(e)}")
            error_count += 1

    print(f"✅ Processing complete")

if __name__ == "__main__":
    main()
