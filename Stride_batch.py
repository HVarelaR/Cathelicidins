## STRIDE secondary structure composition calculated with Python.
import os
import sys
from collections import Counter

def parse_stride_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize a Counter for secondary structures
    sec_struct_counter = Counter()
    total_residues = 0
    
    # Read through each line in the file
    for line in lines:
        if line.startswith('ASG'):
            # Extract the secondary structure type
            sec_struct_type = line[24]  # Secondary structure type is in the 25th column (index 24)
            sec_struct_counter[sec_struct_type] += 1
            total_residues += 1
    
    return sec_struct_counter, total_residues

def calculate_percentages(counter, total):
    percentages = {}
    for struct, count in counter.items():
        percentages[struct] = (count / total) * 100
    return percentages

def process_stride_files(directory_path):
    results = []
    
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".stride"):
            file_path = os.path.join(directory_path, file_name)
            sec_struct_counter, total_residues = parse_stride_file(file_path)
            if total_residues == 0:
                print(f"Warning: No residues found in the file {file_name}. Skipping...")
                continue
            
            percentages = calculate_percentages(sec_struct_counter, total_residues)
            results.append((file_name, percentages))
    
    return results

def save_results_to_tsv(results, output_file):
    structure_names = {
        'H': 'Alpha Helix',
        'G': '310 Helix',
        'I': 'Pi Helix',
        'E': 'Beta Strand',
        'B': 'Beta Bridge',
        'T': 'Turn',
        'C': 'Coil'
    }
    
    all_structures = set(structure_names.keys())
    
    with open(output_file, 'w') as file:
        headers = ["Entry"] + [structure_names[struct] for struct in all_structures]
        file.write("\t".join(headers) + "\n")
        
        for file_name, percentages in results:
            row = [file_name]
            for struct in all_structures:
                row.append(f"{percentages.get(struct, 0.0):.2f}")
            file.write("\t".join(row) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python stride_batch_parser.py <stride_directory> <output_file>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print(f"Error: Directory {directory_path} does not exist or is not a directory.")
        sys.exit(1)
    
    results = process_stride_files(directory_path)
    save_results_to_tsv(results, output_file)
    print(f"Results saved to {output_file}")
