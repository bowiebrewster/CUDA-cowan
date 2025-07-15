#exaustively searches source dir for any files that contain ING11 and copy pastes them into destination directory
#files are index interactively starting at indexstart
import os
import shutil

def copy_files(substr:str, indexstart, source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    count = indexstart

    for root, dirs, files in os.walk(source_dir):
        #print(root, dirs, files)
        for file in files:
            if file == substr:
                source_file = os.path.join(root, file)
                new_filename = f"{substr}_{count}.txt"
                destination_file = os.path.join(destination_dir, new_filename)

                shutil.copy2(source_file, destination_file)
                print(f"Copied: {source_file} -> {destination_file}")
                count += 1

    if count == indexstart:
        print("No {substr} files found.")

# Example usage
source_folder = r"C:\Users\brewster\Desktop\Bowie_calculations\Bowie_calculations"
destination_folder = r"C:\Users\brewster\Desktop\CowanFrontend"
copy_files('ING11',0, source_folder, destination_folder)
