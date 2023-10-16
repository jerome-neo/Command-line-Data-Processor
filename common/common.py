import os
import re
import json
import gzip
import lzma
import bz2
from io import StringIO

import pandas as pd
import urllib3
from urllib3.exceptions import HTTPError

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML
import prompt_toolkit as pt

from service.s3_service import is_public_s3_bucket, upload_to_s3
from validator.output_validator import OutputValidator
from .constants import *


class Common:
    def __init__(self):
        self.input = ""
        self.output = ""
        self.out_format = ""
        self.data = None
        self.input_locally = True
        self.output_locally = True
        self.compress_format = ""

    def get_locality(self) -> None:
        try:
            print_formatted_text(HTML(READ_LOCALLY_QUESTION))
            while True:
                read = pt.prompt(YES_NO_PROMPT)
                if read.lower().strip() not in OPTIONS:
                    print(INVALID_INPUT_MESSAGE)
                    continue
                if read.lower().strip() in NO:
                    self.input_locally = False
                    print_formatted_text(HTML(PATH_TO_API_MESSAGE))
                break

            print_formatted_text(HTML(WRITE_LOCALLY_QUESTION))
            while True:
                write = pt.prompt(YES_NO_PROMPT)
                if write.lower().strip() not in OPTIONS:
                    print(INVALID_INPUT_MESSAGE)
                    continue
                if write.lower().strip() in NO:
                    self.output_locally = False
                    print_formatted_text(HTML(FILES_WRITE_LOCALLY_MESSAGE))
                break
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_output_location(self) -> str:
        print_formatted_text(HTML(OUTPUT_LOCATION_QUESTION))
        while True:
            if self.output_locally:
                output_location = pt.prompt(OUTPUT_LOCATION_INPUT).strip()
                if os.path.exists(output_location) and os.path.isdir(output_location):
                    break
                else:
                    print_formatted_text(HTML(PATH_DOES_NOT_EXIST_MESSAGE))
            else:
                output_location = pt.prompt(S3_BUCKET_INPUT).strip()
                if is_public_s3_bucket(output_location):
                    break
                else:
                    print_formatted_text(HTML(INVALID_BUCKET_MESSAGE))

        self.output = output_location
        return output_location

    def get_input_source(self) -> str:
        print_formatted_text(HTML(INPUT_LOCATION_QUESTION))
        while True:
            if self.input_locally:
                input_source = pt.prompt(INPUT_LOCATION_INPUT).strip()
                if os.path.exists(input_source):
                    break
                else:
                    print_formatted_text(HTML(FILE_DOES_NOT_EXIST_MESSAGE))
            else:
                input_source = pt.prompt(INPUT_API_INPUT).strip()
                break
        self.input = input_source
        return input_source

    def get_output_format(self) -> None:
        print_formatted_text(HTML(OUTPUT_FORMAT_QUESTION))
        while True:
            output_format = pt.prompt(OUTPUT_FORMAT_INPUT,
                                      validator=OutputValidator()).strip()
            if output_format.lower() in OUTPUT_FORMAT:
                if output_format.lower() == "xlsx":
                    print_formatted_text(HTML(OUTPUT_FORMAT_WARNING))
                break
            else:
                print_formatted_text(HTML(UNSUPPORTED_FORMAT_MESSAGE))
        self.out_format = output_format.lower()

    def set_export_compression(self) -> None:
        print_formatted_text(HTML(OUTPUT_COMPRESSION_FORMAT_QUESTION))
        compress = False
        while True:
            should_compress = pt.prompt(YES_NO_PROMPT, validator=OutputValidator()).strip()
            if should_compress.lower().strip() in YES:
                compress = True
                break
            elif should_compress.lower().strip() in NO:
                compress = False
                break
            print(INVALID_INPUT_MESSAGE)

        if compress:
            while True:
                compression_format = pt.prompt(COMPRESSION_FORMAT_PROMPT,
                                               validator=OutputValidator()).strip()
                if compression_format.lower() in COMPRESSION_FORMAT:
                    break
                else:
                    print_formatted_text(HTML(UNSUPPORTED_FORMAT_MESSAGE))
            self.compress_format = compression_format

    def get_data_from_local_file(self, input_source: str) -> None:
        if input_source.endswith(".gz"):
            # The file is compressed gzip
            with gzip.open(input_source, "rt", encoding='utf-8') as file:
                self.data = file.read()
        elif input_source.endswith(".bz2"):
            # The file is compressed with bzip2
            with bz2.open(input_source, "rt", encoding='utf-8') as file:
                self.data = file.read()
        elif input_source.endswith(".xz"):
            # The file is compressed with lzma
            with lzma.open(input_source, ".xz", encoding='utf-8') as file:
                self.data = file.read()
        # elif input_source.endswith(".zip"):
        #     # The file is compressed with zip
        #     with zipfile.ZipFile(input_source, "r") as zfile:
        #         for name in zfile.namelist():
        #             with zfile.open(name) as file:
        #                 self.data[name] = file.read().decode()
        else:
            # The file is uncompressed
            with open(input_source, "r", encoding='utf-8') as file:
                self.data = file.read()
        self.convert_to_df()

    def get_data_from_api(self, input_source: str) -> None:
        http = urllib3.PoolManager()

        try:
            response = http.request("GET", input_source)
        except HTTPError as e:
            print(f"HTTP request failed: {e}")
            return

        if response.status == 200:
            encoding = 'utf-8'  # Default encoding to use if not specified in headers
            # self.data = pd.read_json(StringIO(response.data.decode('utf-8')))
            self.data = json.loads(response.data.decode('utf-8'))
            self.convert_to_df()

        else:
            print(f"API request failed with status code {response.status}")

    def convert_to_df(self) -> None:
        if self.input_locally:
            data_io = StringIO(self.data)
            self.data = pd.read_csv(data_io, sep="\t", dtype=str)
        else:
            if isinstance(self.data, list):
                dfs = []
                for item in self.data:
                    flattened_data = parse_nested_json_to_dataframe(item)
                    df = pd.DataFrame([flattened_data])
                    dfs.append(df)

                # Concatenate the DataFrames to handle multiple elements in the list
                result_df = pd.concat(dfs, ignore_index=True)
            else:
                # Parse as a single JSON object
                flattened_data = parse_nested_json_to_dataframe(self.data)
                result_df = pd.DataFrame([flattened_data])
            self.data = result_df

    def clean(self) -> None:
        print(CLEANING_MESSAGE)
        df = self.data
        # Remove non letters and symbols
        # Keeping only letters including accented ones and numbers
        if self.input_locally:
            df.dropna(inplace=True)
            df.drop_duplicates(inplace=True)
            for col in df.columns:
                # we are keeping - and ' for this
                df[col] = df[col].apply(lambda x: re.sub(r'[^a-zA-Z0-9à-ÿ\'-]+', ' ', x))
        else:
            df.drop_duplicates(inplace=True)
            for col in {"name", "description", "product_type"}:
                df[col] = df[col].apply(lambda x: re.sub(r'[^a-zA-Z0-9à-ÿ]+', ' ', x))

    def load(self) -> None:
        print_formatted_text(HTML(LOADING_MESSAGE))
        if self.input_locally:
            self.get_data_from_local_file(self.input)
        else:
            print_formatted_text(HTML(FETCH_API_MESSAGE))
            self.get_data_from_api(self.input)
        print_formatted_text(HTML(LOAD_SUCCESSFUL_MESSAGE))

    def export(self, name) -> None:
        print(EXPORTING_MESSAGE)
        df = self.data

        if self.output_locally:
            path = os.path.join(self.output, f"{name}.{self.out_format}")
        else:
            path = f"{name}.{self.out_format}"

        if self.out_format == "csv":
            df.to_csv(path, index=False)
        elif self.out_format == "parquet":
            df.to_parquet(path, index=False)
        elif self.out_format == "xlsx":
            df.to_excel(path, index=False)
        else:
            print_formatted_text(HTML(EXPORTING_ERROR_MESSAGE))
            return

        if self.compress_format != "":
            path = self.compress(path)

        if not self.output_locally:
            upload_to_s3(path, self.output)
            os.remove(path)  # clean up
        print(EXPORT_SUCCESSFUL_MESSAGE)

    def compress(self, path: str) -> str:
        print(COMPRESSING_MESSAGE)
        compression_format = self.compress_format
        output_path = f"{path}.{compression_format}"
        if compression_format == "gz":
            with open(path, 'rb') as f_in, gzip.open(output_path, 'wb') as f_out:
                f_out.writelines(f_in)

        elif compression_format == "bz2":
            with open(path, 'rb') as f_in, bz2.BZ2File(output_path, 'wb') as f_out:
                f_out.writelines(f_in)

        elif compression_format == "xz":
            with open(path, 'rb') as f_in, lzma.open(output_path, 'wb') as f_out:
                f_out.writelines(f_in)
        os.remove(path)  # clean up
        return output_path  # return the updated compressed path


def parse_nested_json_to_dataframe(json_data, prefix='') -> dict:
    flattened_data = {}

    if isinstance(json_data, list):
        for i, item in enumerate(json_data):
            element_prefix = f"{prefix}{i}_"
            flattened_data.update(parse_nested_json_to_dataframe(item, element_prefix))
    elif isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, dict):
                # If the value is a dictionary, recursively call the function with an updated prefix
                flattened_data.update(parse_nested_json_to_dataframe(value, f"{prefix}{key}_"))
            elif isinstance(value, list):
                # If the value is a list, create a separate row for each element
                for i, element in enumerate(value):
                    element_prefix = f"{prefix}{key}_{i}_"
                    flattened_data.update(parse_nested_json_to_dataframe(element, element_prefix))
            else:
                flattened_data[f"{prefix}{key}"] = value

    return flattened_data
