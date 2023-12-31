import argparse
from processor import VideoProcessor
from preprocess import PreProcessImage
from tracker import Tracking


def main():
    """
    Main function to process a video and detect stationary objects.

    This function sets up the video processing pipeline by parsing command-line arguments,
    configuring preprocessing techniques, initializing tracking methods, and initiating the
    video processing workflow using the VideoProcessor class.

    Command-line arguments can be used to customize various aspects of the video processing,
    including input and output paths, preprocessing options, tracking parameters, and pixel
    threshold values.

    Usage:
        The program is typically run from the command line, providing necessary arguments.
        For example:
        ```
        python main_program.py -i input_video.mp4 -o output_folder
        ```
    """
    parser = argparse.ArgumentParser(description='This program tracks differences and detects stationary objects in a video.')
    parser.add_argument('-i', '--input', type=str, help='Path to the input video.', required=True)
    parser.add_argument('-o', '--output', type=str, help='Path to output folder.', default=VideoProcessor.DEFAULT_OUT_PATH)
    parser.add_argument('-m', '--mask', type=str, help='Path to a mask image.', default=None)
    parser.add_argument('-g', '--ignore', type=str, help='Path to a list of positions of boxes in the frame that you want the program to ignore. Each line contains 1 box position. Example format: [x1, y1, x2, y2]', default=None)
    parser.add_argument('--iou', type=float, help='IOU threshold for object matching.', default=Tracking.DEFAULT_IOU_THRESHOLD)
    parser.add_argument('--min-size', type=int, help='Minimun area of the contour box to be recorded as an object.', default=Tracking.DEFAULT_MIN_SIZE)
    parser.add_argument('--track-rate', type=int, help='Number of frames between stationary object checks', default=Tracking.DEFAULT_TRACK_RATE)
    parser.add_argument('--white', type=int, help='Set the minimum value (from 0 to 255) to be white pixel otherwise will be turned black.', default=VideoProcessor.DEFAULT_WHITE_THRESHOLD)
    parser.add_argument('--black', type=int, help='Set the minimum value (from 0 to 255) to be black pixel otherwise will be turned white.', default=VideoProcessor.DEFAULT_BLACK_THRESHOLD)
    parser.add_argument("--gray", type=bool, help="(bool) False to turn off grayscale in preprocessing, True otherwise", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--contrast", type=bool, help="(bool) True to turn on auto contrast in preprocessing, False otherwise", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--blur", type=bool, help="(bool) True to turn on blurring in preprocessing, False otherwise", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--edge", type=bool, help="(bool) True to turn on finding edge in preprocessing, False otherwise", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--save", type=bool, help="(bool) True to turn on saving result video in preprocessing, False otherwise", action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()
    
    pre_process = PreProcessImage(
        gray=args.gray, 
        contrast=args.contrast, 
        blur=args.blur, 
        edge=args.edge, 
        mask_path=args.mask
        )
    
    tracking = Tracking(
        track_rate=args.track_rate,
        ignore_path=args.ignore,
        min_size=args.min_size,
        iou_threshold=args.iou
    )
    
    video_processor = VideoProcessor(
        source_path=args.input,
        out_path=args.output, 
        preprocess=pre_process, 
        tracking=tracking,
        white_threshold=args.white,
        black_threshold=args.black
        )
    
    video_processor.process_video()


if __name__ == "__main__":
    main()