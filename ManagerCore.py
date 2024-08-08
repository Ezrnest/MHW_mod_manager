import datetime
import shutil
import io
import os
import sys
import traceback
import winreg
import zipfile
from typing import Sequence, List, Literal
from zipfile import ZipFile
import collections
import re
from pathlib import Path
import json

import vdf
from sortedcontainers import SortedSet

from FileTools import MRL3File, EPV3File, FileSystemZipWrapper, SevenZipZipWrapper

部位ID_名称_map = {0: '头盔', 1: '身体', 2: '护手', 3: '腰部', 4: '护腿'}
部位ID_路径_map = {0: 'helm', 1: 'body', 2: 'arm', 3: 'wst', 4: 'leg'}
部位路径_ID_map = {v: k for k, v in 部位ID_路径_map.items()}

regex_pp = re.compile(
    r"nativePC/pl/(?P<prefix>[mf])_equip/pl(?P<address>\d{3}_\d{4})/(?P<part>arm|body|helm|leg|wst)")


def get_steam_path():
    try:
        # Open the registry key where Steam stores its installation path
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
        return steam_path
    except FileNotFoundError:
        return "C:/Program Files (x86)/Steam"


def find_mhw_folder():
    # Path to the Steam installation folder
    steam_path = get_steam_path()
    library_folders_file = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
    if not os.path.exists(library_folders_file):
        return None
    # Read the libraryfolders.vdf file
    with open(library_folders_file, 'r') as f:
        library_folders = vdf.load(f)
    # Iterate over each Steam library folder
    for path in library_folders['libraryfolders'].values():
        steamapps_path = os.path.join(path['path'], "steamapps")
        manifest_path = os.path.join(steamapps_path, "appmanifest_582010.acf")

        if os.path.exists(manifest_path):
            with open(manifest_path, 'r') as f:
                app_manifest = vdf.load(f)

            # Check if the installed game is MHW
            if app_manifest['AppState']['name'] == "Monster Hunter: World":
                return os.path.join(steamapps_path, "common", app_manifest['AppState']['installdir'])

    return None


def writeFileZip(zip_in, zip_out, in_path: str, out_path, path_processor):
    if out_path in zip_out.namelist():
        # print(f"文件已存在：{out_path}")
        return None
    file_data = zip_in.read(in_path)
    additional_files = []
    special_file = None
    if in_path.endswith(".mrl3"):
        special_file = MRL3File(file_data)
    elif in_path.endswith(".epv3"):
        special_file = EPV3File(file_data)
    else:
        zip_out.writestr(out_path, file_data)
    if special_file is not None:
        additional_files = special_file.get_ref_paths()
        special_file.process_references(path_processor)
        zip_out.writestr(out_path, special_file.to_bytes())
    return out_path, additional_files


def extract_zip_part_to_zip(zip_in, zip_out, in_pl_info, out_pl_info, part_id, in_content_root="",
                            info_io=sys.stdout):
    in_pl_prefix, in_pl_address = in_pl_info
    out_pl_prefix, out_pl_address = out_pl_info
    all_files = set(zip_in.namelist())
    in_content_folder = f"{in_content_root}nativePC/"

    # process first the files in in_part_path, adding extra files if necessary
    part_folder_name = 部位ID_路径_map[part_id]
    in_part_path = f"{in_content_folder}pl/{in_pl_prefix}_equip/pl{in_pl_address}/{part_folder_name}"
    remaining_files = SortedSet(f for f in zip_in.namelist() if f.startswith(in_part_path))

    def rel_path_processor(x):
        return (x.replace("\\", "/").replace(in_pl_prefix + "_", out_pl_prefix + "_")
                .replace(in_pl_address, out_pl_address))

    in_files = []
    out_files = []
    while remaining_files:
        in_path = remaining_files.pop(0)
        out_path = rel_path_processor(in_path[len(in_content_root):])
        res = writeFileZip(zip_in, zip_out, in_path, out_path, rel_path_processor)
        if not res:
            continue
        out_path, additional_files = res
        # print(f"{file_path} -> {out_path}")

        in_files.append(in_path)
        out_files.append(out_path)
        if additional_files:
            add_abs_path = [in_content_folder + f for f in additional_files]
            # print(additional_files)
            # print(all_files)
            intersection = all_files.intersection(add_abs_path)
            # print(f"intersection: {intersection}")
            remaining_files.update(intersection)

    return out_files


def open_folder_or_zip(file_path: str, mode: Literal["r", "w", "x", "a"] = "r", compression=zipfile.ZIP_DEFLATED):
    if os.path.isdir(file_path):
        return FileSystemZipWrapper(file_path, mode=mode, compression=compression)
    elif file_path.endswith(".zip"):
        return ZipFile(file_path, mode=mode, compression=compression)
    elif file_path.endswith(".7z"):
        return SevenZipZipWrapper(file_path, mode=mode)
    else:
        raise ValueError("Unsupported file type")


def analyze_pl(file_path):
    with open_folder_or_zip(file_path, "r") as zip_in:
        # noinspection PyTypeChecker
        all_files: list[str] = sorted(zip_in.namelist(), key=len)
    # find the first nativePC/
    root_folder = None
    for e in all_files:
        if e.startswith("nativePC/"):
            root_folder = ""
            break
        if "/nativePC/" in e:
            root_folder = e[:e.index("/nativePC/") + 1]
            break
    if root_folder is None:
        return None, SortedSet()
    pp_info_set = SortedSet()
    for file in all_files:
        if not file.startswith(root_folder):
            continue
        match = regex_pp.match(file[len(root_folder):])
        if not match:
            continue
        pp_info_set.add((match.group("prefix"), match.group("address"), 部位路径_ID_map[match.group("part")]))
    return root_folder, pp_info_set


def output_single_pl_zip(in_zip_path, rep_info_list, zip_out, files_modified: set, in_content_root=""):
    with open_folder_or_zip(in_zip_path, "r") as zip_in:
        for partId, in_pl_info, out_pl_info in rep_info_list:
            partId_list = [partId] if partId is not None else range(5)
            for i in partId_list:
                out = extract_zip_part_to_zip(zip_in, zip_out, in_pl_info, out_pl_info, i,
                                              in_content_root=in_content_root)
                if out:
                    files_modified.update(out)


def single_pl_zip(in_zip_path, rep_info_list, out_zip_path, info_io=sys.stdout, in_content_root=""):
    with ZipFile(out_zip_path, "w") as zip_out:
        output_single_pl_zip(in_zip_path, rep_info_list, zip_out, set(), in_content_root=in_content_root)
        files = zip_out.namelist()
    print(f"处理文件完毕：[{in_zip_path}]->[{out_zip_path}]", file=info_io)
    return files


def single_pl_folder(in_zip_path, rep_info_list, out_folder, info_io=sys.stdout, in_content_root=""):
    with FileSystemZipWrapper(out_folder, "w") as zip_out:
        output_single_pl_zip(in_zip_path, rep_info_list, zip_out, set(), in_content_root=in_content_root)
        files = zip_out.namelist()
    print(f"处理文件完毕：[{in_zip_path}]->[{out_folder}]", file=info_io)
    return files


def mixture_pl_zip(info_list: list[dict], zip_out_path, info_io=sys.stdout):
    # check
    for info in info_list:
        if Path(zip_out_path) == Path(info["src_path"]):
            print(f"导出文件与输入文件相同：{zip_out_path}", file=info_io)
            return None
    # make dirs
    os.makedirs(os.path.dirname(zip_out_path), exist_ok=True)
    files = set()
    with ZipFile(zip_out_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_out:
        for info in info_list:
            in_zip_path = info["src_path"]
            content_root = info.get("in_content_root", "")
            rep_info_list = info["rep_info"]
            output_single_pl_zip(in_zip_path, rep_info_list, zip_out, files, in_content_root=content_root)
    return files


def process_simple_pl_zip(in_zip_path, out_path, target_pl_info=("m", "105_0000"), info_io=sys.stdout,
                          in_content_root=""):
    root_folder, pl_parts = analyze_pl(in_zip_path)
    if len(pl_parts) == 0:
        print(f"未找到装备文件：{in_zip_path}", file=info_io)
        return None
    in_pl_pre, in_pl_add, _ = pl_parts.pop()
    in_pl_info = (in_pl_pre, in_pl_add)
    rep_info_list = [(i, in_pl_info, target_pl_info) for i in range(5)]
    if out_path.endswith(".zip"):
        single_pl_zip(in_zip_path, rep_info_list, out_path, info_io=info_io, in_content_root=in_content_root)
    else:
        single_pl_folder(in_zip_path, rep_info_list, out_path, info_io=info_io, in_content_root=in_content_root)


def cleanup_files(mod_files: Sequence[str], root_folder: str):
    # sort by length in descending order so that subfolders are processed first
    mod_files = sorted([f for f in mod_files if f.startswith("nativePC/")], key=len, reverse=True)

    for file in mod_files:
        abs_path = os.path.join(root_folder, file)
        if not os.path.exists(abs_path):
            continue
        if file.endswith("/"):
            if not os.listdir(abs_path):
                os.rmdir(abs_path)
                # print(f"Removing {file}")
        else:
            os.remove(abs_path)
            # print(f"Removing {file}")


def findAvailableFilename(folder, prefix="Mod_", suffix=".zip"):
    files = set(os.listdir(folder))
    for i in range(1, 2 ** 31):
        new_file = f"{prefix}{i}{suffix}"
        if new_file not in files:
            return new_file
    return None


def find_top_subfolders(root_folder, target_name) -> list[str]:
    result = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Check if target_name is in the current list of subdirectories
        if target_name in dirnames:
            # Append the path of the found subfolder
            result.append(os.path.join(str(dirpath), target_name))
            # Remove the found folder from the list to prevent deeper search within it
            dirnames.remove(target_name)
    return result


def find_mods_from_shouji(root_folder):
    native_pc_list = find_top_subfolders(root_folder, "nativePC")
    resulting_mods = []
    for path in native_pc_list:
        p = Path(path)
        if p.parent.name != "files":
            continue
        src_folder = p.parent.parent
        path_info_xml = src_folder / "info.xml"
        if not path_info_xml.exists():
            continue
        # with open(path_info_xml, "r") as f:
        #     text = f.read()
        import xml.etree.ElementTree as ET
        tree = ET.parse(path_info_xml)
        root = tree.getroot()
        name_node = root.find("moduleName")
        if name_node is None:
            continue
        name = name_node.text
        resulting_mods.append((name, p.parent))
    return resulting_mods


def ppInfoEncode(pp_info):
    prefix, address, part_id = pp_info
    if part_id is None:
        part_id = ""
    return f"{prefix}.{address}.{part_id}"


def ppInfoDecode(pp_info_text):
    prefix, address, part_id = pp_info_text.split(".")
    if len(part_id) == 0:
        part_id = None
    else:
        part_id = int(part_id)
    return prefix, address, part_id


def plInfoDecode(pl_info_text):
    prefix, address = pl_info_text.split(".")
    return prefix, address


def plInfoEncode(pl_info):
    prefix, address = pl_info
    return f"{prefix}.{address}"


class ManagerCore:
    PATH_PL_MAPPING = "data/pl_mapping.csv"
    PATH_MODS_FOLDER = "mods"
    PATH_CONFIG = "config.json"

    def __init__(self):
        self.config = {}
        self.init()

    def init(self):
        self.init_config()

    def init_config(self):
        try:
            with open(ManagerCore.PATH_CONFIG, 'r') as file:
                self.config = json.load(file)
                print("Loaded config")
                return
        except Exception as e:
            pass
        # if not os.path.exists(ManagerCore.PATH_CONFIG):
        self.config = {"game_root": None, "mods": {},
                       "history": {}
                       }
        self.save_config()
        return

    # def init_pl_mapping(self):
    #     self.pl_mapping = PL_MAPPING
    #     print("Loaded pl_mapping")

    def formatPlInfo(self, pl_info, details=True):
        prefix, path = pl_info
        from MHWData import PL_MAPPING
        name = PL_MAPPING[path]
        if prefix == "f":
            name += "[女]"
        elif prefix == "m":
            name += "[男]"
        if details:
            name += '(' + path + ')'
        return name

    def formatPPInfo(self, pp_info, details=True):
        prefix, address, part_id = pp_info
        from MHWData import PP_MAPPING
        text = PP_MAPPING[part_id][address]
        if prefix == "f":
            text += "[女]"
        elif prefix == "m":
            text += "[男]"
        if details:
            text += '(' + address + ')'
        return text

    def is_game_root_valid(self, game_root):
        if game_root is None or not isinstance(game_root, str):
            return False
        if not os.path.exists(game_root):
            return False
        # must be a valid game root containing MonsterHunterWorld.exe
        return os.path.exists(os.path.join(game_root, "MonsterHunterWorld.exe"))

    def set_game_root(self, game_root):
        self.config["game_root"] = game_root
        self.save_config()
        return True

    def check_game_root(self, output_io=sys.stdout):
        root = self.config["game_root"]
        if root is None:
            try:
                root = find_mhw_folder()
            except Exception as e:
                root = None
            if not self.is_game_root_valid(root):
                root = None
            else:
                self.config["game_root"] = root

        valid = self.is_game_root_valid(root)
        if not valid:
            print("游戏根目录无效", file=output_io)
        return valid

    def save_config(self):
        with open(ManagerCore.PATH_CONFIG, 'w') as file:
            json.dump(self.config, file, indent=4, ensure_ascii=False)

    def modAddFromFile(self, source_path, mod_name=None, replace=False, output_io=sys.stdout):
        config = self.config
        if mod_name is None:
            zip_file_name = os.path.basename(source_path)
            mod_name = os.path.splitext(zip_file_name)[0]
        # check the name is unique
        if mod_name in config["mods"].keys():
            if replace:
                print(f"<{mod_name}>已存在，将替换之前的模组", file=output_io)
            else:
                print(f"<{mod_name}>已存在，跳过", file=output_io)
                return

        content_root, pp_info_set = analyze_pl(source_path)
        # print(content_root, pp_info_set)
        if len(pp_info_set) == 0:
            print(f"警告：<{mod_name}>中未找到有效的防具文件，跳过", file=output_io)
            return
        # copy the zip file to the mod folder
        os.makedirs(ManagerCore.PATH_MODS_FOLDER, exist_ok=True)

        # create the folder if necessary
        rep_info = [(part_id, (prefix, address), (prefix, address)) for prefix, address, part_id in pp_info_set]
        # print(rep_info)
        info_dict = {
            "src_path": source_path,
            "in_content_root": content_root,
            "rep_info": rep_info
        }
        storage_path = os.path.join(ManagerCore.PATH_MODS_FOLDER, f"{mod_name}.zip")
        if os.path.exists(storage_path):
            storage_path = findAvailableFilename(ManagerCore.PATH_MODS_FOLDER, suffix=".zip")
        try:
            res = mixture_pl_zip([info_dict], storage_path, info_io=output_io)
            if res is None:
                print(f"错误：添加<{mod_name}>失败", file=output_io)
                return
        except:
            traceback.print_exc(file=output_io)
            return
        self.modInitConfig(mod_name, pp_info_set)
        print(f"<{mod_name}>已添加", file=output_io)

    def modInitConfig(self, mod_name, pp_info_set):
        pl_info_source = [ppInfoEncode(pp_info) for pp_info in pp_info_set]
        pl_info_rep = {s: s for s in pl_info_source}
        pl_info = {
            "source": pl_info_source,
            "rep": pl_info_rep
        }
        mod_info = {
            "filename": f"{mod_name}.zip",
            "type": "pl",
            "pl_info": pl_info,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "loaded": False,
            "loaded_file_list": []
        }
        self.config["mods"][mod_name] = mod_info
        self.save_config()

    def modDelete(self, mod_name, output_io=sys.stdout):
        if mod_name not in self.config["mods"]:
            print(f"<{mod_name}>不存在", file=output_io)
            return
        if self.modIsLoaded(mod_name):
            print(f"错误：<{mod_name}>已加载，无法删除", file=output_io)
            # self.modUnload(mod_name, output_io=output_io)
            return
        info = self.config["mods"][mod_name]
        self.config["mods"].pop(mod_name)
        # delete file
        filename = info.get("filename", f"{mod_name}.zip")
        zip_file_path = os.path.join(ManagerCore.PATH_MODS_FOLDER, filename)
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
        print(f"<{mod_name}>已删除", file=output_io)
        self.save_config()

    def modGetRepInfo(self, mod_name):
        mod_info = self.config["mods"].get(mod_name)
        if mod_info is None:
            return None
        encoded_map = mod_info["pl_info"]["rep"]
        res = []
        for k, v in encoded_map.items():
            in_prefix, in_address, in_part_id = ppInfoDecode(k)
            out_prefix, out_address, out_part_id = ppInfoDecode(v)
            t = (in_part_id, (in_prefix, in_address), (out_prefix, out_address))
            res.append(t)
        return res

    def modExport(self, mod_name, export_folder="out", output_io=sys.stdout):
        if mod_name not in self.config["mods"]:
            print(f"<{mod_name}>不存在", file=output_io)
            return
        mod_info = self.config["mods"][mod_name]
        zip_file_path = os.path.join(ManagerCore.PATH_MODS_FOLDER, f"{mod_name}.zip")
        export_file_path = os.path.join(export_folder, f"{mod_name}.zip")
        rep_info = self.modGetRepInfo(mod_name)
        single_pl_zip(zip_file_path, rep_info, export_file_path)
        print(f"<{mod_name}>已导出到[{export_file_path}]", file=output_io)

    def getModDict(self) -> dict:
        return self.config["mods"]

    def getLoadedModDict(self) -> dict:
        mods = self.config["mods"]
        return {k: v for k, v in mods.items() if v.get("loaded")}

    def modExists(self, mod_name: str):
        return mod_name in self.config["mods"]

    def modGetZipPath(self, mod_name: str):
        mod_info = self.config["mods"].get(mod_name)
        if mod_info is None:
            return None
        filename = mod_info.get("filename", f"{mod_name}.zip")
        return os.path.join(ManagerCore.PATH_MODS_FOLDER, filename)

    def modLoad(self, mod_name: str, force_load=False, output_io=sys.stdout):
        if not self.check_game_root(output_io=output_io):
            return
        config = self.config
        game_root = config["game_root"]
        if mod_name not in config["mods"]:
            print(f"<{mod_name}>不存在", file=output_io)
            return
        mod_info = config["mods"][mod_name]
        if mod_info.get("loaded"):
            if force_load:
                print(f"<{mod_name}>已加载，正重新加载", file=output_io)
                self.modUnload(mod_name)
            else:
                print(f"<{mod_name}>已加载，不再重新加载", file=output_io)
                return
        # extract the zip file
        mod_zip_src = self.modGetZipPath(mod_name)
        rep_info = self.modGetRepInfo(mod_name)
        mod_files = single_pl_folder(mod_zip_src, rep_info, game_root)
        # check conflict

        # new_files = get_extract_filenames(zip_file_path, mod_info["pl_info"], mod_info["pl_target_info"])
        # new_files = set(filter(lambda x: not x.endswith("/"), new_files))
        # for name, info in self.getLoadedModDict().items():
        #     loaded_files = set(info["loaded_file_list"])
        #     if any(f in new_files for f in loaded_files):
        #         print(f"错误：<{mod_name}>与已加载的<{name}>存在冲突，无法加载", file=output_io)
        #         return

        # print(rep_info)
        # mod_files = extract_known_zip_to_target(zip_file_path, game_root, mod_info["pl_info"],
        #                                         mod_info["pl_target_info"])
        mod_info["loaded"] = True
        mod_info["loaded_file_list"] = list(mod_files)
        print(f"<{mod_name}>加载完毕", file=output_io)
        self.save_config()

    def modGetInfo(self, mod_name: str):
        return self.config["mods"].get(mod_name)

    def modIsLoaded(self, mod_name: str):
        if not self.modExists(mod_name):
            return False
        return self.config["mods"][mod_name].get("loaded")

    def modUnload(self, mod_name: str, output_io=sys.stdout):
        if not self.check_game_root(output_io=output_io):
            return
        config = self.config
        if mod_name not in config["mods"]:
            print(f"<{mod_name}>不存在", file=output_io)
            return
        mod_info = config["mods"][mod_name]
        if not mod_info.get("loaded"):
            print(f"<{mod_name}>未加载, 无需卸载", file=output_io)
            mod_info["loaded"] = False
            self.save_config()
            return
        game_root = config["game_root"]
        modified_files = mod_info["loaded_file_list"]
        cleanup_files(modified_files, game_root)
        mod_info["loaded"] = False
        mod_info["loaded_file_list"] = []
        print(f"<{mod_name}>已卸载", file=output_io)
        self.save_config()

    # def modReload(self, mod_name, output_io=sys.stdout):
    #     self.modUnload(mod_name, output_io=output_io)
    #     self.modLoad(mod_name, output_io=output_io)

    def modUnloadAll(self, output_io=sys.stdout):
        for mod_name in self.getLoadedModDict().keys():
            self.modUnload(mod_name, output_io=output_io)

    def modSetTarget(self, mod_name_list, target_pl_info, output_io=sys.stdout):
        for mod_name in mod_name_list:
            if not self.modExists(mod_name):
                print(f"<{mod_name}>不存在", file=output_io)
                continue
            mod_info = self.config["mods"][mod_name]
            sources = mod_info["pl_info"]["source"]
            target_prefix, target_address = target_pl_info
            rep_dict = {}
            for k in sources:
                src_pp = ppInfoDecode(k)
                target_pp = (target_prefix, target_address, src_pp[2])
                rep_dict[k] = ppInfoEncode(target_pp)
            mod_info["pl_info"]["rep"] = rep_dict
            print(f"<{mod_name}>目标防具设置为{self.formatPlInfo(target_pl_info)}", file=output_io)
        self.save_config()

    def modsSetPPTarget(self, mod_name_list, target_pp_dict, info_io=sys.stdout):
        for mod_name in mod_name_list:
            if not self.modExists(mod_name):
                print(f"<{mod_name}>不存在", file=info_io)
                continue
            mod_info = self.config["mods"][mod_name]
            sources = mod_info["pl_info"]["source"]
            rep_dict = {}
            for k in sources:
                src_pp = ppInfoDecode(k)
                target_pp = target_pp_dict.get(src_pp[2])
                if target_pp is None:
                    continue
                rep_dict[k] = ppInfoEncode(target_pp)
            mod_info["pl_info"]["rep"] = rep_dict
            print(f"<{mod_name}>设置完毕", file=info_io)

    def modRename(self, mod_name, new_name, info_io=sys.stdout):
        if not self.modExists(mod_name):
            print(f"错误：<{mod_name}>不存在", file=info_io)
            return
        if mod_name == new_name:
            print(f"<{mod_name}>已重命名为<{new_name}>", file=info_io)
            return

        if self.modExists(new_name):
            print(f"错误：名称<{new_name}>已存在", file=info_io)
            return

        mod_info = self.config["mods"][mod_name]
        del self.config["mods"][mod_name]
        self.config["mods"][new_name] = mod_info

        # keep the original file name
        # new_filename = f"{new_name}.zip"
        # old_file_path = os.path.join(ManagerCore.PATH_MODS_FOLDER, mod_info["filename"])
        # try:
        #     os.rename(old_file_path, os.path.join(ManagerCore.PATH_MODS_FOLDER, new_filename))
        # except OSError:
        #     new_filename = findAvailableFilename(ManagerCore.PATH_MODS_FOLDER)
        #     os.rename(old_file_path, os.path.join(ManagerCore.PATH_MODS_FOLDER, new_filename))
        # mod_info["filename"] = new_filename
        #

        print(f"<{mod_name}>已重命名为<{new_name}>", file=info_io)
        self.save_config()

    def modMixtureExport(self, mixture_list, mod_name, save=True, export_file=None, info_io=sys.stdout):
        # group mixture list by name
        d = collections.defaultdict(list)
        for src_name, rep_pp_info in mixture_list:
            d[src_name].append(rep_pp_info)
        full_info_list = []
        for src_name, target_pp_info_list in d.items():
            mod_info = self.modGetInfo(src_name)
            sources = [ppInfoDecode(s) for s in mod_info["pl_info"]["source"]]
            # match rep_pp_info_list and sources by part_id
            rep_info_list = []
            d_src = {pp_info[2]: pp_info[:2] for pp_info in sources}
            d_target = {pp_info[2]: pp_info[:2] for pp_info in target_pp_info_list}
            for part_id in d_src.keys() & d_target.keys():
                rep_info_list.append((part_id, d_src[part_id], d_target[part_id]))
            filepath = self.modGetZipPath(src_name)
            info_dict = {"src_path": filepath, "rep_info": rep_info_list}
            full_info_list.append(info_dict)
        dest = None
        if save:
            if self.modExists(mod_name):
                info_io.write(f"错误：<{mod_name}>已存在!")
                return
            dest = os.path.join(ManagerCore.PATH_MODS_FOLDER, f"{mod_name}.zip")
            mixture_pl_zip(full_info_list, dest, info_io=info_io)
            _, pp_info_set = analyze_pl(dest)
            self.modInitConfig(mod_name, pp_info_set)
        if export_file:
            os.makedirs(os.path.dirname(export_file), exist_ok=True)
            if dest:
                # copy the file
                shutil.copy(dest, export_file)
            else:
                mixture_pl_zip(full_info_list, export_file, info_io=info_io)

    def getRecentPl(self):
        return [plInfoDecode(x) for x in self.config.get("recent_pl", [])]

    def addRecentPl(self, pl_info):
        pl_text = plInfoEncode(pl_info)
        self.config["recent_pl"] = [pl_text] + [x for x in self.config.get("recent_pl", []) if x != pl_text][:10]
        self.save_config()

    def getPresetSuite(self):
        return self.config.get("preset_suite", [])

    def setPredefinedSuite(self, suite_list):
        self.config["preset_suite"] = suite_list
        self.save_config()

    # def getRecentPP(self):
    #     return [ppInfoDecode(x) for x in self.config.get("recent_pp", [])]
    #
    # def addRecentPP(self, pp_info):
    #     recent_pp = self.getRecentPP()
    #     recent_pp = [pp_info] + [x for x in recent_pp if x != pp_info][:5]
    #     self.config["recent_pp"] = [ppInfoEncode(x) for x in recent_pp]
    #     self.save_config()
