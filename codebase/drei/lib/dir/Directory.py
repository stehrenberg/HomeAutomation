import os

__author__ = 's.jahreiss'


def get_file_list(dir_path, file_extensions):
    """
    Returns a list of all available sounds in the file system.
    :return: All available sounds in the filesystem.
    """
    files = []
    for file_name in os.listdir(dir_path):
        for file_extension in file_extensions:
            if file_name.endswith(file_extension):
                files.append(file_name)
    return files
