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

            # Rimuove lo sfondo e crea il canale trasparente
            nobg_data = remove(img_data)
            img = Image.open(io.BytesIO(nobg_data))

            # Trova i confini del soggetto e ritaglia
            bbox = img.getbbox()
            if bbox:
                cropped_img = img.crop(bbox)

                # Crea uno sfondo bianco della stessa dimensione dell'immagine ritagliata
                background = Image.new("RGB", cropped_img.size, (255, 255, 255))
                
                # Incolla il soggetto sullo sfondo bianco usando la trasparenza come maschera
                if cropped_img.mode == 'RGBA':
                    background.paste(cropped_img, mask=cropped_img.split()[3])
                else:
                    background.paste(cropped_img)

                # Salva l'immagine finale
                background.save(out_path, "PNG")
                print(f"✅ Salvata con sfondo bianco: {out_path}")
        except Exception as e:
            print(f"❌ Errore su {filename}: {e}")

if __name__ == "__main__":
    process_images()
