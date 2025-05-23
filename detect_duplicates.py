import os
import hashlib
import imagehash
from PIL import Image
from collections import defaultdict
import shutil

# Coleta todas as imagens válidas no diretório e subpastas
def get_all_images(root_dir):
    image_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                image_paths.append(os.path.join(dirpath, filename))
    return image_paths

# Calcula o hash de conteúdo do arquivo (para identificar arquivos idênticos byte a byte)
def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Gera o hash perceptual (semelhança visual)
def perceptual_hash(filepath):
    try:
        img = Image.open(filepath)
        return str(imagehash.phash(img))
    except Exception:
        return None

# Detecta duplicatas por nome, conteúdo e similaridade visual (aproximada)
def detect_duplicates(image_paths):
    name_map = defaultdict(list)
    hash_map = defaultdict(list)
    visual_map = defaultdict(list)

    phash_list = []

    for path in image_paths:
        name_map[os.path.basename(path)].append(path)

        file_hash = hash_file(path)
        hash_map[file_hash].append(path)

        visual_hash = perceptual_hash(path)
        if visual_hash:
            phash_list.append((visual_hash, path))

    # Comparação aproximada de hashes perceptuais
    visited = set()
    for i, (hash1, path1) in enumerate(phash_list):
        if path1 in visited:
            continue
        group = [path1]
        for j in range(i + 1, len(phash_list)):
            hash2, path2 = phash_list[j]
            if path2 in visited:
                continue
            diff = imagehash.hex_to_hash(hash1) - imagehash.hex_to_hash(hash2)
            if diff <= 5:  # Ajuste esse valor se quiser mais ou menos sensibilidade
                group.append(path2)
                visited.add(path2)
        if len(group) > 1:
            visual_map[hash1] = group

    return name_map, hash_map, visual_map

# Gera o log das duplicatas encontradas
def write_log(duplicates, output_file='duplicates_log.csv'):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Tipo,Hash/Nome,Caminho\n")
        for kind, dup_map in duplicates.items():
            for key, files in dup_map.items():
                if len(files) > 1:
                    for file in files:
                        f.write(f"{kind},{key},{file}\n")

# Move os arquivos duplicados para uma pasta de backup
def move_all_duplicates(dup_maps, root_dir):
    all_duplicates = set()

    for dup_map in dup_maps:
        for files in dup_map.values():
            if len(files) > 1:
                all_duplicates.update(files[1:])  # preserva o primeiro

    backup_dir = os.path.join(root_dir, 'backup_files')
    os.makedirs(backup_dir, exist_ok=True)

    for file in all_duplicates:
        dest = os.path.join(backup_dir, os.path.basename(file))
        if os.path.exists(file):
            shutil.move(file, dest)
            print(f"Movido: {file} -> {dest}")
        else:
            print(f"Arquivo não encontrado (possivelmente já movido): {file}")

# Função principal
def main():
    root_dir = input("Digite o caminho do diretório com as imagens: ").strip().strip('"').strip("'")
    images = get_all_images(root_dir)
    name_map, hash_map, visual_map = detect_duplicates(images)

    write_log({'Nome': name_map, 'Hash': hash_map, 'Visual': visual_map})
    print("Análise concluída. Log gerado como 'duplicates_log.csv'.")

    confirm = input("Deseja mover os arquivos duplicados para a pasta de backup? (s/n): ").strip().lower()
    if confirm == 's':
        move_all_duplicates([hash_map, visual_map], root_dir)
        print("Arquivos duplicados movidos para a pasta 'backup_files'.")

if __name__ == '__main__':
    main()
