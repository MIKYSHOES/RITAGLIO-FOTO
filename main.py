import os
import io
from PIL import Image
from rembg import remove

INPUT_DIR = "foto_input"
OUTPUT_DIR = "foto_output"

def process_images():
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"Cartella '{INPUT_DIR}' creata.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    valid_ext = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(valid_ext)]

    if not files:
        print("Nessuna immagine trovata.")
        return

    for filename in files:
        in_path = os.path.join(INPUT_DIR, filename)
        out_path = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + "_ritagliata.png")

        try:
            with open(in_path, 'rb') as f:
                img_data = f.read()

            nobg_data = remove(img_data)
            img = Image.open(io.BytesIO(nobg_data))

            bbox = img.getbbox()
            if bbox:
                cropped_img = img.crop(bbox)
                cropped_img.save(out_path, "PNG")
                print(f"✅ Salvata: {out_path}")
        except Exception as e:
            print(f"❌ Errore su {filename}: {e}")

if __name__ == "__main__":
    process_images()
