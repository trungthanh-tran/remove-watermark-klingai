import argparse
import ffmpeg
import subprocess
import platform
import urllib.request
import zipfile
import time
import os
import sys

# Define Kling logo.
# TODO: FInd the X,Y,W,H by opencv
X = 831
Y= 925
W = 110
H = 30
URL_FFMPEG = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'

# Check if ffmpeg is available
def check_ffmpeg():
    try:
        # Check if ffmpeg is available by running a simple command
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("FFmpeg is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        download_ffmpeg()
        wait_for_ffmpeg()


def download_ffmpeg():
    system = platform.system().lower()
    if system == 'windows':
        ffmpeg_bin = os.path.join('ffmpeg', 'ffmpeg-master-latest-win64-gpl', 'bin', 'ffmpeg.exe')
        if os.path.exists(ffmpeg_bin):
            print(f"Found ffmpeg in {ffmpeg_bin}")
        else:
            print("FFmpeg is not installed in system. Downloading and installing FFmpeg...")
            zip_path = 'ffmpeg.zip'
            download_with_progress(URL_FFMPEG, zip_path)
            print(f"Extracting zip file to {ffmpeg_bin}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('ffmpeg')
            os.remove(zip_path)
        os.environ['PATH'] += os.pathsep + os.path.abspath(os.path.dirname(ffmpeg_bin))
    elif system == 'linux':
        print("FFmpeg is not installed in system. Downloading and installing FFmpeg...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'])
    elif system == 'darwin':  # macOS
        print("FFmpeg is not installed in system. Downloading and installing FFmpeg...")
        subprocess.run(['brew', 'install', 'ffmpeg'])
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)


def wait_for_ffmpeg(timeout=120):
    start_time = time.time()
    while True:
        try:
            subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("FFmpeg is now available.")
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            if time.time() - start_time > timeout:
                print("Timeout: FFmpeg is still not available after 2 minutes.")
                sys.exit(1)
            print("Waiting for FFmpeg to be available...")
            time.sleep(30)

def download_with_progress(url, path):
    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percentage = downloaded / total_size * 100
        sys.stdout.write(f"\rDownloading: {percentage:.2f}%")
        sys.stdout.flush()
    urllib.request.urlretrieve(url, path, show_progress)
    print("\nDownload completed.")

def ask_file_action(file_path):
    if os.path.exists(file_path):
        while True:
            user_input = input(f"The file '{file_path}' already exists. Do you want to delete it? (y/n): ").strip().lower()
            if user_input == 'y':
                os.remove(file_path)
                print(f"The file '{file_path}' has been overwritten.")
                break
            elif user_input == 'n':
                print(f"The file '{file_path}' will be kept. Exit...")
                sys.exit(1)
            else:
                print("Invalid input. Please enter 'delete' or 'keep'.")

def main():
    parser = argparse.ArgumentParser(description="-i input file -o output file")
    # Adding optional arguments
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    # Read arguments from command line
    args = parser.parse_args()

    if not args.input:
        print(f"Input file is required.")
        exit()
    if not args.output:
        print(f"Output file is required.")
        exit()

    ask_file_action(args.output)

    (
        ffmpeg
        .input(args.input)
        .filter('delogo', x=X, y=Y, w=W, h=H)
        .output(args.output)
        .run(quiet=True)
    )


if __name__ == "__main__":
    check_ffmpeg()
    main()