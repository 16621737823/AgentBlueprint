def get_version_uuid(package_name:str):
    with open("load_modules/version.txt", "r") as file:
        for line in file:
            if package_name in line:
                return line.split(":")[1].strip()