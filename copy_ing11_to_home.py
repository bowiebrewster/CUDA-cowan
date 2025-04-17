import os
import shutil

def copy_ing11out_files(source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    count = 1

    for root, dirs, files in os.walk(source_dir):
        print(root, dirs, files)
        for file in files:
            if file == "ING11":
                source_file = os.path.join(root, file)
                new_filename = f"ING11_{count}.txt"
                destination_file = os.path.join(destination_dir, new_filename)

                shutil.copy2(source_file, destination_file)
                print(f"Copied: {source_file} -> {destination_file}")
                count += 1

    if count == 1:
        print("No ING11 files found.")

# Example usage
source_folder = r"C:\Users\brewster\Desktop\Cowan\Test"
destination_folder = r"C:\Users\brewster\Desktop\CUDA Cowan  redone"
copy_ing11out_files(source_folder, destination_folder)
