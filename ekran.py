import os
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def write_to_json(event_type, file_path):
    olaylar = {
        "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Olay": event_type,
        "Dosya": file_path
    }
    json_dosya = "/home/ubuntu/bsm/logs/changeso.json"

    try:
        with open(json_dosya, "a", encoding="utf-8") as file:
            json.dump(olaylar, file, ensure_ascii=False)
            file.write("\n")
    except FileNotFoundError:
        with open(json_dosya, "w", encoding="utf-8") as file:
            json.dump(olaylar, file, ensure_ascii=False)
            file.write("\n")

class Izleyici(FileSystemEventHandler):
    def on_created(self, event):
        write_to_json("Yeni dosya oluşturuldu.", event.src_path)

    def on_modified(self, event):
        write_to_json("Dosya değiştirildi.", event.src_path)

    def on_deleted(self, event):
        write_to_json("Dosya silindi.", event.src_path)

    def on_moved(self, event):
        write_to_json("Dosya taşındı veya adı değiştirildi.", event.src_path)

if __name__ == "__main__":
    izlenecek_dizin = "/home/ubuntu/bsm/test"

    if not os.path.exists(izlenecek_dizin):
        print(f"Hata: '{izlenecek_dizin}' dizini bulunamadı.")
        exit(1)

    event_handler = Izleyici()
    observer = Observer()
    observer.schedule(event_handler, izlenecek_dizin, recursive=True)
    observer.start()

    try:
        print(f"İzleme başlatıldı: {izlenecek_dizin}")
        observer.join()
    except KeyboardInterrupt:
        print("\nİzleme durduruldu.")
    finally:
        observer.stop()
        observer.join() 
