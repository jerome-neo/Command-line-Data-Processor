import time

from prompt_toolkit import print_formatted_text, HTML

from common import Common

output_file_name = "result"

def main():
    """
    Main function for running the command line application.

    This function initializes the 'Common' class, interacts with the user through prompts, loads data, performs cleaning
    , exports data to a specified location, and measures the execution time.
    """
    app = Common()
    app.get_locality()
    app.get_input_source()
    app.get_output_location()
    app.get_output_format()
    app.set_export_compression()

    start_time = time.time()
    app.load()
    app.clean()
    app.export(output_file_name)
    end_time = time.time()

    message = f"Program executed in {end_time - start_time:.2f} seconds"
    print_formatted_text(HTML("<skyblue><b>" + message + "</b></skyblue>"))


if __name__ == "__main__":
    main()
