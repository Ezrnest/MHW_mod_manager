import os.path
import zipfile
from pathlib import Path
from typing import Sequence, List, Collection

from sortedcontainers import SortedSet


class SpecialFileWithReferences:
    def __init__(self, binary_data: bytes):
        pass
        self.references = []

    def to_bytes(self):
        pass

    def process_references(self, func):
        self.references = [func(string) for string in self.references]

    def get_ref_paths(self):
        """
        Get the paths of the references under the nativePC folder
        :return:
        """
        pass


def add_ref_path_suffix(lst, suffix=""):
    path_list = []
    for s in lst:
        s = s.replace('\\', '/')
        if s.endswith('/'):
            path_list.append(s)
        else:
            path_list.append(s + suffix)
    return path_list


class MRL3File(SpecialFileWithReferences):
    FILE_PATH_PREFIX = b'\xEB\x5D\x1F\x24\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    def __init__(self, binary_data: bytes):
        super().__init__(binary_data)
        self.binary_contents = None
        self.read_file(binary_data)

    def read_file(self, data: bytes):
        binary_contents = []
        strings = []
        pos = 0
        while True:
            npos = data.find(MRL3File.FILE_PATH_PREFIX, pos)
            if npos == -1:
                break
            binary_contents.append(data[pos:npos])
            pos = npos
            string_start = pos + len(MRL3File.FILE_PATH_PREFIX)
            string_end = data.find(0, string_start)
            string_bytes = data[string_start:string_end]
            string_value = string_bytes.decode('utf-8')
            strings.append(string_value)
            pos = string_end

        binary_contents.append(data[pos:])
        self.binary_contents = binary_contents
        self.references = strings

    def save_file(self, output_path):
        with open(output_path, 'wb') as file:
            file.write(self.to_bytes())

    def to_bytes(self):
        # insert the strings back into the binary data
        data = b''
        for i, string in enumerate(self.references):
            data += self.binary_contents[i]
            data += MRL3File.FILE_PATH_PREFIX
            data += string.encode('utf-8')
        data += self.binary_contents[-1]
        return data

    def get_ref_paths(self):
        return add_ref_path_suffix(self.references, ".tex")


class EPV3File(SpecialFileWithReferences):
    FILE_PREFIX = b'\x65\x70\x76\x00\x33\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x65\x00'

    def __init__(self, binary_data: bytes):
        super().__init__(binary_data)
        if not binary_data.startswith(EPV3File.FILE_PREFIX):
            raise ValueError("Invalid EPV3 file")

        refs = []
        str_start = len(EPV3File.FILE_PREFIX)
        while True:
            str_end = binary_data.find(0, str_start)
            if str_end == str_start:
                break
            string = binary_data[str_start:str_end].decode('utf-8')
            refs.append(string)
            str_start = str_end + 1
        self.references = refs
        self.remaining_data = binary_data[str_end:]

    def to_bytes(self):
        data = EPV3File.FILE_PREFIX
        for ref in self.references:
            data += ref.encode('utf-8')
            data += b'\x00'
        data += self.remaining_data
        return data

    def get_ref_paths(self):
        return add_ref_path_suffix(self.references, ".efx")


def listAllFiles(folder) -> List[str]:
    relative_files = []
    for root, dirs, file in os.walk(folder):
        root = str(root)
        for f in file:
            relative_files.append(os.path.relpath(os.path.join(root, f), folder).replace("\\", "/"))
        for d in dirs:
            relative_files.append(os.path.relpath(os.path.join(root, d), folder).replace("\\", "/") + "/")
    return relative_files


class FileSystemZipWrapper:
    def __init__(self, root_folder, mode='r', *args, **kwargs):
        self.root_folder = Path(root_folder)
        self.files = SortedSet()
        self.mode = mode
        if 'r' in mode:
            self.files = SortedSet(listAllFiles(root_folder))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def writestr(self, path, data):
        # print(path)
        dest = self.root_folder / path
        # print(dest,dest.is_dir())
        path.replace("\\", "/")
        self.files.add(path)
        if path.endswith("/"):
            dest.mkdir(parents=True, exist_ok=True)
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, 'wb') as f:
            f.write(data)

    def read(self, path):
        dest = self.root_folder / path
        if dest.is_dir():
            return b''
        with open(self.root_folder / path, 'rb') as f:
            return f.read()

    def namelist(self) -> Collection[str]:
        return self.files


from py7zr import SevenZipFile


class SevenZipZipWrapper:
    def __init__(self, path, mode='r', *args, **kwargs):
        if mode != "r":
            raise ValueError("Only read mode is supported for 7z files")
        self.path = path
        self.file_dict = None
        self.filenames = set()
        with SevenZipFile(path, "r") as z:
            for info in z.list():
                name = info.filename
                if info.is_directory and not name.endswith("/"):
                    name += "/"
                self.filenames.add(name)

    def init_files(self):
        if self.file_dict is not None:
            return
        path = self.path
        file_dict = {}
        with SevenZipFile(path, "r") as z:
            for k, v in z.readall().items():
                file_dict[k] = v.read()
        # add directories
        for name in self.filenames:
            if name in file_dict:
                continue
            file_dict[name] = b''
        self.file_dict = file_dict

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def writestr(self, path, data):
        raise ValueError("Writing to 7z files is not supported")

    def read(self, path):
        self.init_files()
        return self.file_dict[path]

    def namelist(self):
        return self.filenames
