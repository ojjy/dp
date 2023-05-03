import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def set_downloads_folder(system_name, table_name):
    """
    set downloads folder
    system_name = "hira"||"datagokr"
    :param system_name:
    :return:
    """
    # project폴더의 하위downloads폴더
    downloads_folder = os.path.join(project_path, "downloads")
    system_folder = os.path.join(downloads_folder, system_name)
    table_name_folder = os.path.join(system_folder, table_name)
    download_folder_fullpath = table_name_folder
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    if not os.path.exists(system_folder):
        os.makedirs(system_folder)
    if not os.path.exists(table_name_folder):
        os.makedirs(table_name_folder)

    print(f"{download_folder_fullpath} download folder fullpath: {download_folder_fullpath}")
    return download_folder_fullpath