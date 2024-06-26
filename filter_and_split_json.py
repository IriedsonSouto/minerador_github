import os
import json
import random

# Configurações
INPUT_DIR = 'output'
OUTPUT_DIR = 'filtered_output'
MAX_ENTRIES_PER_FILE = 320
MIN_COMMENT_WORDS = 5  # Número mínimo de palavras em um comentário para ser considerado relevante
MAX_FILES = 1  # Número máximo de arquivos a serem gerados

def load_json_files(input_dir):
    data = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, 'r') as file:
                file_data = json.load(file)
                data.extend(file_data)
    return data

def filter_relevant_comments(data, min_words):
    def is_relevant(comment):
        word_count = len(comment.split())
        return word_count >= min_words

    return [entry for entry in data if is_relevant(entry['comments'])]

def remove_duplicates(data):
    seen_ids = set()
    unique_data = []
    for entry in data:
        if entry['id'] not in seen_ids:
            unique_data.append(entry)
            seen_ids.add(entry['id'])
    return unique_data

def save_filtered_data(data, output_dir, max_entries_per_file, max_files):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        # Excluir todos os arquivos existentes na pasta de saída
        for filename in os.listdir(output_dir):
            filepath = os.path.join(output_dir, filename)
            os.remove(filepath)

    file_index = 1
    data_to_save = data[:max_entries_per_file * max_files]

    for i in range(0, len(data_to_save), max_entries_per_file):
        chunk = data_to_save[i:i + max_entries_per_file]
        output_filename = os.path.join(output_dir, f'filtered_data_{file_index}.json')
        with open(output_filename, 'w') as file:
            json.dump(chunk, file, indent=4)
        file_index += 1
        if file_index > max_files:
            break

def main():
    # Carregar todos os arquivos JSON gerados
    all_data = load_json_files(INPUT_DIR)

    # Filtrar os comentários relevantes
    filtered_data = filter_relevant_comments(all_data, MIN_COMMENT_WORDS)

    # Remover duplicatas
    unique_data = remove_duplicates(filtered_data)

    # Embaralhar os dados únicos filtrados
    random.shuffle(unique_data)

    # Salvar os dados filtrados e únicos em novos arquivos JSON
    save_filtered_data(unique_data, OUTPUT_DIR, MAX_ENTRIES_PER_FILE, MAX_FILES)

    print(f"Processamento concluído. Dados salvos em {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
