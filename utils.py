# MADE BY DANIEL NACHUM @ https://github.com/danielnachumdev
from platform import uname
import os
import filecmp

TNI = 0  # Test number index
TTI = 1  # test target index
TCI = 2  # test command index
RANDOM = "sdfgjyuasdfgpiharpiguhaprughdakjhfbga"
PASSED = "PASSED"
FAILED = "FAILED"
VALGRIND_ERROR = "VALGRIND ERROR"


def cm(cm: str) -> int:
    return os.system(cm)


def dir_files(path: str):
    '''
    Get all files from a directory

    Arguments:
        path {str} -- Path to the directory

    Returns:
        list[str] -- List of all files in the directory
    '''
    res = []
    for f in os.listdir(path):
        p = path+f
        if os.path.isfile(p):
            res.append(p)
    return res


def f_exists(path: str) -> bool:
    '''
    Check if a file exists and is not a directory before using it

    Arguments:
        path {str} -- Path to the file to check

    Returns:
        bool -- True if the path is a file, False otherwise
    '''
    return os.path.isfile(path)


def d_file(path: str) -> None:
    if f_exists(path):
        os.remove(path)


def f_name(path: str) -> str:
    """
    Get the name of a file"""
    return os.path.basename(path)


def f_type(path: str) -> str:
    '''
    Get thetype of a file

    Arguments:
        path {str} -- Path to the file

    Returns:
        str -- The file type
    '''
    return os.path.splitext(path)[1]


def f_conts(path: str):
    """
    Get the contents of a file"""
    if f_exists(path):
        with open(path, 'r') as f:
            return f.readlines()
    else:
        raise FileNotFoundError(f"{path} not found")


def are_files_contents_the_same(path1: str, path2: str) -> bool:
    try:
        if filecmp.cmp(path1, path2, shallow=False):
            return True
    except FileNotFoundError:
        print("At least one of the given files was not found.")
    return False


def is_line_longer_than(line: str, length: int) -> bool:
    return len(line) >= length


def is_in_wsl() -> bool:
    return 'microsoft-standard' in uname().release


def print_array(array: list) -> None:
    for i in array:
        print(i.strip())


def __is_installed(name: str) -> bool:
    def is_valid_version(version):
        for c in version:
            if c not in "0123456789.":
                return False
        return True
    tmp = f"{RANDOM}.txt"
    cm(f"{name} --version >{tmp}")
    output = f_conts(tmp)[0]  # EXAMPLE_OUTPUT = "valgrind-3.15.0\n"
    d_file(tmp)
    if output.count("\n") == 1 and output[-1:] == "\n":
        output = output.strip('\n')
    else:
        return False
    if name in ["valgrind", "make", "gcc"]:
        if name == "valgrind":
            version = output.split("-")[-1]
        else:
            version = output.split(" ")[-1]
        if is_valid_version(version):
            return True
    else:
        raise NotImplementedError(f"{name} is not supported")
    return False


IS_VALGRIND_INSTALLED = __is_installed("valgrind")
IS_MAKE_INSTALLED = __is_installed("make")
IS_GCC_INSTALLED = __is_installed("gcc")


def is_valgrind_result_ok(vlg):
    return "ERROR SUMMARY: 0 errors from 0 contexts" in vlg[-1]