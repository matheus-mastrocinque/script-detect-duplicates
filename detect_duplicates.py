import os
import hashlib
import imagehash
from PIL import Image
from collections import defaultdict
import shutil

def get_all_images(root_dir):
    image_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(os.path.join(dirpath, filename))
    return image_paths

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def perceptual_hash(filepath):
    try:
        img = Image.open(filepath)
        return str(imagehash.phash(img))
    except Exception as e:
        return None

def detect_duplicates(image_paths):
    name_map = defaultdict(list)
    hash_map = defaultdict(list)
    visual_map = defaultdict(list)

    for path in image_paths:
        name_map[os.path.basename(path)].append(path)
        file_hash = hash_file(path)
        hash_map[file_hash].append(path)

        visual_hash = perceptual_hash(path)
        if visual_hash:
            visual_map[visual_hash].append(path)

    return name_map, hash_map, visual_map

def write_log(duplicates, output_file='duplicates_log.csv'):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Tipo,Hash/Nome,Caminho\n")
        for kind, dup_map in duplicates.items():
            for key, files in dup_map.items():
                if len(files) > 1:
                    for file in files:
                        f.write(f"{kind},{key},{file}\n")

def move_duplicates(dup_map, root_dir):
    backup_dir = os.path.join(root_dir, 'backup_files')
    os.makedirs(backup_dir, exist_ok=True)
    for key, files in dup_map.items():
        if len(files) > 1:
            for file in files[1:]:  # mantém o primeiro
                dest = os.path.join(backup_dir, os.path.basename(file))
                shutil.move(file, dest)

def main():
    root_dir = input("Digite o caminho do diretório com as imagens: ").strip()
    images = get_all_images(root_dir)
    name_map, hash_map, visual_map = detect_duplicates(images)

    write_log({'Nome': name_map, 'Hash': hash_map, 'Visual': visual_map})

    print("Análise concluída. Log gerado como 'duplicates_log.csv'.")
    confirm = input("Deseja mover os arquivos duplicados para a pasta de backup? (s/n): ").strip().lower()
    if confirm == 's':
        move_duplicates(hash_map, root_dir)
        move_duplicates(visual_map, root_dir)
        print("Arquivos duplicados movidos para a pasta 'backup_files'.")

if __name__ == '__main__':
    main()
