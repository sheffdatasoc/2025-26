import re
import argparse
import os

# Pattern: PLC/Island 1/<machine-type>/<machine-name>/...
pattern = re.compile(r'^PLC/Island 1/[^/]+/([^/]+)/')

def extract_and_group(input_file):
    groups = {}
    with open(input_file, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('//'):
                continue
            parts = line.split(',', 1)
            if not parts:
                continue
            header = parts[0].strip()
            match = pattern.match(header)
            if match:
                machine_name = match.group(1)
                groups.setdefault(machine_name, []).append(line)
    return groups

def write_groups(groups, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for machine_name, lines in groups.items():
        file_name = f"{machine_name}.csv"
        out_path = os.path.join(output_dir, file_name)
        with open(out_path, 'w') as fout:
            for line in lines:
                fout.write(line + "\n")
        print(f"Written {len(lines)} lines to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and group lines by machine name.")
    parser.add_argument("input_file", help="Path to the input CSV file.")
    parser.add_argument("--output", default=".", help="Output directory for the machine csv files.")
    args = parser.parse_args()

    groups = extract_and_group(args.input_file)
    write_groups(groups, args.output)