import unittest
import os
from common import Common

bucket = "myawsbucket-jerome"  # change me


class CommonTest(unittest.TestCase):

    def test_aws_config(self):
        from service.s3_service import verify_config
        self.assertIsNone(verify_config())

    def test_get_data_from_local_file_uncompressed(self):
        app = Common()
        file_path = os.path.join("example_data", "data.tsv")
        app.get_data_from_local_file(file_path)
        # Assuming that the method returns a dataframe, we can check if it's empty
        self.assertFalse(app.data.empty, "Dataframe is empty")

    def test_get_data_from_local_file_compressed(self):
        app = Common()
        file_path = os.path.join("example_data", "title.basics.tsv.gz")
        app.get_data_from_local_file(file_path)
        print(app.data.iloc[:, 3])
        # Assuming that the method returns a dataframe, we can check if it's empty
        self.assertFalse(app.data.empty, "Dataframe is empty")

    def test_get_from_api(self):
        app = Common()
        app.input_locally = False
        api = "http://makeup-api.herokuapp.com/api/v1/products.json?brand=maybelline"
        app.get_data_from_api(api)
        self.assertFalse(app.data.empty, "Dataframe is empty")

    # Uncompressed Input and Output
    def test_write_to_csv(self):
        app = Common()
        app.out_format = "csv"

        app.input_locally = True
        app.input = os.path.join("example_data", "data.tsv")
        app.output_locally = os.path.join("example_data", "result")
        app.get_data_from_local_file(app.input)
        app.clean()
        app.export("from_uncompressed_tsv_to_csv")
        self.assertFalse(app.data.empty, "Dataframe is empty")

        app.input_locally = False
        api = "http://makeup-api.herokuapp.com/api/v1/products.json?brand=maybelline"
        app.get_data_from_api(api)
        app.clean()
        app.export("from_api_to_csv")
        self.assertFalse(app.data.empty, "Dataframe is empty")

    def test_write_to_parquet(self):
        app = Common()
        app.out_format = "parquet"

        app.input_locally = True
        app.input = os.path.join("example_data", "data.tsv")
        app.output_locally = os.path.join("example_data", "result")
        app.get_data_from_local_file(app.input)
        app.clean()
        app.export("from_uncompressed_tsv_to_parquet")
        self.assertFalse(app.data.empty, "Dataframe is empty")

        app.input_locally = False
        api = "http://makeup-api.herokuapp.com/api/v1/products.json?brand=maybelline"
        app.get_data_from_api(api)
        app.clean()
        app.export("from_api_to_parquet")
        self.assertFalse(app.data.empty, "Dataframe is empty")

    # Uncompressed input compressed output
    def test_write_to_csv_gz(self):
        app = Common()
        app.out_format = "csv"
        app.compress_format = "gz"

        app.input_locally = True
        app.input = os.path.join("example_data", "data.tsv")
        app.output_locally = os.path.join("example_data", "result")
        app.get_data_from_local_file(app.input)
        app.clean()
        app.export("from_uncompressed_tsv_to_csv")
        self.assertFalse(app.data.empty, "Dataframe is empty")

        app.input_locally = False
        api = "http://makeup-api.herokuapp.com/api/v1/products.json?brand=maybelline"
        app.get_data_from_api(api)
        app.clean()
        app.export("from_api_to_csv")
        self.assertFalse(app.data.empty, "Dataframe is empty")

    def test_write_to_csv_bz2(self):
        app = Common()
        app.out_format = "csv"
        app.compress_format = "bz2"

        app.input_locally = True
        app.input = os.path.join("example_data", "data.tsv")
        app.output_locally = os.path.join("example_data", "result")
        app.get_data_from_local_file(app.input)
        app.clean()
        app.export("from_uncompressed_tsv_to_csv")
        self.assertFalse(app.data.empty, "Dataframe is empty")

        app.input_locally = False
        api = "http://makeup-api.herokuapp.com/api/v1/products.json?brand=maybelline"
        app.get_data_from_api(api)
        app.clean()
        app.export("from_api_to_csv")
        self.assertFalse(app.data.empty, "Dataframe is empty")

    def test_write_to_csv_xz(self):
        app = Common()
        app.out_format = "csv"
        app.compress_format = "xz"

        app.input_locally = True
        app.input = os.path.join("example_data", "data.tsv")
        app.output_locally = os.path.join("example_data", "result")
        app.get_data_from_local_file(app.input)
        app.clean()
        app.export("from_uncompressed_tsv_to_csv")
        self.assertFalse(app.data.empty, "Dataframe is empty")

        app.input_locally = False
        api = "http://makeup-api.herokuapp.com/api/v1/products.json?brand=maybelline"
        app.get_data_from_api(api)
        app.clean()
        app.export("from_api_to_csv")
        self.assertFalse(app.data.empty, "Dataframe is empty")

    def test_upload_to_s3(self):
        # API call -> process -> csv -> compress -> upload to S3
        app = Common()
        app.out_format = "csv"
        app.output_locally = bucket
        app.compress_format = "bz2"

        app.input_locally = False
        api = "http://makeup-api.herokuapp.com/api/v1/products.json?brand=maybelline"
        app.get_data_from_api(api)
        app.clean()
        app.export("from_api_to_csv")
        self.assertFalse(app.data.empty, "Dataframe is empty")


if __name__ == '__main__':
    unittest.main()
