import os
import shutil
import warnings
from ebooklib import epub
from PyPDF2 import PdfReader

warnings.filterwarnings("ignore")  # Uyarıları bastırmak için

# PDF işleme
def process_pdf(file_path, target_folder):
    try:
        reader = PdfReader(file_path)
        if not any(page.extract_text() for page in reader.pages):
            print(f"Metinsiz PDF bulundu ve taşındı: {file_path}")
            shutil.move(file_path, target_folder)
        else:
            print(f"Metin içeriyor: {file_path}")
    except Exception as e:
        print(f"PDF işleme hatası: {file_path}, Hata: {e}")
        shutil.move(file_path, target_folder)

# EPUB işleme
def process_epub(file_path, target_folder):
    try:
        book = epub.read_epub(file_path)
        if not book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            print(f"Metinsiz EPUB bulundu ve taşındı: {file_path}")
            shutil.move(file_path, target_folder)
        else:
            print(f"Metin içeriyor: {file_path}")
    except Exception as e:
        print(f"EPUB işleme hatası: {file_path}, Hata: {e}")
        shutil.move(file_path, target_folder)

# MOBI işleme
def process_mobi(file_path, target_folder):
    try:
        # MOBI desteği için "mobi" modülü kullanılabilir (örneğin, Calibre'nin MOBI API'leri)
        # Ancak MOBI'yi analiz etme kısmı genellikle EPUB benzeri yaklaşır.
        print(f"MOBI desteği henüz tam entegre edilmedi: {file_path}")
    except Exception as e:
        print(f"MOBI işleme hatası: {file_path}, Hata: {e}")
        shutil.move(file_path, target_folder)

# Klasör tarama
def scan_files(root_folder, target_folder, scan_subfolders=True):
    for folder, subfolders, filenames in os.walk(root_folder):
        if not scan_subfolders and folder != root_folder:
            continue  # Alt klasörler taranmayacaksa atla

        for filename in filenames:
            file_path = os.path.join(folder, filename)
            try:
                if filename.lower().endswith('.pdf'):
                    process_pdf(file_path, target_folder)
                elif filename.lower().endswith('.epub'):
                    process_epub(file_path, target_folder)
                elif filename.lower().endswith('.mobi'):
                    process_mobi(file_path, target_folder)
                else:
                    print(f"Desteklenmeyen dosya türü: {filename}")
            except Exception as e:
                print(f"Dosya işleme hatası: {file_path}, Hata: {e}")

# Ana program
def main():
    root_folder = input("Tarama yapılacak ana klasörün yolunu girin: ").strip()
    target_folder = input("Metinsiz dosyaların taşınacağı hedef klasörün yolunu girin: ").strip()
    scan_subfolders = input("Alt klasörler de taransın mı? (Y/N): ").strip().upper() == 'Y'

    if not os.path.exists(root_folder):
        print("Ana klasör bulunamadı. Çıkış yapılıyor.")
        return

    if not os.path.exists(target_folder):
        print("Hedef klasör bulunamadı, oluşturuluyor...")
        os.makedirs(target_folder)

    print("Tarama başlatılıyor...")
    scan_files(root_folder, target_folder, scan_subfolders)
    print("Tarama tamamlandı!")

if __name__ == "__main__":
    main()
