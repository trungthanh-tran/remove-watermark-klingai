import argparse
import ffmpeg

# Define Kling logo.
# TODO: FInd the X,Y,W,H by opencv
X = 831
Y= 925
W = 110
H = 30

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
    (
        ffmpeg
        .input(args.input)
        .filter('delogo', x=X, y=Y, w=W, h=H)
        .output(args.output)
        .run()
    )


if __name__ == "__main__":
    main()