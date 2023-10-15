OPTIONS = ['y', 'n', 'yes', 'no']
YES = ['yes', 'y']
NO = ['no', 'n']
OUTPUT_FORMAT = ["csv", "parquet", "xlsx"]
COMPRESSION_FORMAT = ["gz", "bz2", "xz"]
INVALID_INPUT_MESSAGE = "Invalid input. Please enter either 'Y' or 'N'."
PATH_DOES_NOT_EXIST_MESSAGE = "<ansired><b>Path does not exist. Please try again.</b></ansired>"
FILE_DOES_NOT_EXIST_MESSAGE = "<ansired><b>File does not exist. Please try again.</b></ansired>"
UNSUPPORTED_FORMAT_MESSAGE = "<ansired><b>Format not supported. Please try again.</b></ansired>"
YES_NO_PROMPT = "Yes [Y] / No [N]: "

# GET LOCALITY
READ_LOCALLY_QUESTION = "<b>File(s) <skyblue>read</skyblue> locally?</b>"
WRITE_LOCALLY_QUESTION = "<b>File(s) <violet>written</violet> locally? Yes[Y] / No [N]:</b>"
PATH_TO_API_MESSAGE = "<ansigreen><b>Path to file will be an API endpoint.</b></ansigreen>"
FILES_WRITE_LOCALLY_MESSAGE = "<ansigreen><b>Files will be written to your S3 public bucket.</b></ansigreen>"

# GET OUTPUT
OUTPUT_LOCATION_QUESTION = "<b>Output Location:</b>"
OUTPUT_LOCATION_INPUT = "Enter the output location, /path/to/your/file: "
S3_BUCKET_INPUT = "Enter the output location, S3 Bucket: "
INVALID_BUCKET_MESSAGE = "<ansired><b>S3 Bucket does not exist or is not public. Please try again.</b></ansired>"

# GET INPUT
INPUT_LOCATION_QUESTION = "<b>Input Location:</b>"
INPUT_LOCATION_INPUT = "Enter the input source, /path/to/your/file: "
INPUT_API_INPUT = "Enter the input API: "

# GET OUTPUT FORMAT
OUTPUT_FORMAT_QUESTION = "<b>Compression settings:</b>"
OUTPUT_FORMAT_WARNING = ("<ansired>Warning: Exporting to excel is not supported for large file " +
                         "sizes.</ansired>")
COMPRESSION_FORMAT_PROMPT = "Format for compression (gz, bz2, xz): "

# OTHERS
LOADING_MESSAGE = "<b><ansigreen>Loading data.</ansigreen></b>"
FETCH_API_MESSAGE = "<b><ansigreen>Fetching from API.</ansigreen></b>"
LOAD_SUCCESSFUL_MESSAGE = "<b><ansigreen>File loaded successfully.</ansigreen></b>"
EXPORTING_MESSAGE = "Exporting."
EXPORTING_ERROR_MESSAGE = "<ansired><b>Export error. Please try again.</b></ansired>"
EXPORT_SUCCESSFUL_MESSAGE = "File exported successfully."
COMPRESSING_MESSAGE = "Compressing."
