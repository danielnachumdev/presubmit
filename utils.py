# MADE BY DANIEL NACHUM @ https://github.com/danielnachumdev
from platform import uname
import os
import filecmp

DEFAULT_TESTS_PATH = "./extracts/io/"
DEFAULT_ARG_TYPE = ".arg"
DEFAULT_IN_TYPE = ".in"
DEFUALT_OUT_TYPE = ".stdout"
PRINT_CENTER = 80
TNI = 0  # Test number index
TTI = 1  # test target index
TCI = 2  # test command index
RANDOM = "sdfgjyuasdfgpiharpiguhaprughdakjhfbga"
PASSED = "PASSED"
FAILED = "FAILED"
VALGRIND_ERROR = "VALGRIND ERROR"
__VERSION_URL = "https://raw.githubusercontent.com/danielnachumdev/presubmit/main/version"
__LATEST_VERSION_ERROR = -1
CURRENT_VERSION = 1.01


def proccess_command_line_arguments(args):
    if(len(args) <= 0):
        return DEFAULT_TESTS_PATH, DEFAULT_ARG_TYPE, DEFAULT_IN_TYPE, DEFUALT_OUT_TYPE
    FLAGS = ["-t", "-a", "-i", "-o"]
    FLAGS_EXPLANATIONS = ["the path to the folder that the tests are in", "the type of file that has the arguments",
                          "the type of file for the input data", "the type of file for the expected output"]
    exit_early: bool = False
    i = 0
    while i < len(args):
        arg = args[i]
        if "-" in arg:
            if arg not in FLAGS:
                print(f"UNKOWN FLAG: {arg}")
                exit_early = True
            else:
                if i + 1 >= len(args) or args[i+1] in FLAGS:
                    print(f"NO ARGUMENT FOR {arg}")
                    exit_early = True
                else:
                    if arg == "-t":
                        tests_path = args[i+1]
                    elif arg == "-a":
                        ARGUMENTS_FILE_PATH = args[i+1]
                    elif arg == "-i":
                        INPUT_FILE_PATH = args[i+1]
                    elif arg == "-o":
                        OUTPUT_FILE_PATH = args[i+1]
                    i += 1
        i += 1
    if exit_early:
        print("USAGE: python3 presubmit.py -t <tests_folder_path> -a <arguments_file_type> -i <input_file_type> -o <output_file_type>")
        exit(0)
    print("HEYYYYYYY")


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


def __get_latest_version() -> float:

    def __get_current_folder() -> str:
        return os.path.dirname(os.path.realpath(__file__))

    try:
        path = f"{__get_current_folder()}//{RANDOM}"
        cm(f"curl -s {__VERSION_URL} > {path}")
        version = float(f_conts(path)[0])
        return version, None
    except Exception as e:
        return __LATEST_VERSION_ERROR, e
    finally:
        d_file(path)


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
        p = path + f
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
    return 'Linux' == uname().system


def print_array(array: list) -> None:
    for i in array:
        print(i.strip())


def is_valgrind_result_ok(vlg):
    return "ERROR SUMMARY: 0 errors from 0 contexts" in vlg[-1]


def verify_version():
    if LATEST_VERSION == __LATEST_VERSION_ERROR:
        print(f"VERSION CHECK ERROR: {__LATEST_VERSION_ERROR}")
        return

    if CURRENT_VERSION < LATEST_VERSION:
        print("VERSION WARNING".center(PRINT_CENTER, "-"))
        print(
            f"Your version is {CURRENT_VERSION} and the latest version is {LATEST_VERSION}")
        print("Please update to the latest version")
        return


IS_VALGRIND_INSTALLED = __is_installed("valgrind") if is_in_wsl() else False
IS_MAKE_INSTALLED = __is_installed("make") if is_in_wsl() else False
IS_GCC_INSTALLED = __is_installed("gcc") if is_in_wsl() else False
LATEST_VERSION, __LATEST_VERSION_ERROR = __get_latest_version()
