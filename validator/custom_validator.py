import os


class CustomValidator:

    @staticmethod
    def path_validate(path: str) -> str:
        """
        try:
            path = validate_path(" my /path /with spaces ")
            print(f"The path {path} is valid.")
        except FileNotFoundError as e:
            print(e)
        :param path:
        :return:
        """
        # Remove spaces from the path
        path = path.replace(" ", "")

        # Check if the path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path {path} does not exist.")

        return path
