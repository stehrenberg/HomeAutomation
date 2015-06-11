import os

__author__ = 's.jahreiss'


def get_file_list(dir_path, file_extensions):
    """
    Returns a list of all available files in the file system under the specified path with the specified file extensions.
    :return: All available files in the filesystem with the specified file extensions under the specified file path.
    """
    files = []
    for file_name in os.listdir(dir_path):
        for file_extension in file_extensions:
            if file_name.endswith(file_extension):
                files.append(file_name)
    return files
