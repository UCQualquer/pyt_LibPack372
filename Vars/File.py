import os, mimetypes, re
from typing import Tuple, Dict, List
from . import removeDuplicates, listStrip

"""
    ########### Pillow file format support
    ###### All, including Arabic formats and celestial ones

    ## Full-Supported formats, including the ones only God can see
    __ff: List[str] = \
        ['apng', 'bmp', 'dib',
        'eps', 'gif', 'icns',
        'ico', 'im', 'j2k',
        'j2p', 'jpeg', 'jpx',
        'msp', 'pcx', 'png',
        'ppm', 'sgi', 'spi',
        'tga', 'tiff', 'webp',
        'xbm']

    ## Read-Only formats, including the ones only God can see
    __rr: List[str] = \
        ['blp', 'cur', 'dds',
        'dxc', 'flc', 'fli',
        'fpx', 'ftex', 'gbr',
        'gd', 'imt', 'iptc',
        'mcidas', 'mic', 'mpo',
        'naa', 'pcd', 'pixar',
        'psd', 'wal', 'wmf',
        'xpm', 'xvpics']

    ## Write-Only formats, including the ones only God can see
    __ww: List[str] = \
        ['palm', 'pdf']

    __rr += [x for x in __ff if x not in __rr]
    __ww += [x for x in __ff if x not in __ww]
    pil_support1: Dict[str, List[str]] = ({
        'full': __ff,
        'read': __rr,
        'write': __ww
    })

    ## All formats
    __aa = []
    __aa += [x for x in __rr if x not in __aa]
    __aa += [x for x in __ww if x not in __aa]
    pil_support1_all = __aa




    ###### Only recommended
    ## Full-Supported formats, that a Human can read
    __f: List[str] = \
        ['apng', 'bmp', 'gif',
        'ico', 'jpeg', 'jpg',
        'png', 'tiff', 'webp']

    ## Read-Only formats, that a Human can read
    __r: List[str] = \
        ['blp', 'cur', 'dcx',
        'dds', 'flc', 'fli',
        'fpx', 'ftex', 'gbr',
        'gd', 'imt', 'iptc',
        'mcv', 'mic', 'mpo',
        'naa', 'pcd', 'pixar',
        'psd', 'wal', 'wmf',
        'xpm', 'xvpics']

    ## Write-Only formats, that a Human can read
    __w: List[str] = \
        ['pdf']

    __r += [x for x in __f if x not in __r]
    __w += [x for x in __f if x not in __w]
    pil_support2: Dict[str, List[str]] = ({
        'full': __f,
        'read': __r,
        'write': __w
    })

    ## All formats
    __a = []
    __a += [x for x in __r if x not in __a]
    __a += [x for x in __w if x not in __a]
    pil_support2_all = __a

    ## Use when this format appears
    ## E.g: i.save('newimage.spi', format = 'SPIDER')
    pil_special_cases: Dict[str, str] = {
            'spi' : 'SPIDER'
    }
"""

class File(object):
    __types: Dict[str, List[str]] = ({
        'image':
            ['apng', 'bmp', 'gif',
            'ico', 'jpeg', 'jpg',
            'png', 'tiff', 'webp'],

        'video':
            ['mkv', 'mp4', 'webm',
            'flv', 'avi', 'amv'],

        'audio':
            ['mp3', 'm4a', 'flac',
            'wav', 'wma', 'aac']
    })


    __file_path: str = None

########################################################## INIT

    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__setup()

########################################################## SETUP

    def __setup(self):
        self.__file_path = os.path.abspath(self.__file_path)



########################################################## SIZE

    @property
    def Size(self) -> int:
        return self.__getSize()

########################################################## EXISTS

    @property
    def Exists(self) -> bool:
        return self.__getExists()

########################################################## PATH

    @property
    def Path(self) -> str:
        return self.__getPath()
    
    @Path.setter
    def Path(self, value: str):
        self.__setPath(value)

########################################################## DIR

    @property
    def Dir(self) -> str:
        return self.__getDir()
    
    @Dir.setter
    def Dir(self, value: str):
        self.__setDir(value)

########################################################## FILENAME

    @property
    def Filename(self) -> str:
        return self.__getFilename()

    @Filename.setter
    def Filename(self, value: str):
        self.__setFilename(value)

########################################################## EXTENSION

    @property
    def Extension(self):
        return self.__getExtension()

    @Extension.setter
    def Extension(self, value: str):
        self.__setExtension(value)

########################################################## TYPE

    @property
    def Type(self) -> str:
        return self.__getType()



########################################################## SIZE

    def __getSize(self) -> int:
        return os.path.getsize(self.Path) if self.Exists else 0

########################################################## EXISTS

    def __getExists(self) -> bool:
        return os.path.exists(self.Path)

########################################################## PATH

    def __getPath(self) -> str:
        return self.__file_path
    
    def __setPath(self, value: str):
        self.__file_path = value
        self.__setup()

########################################################## DIR

    def __getDir(self) -> str:
        return os.path.dirname(self.Path) if self.Filename else self.Path

    def __setDir(self, value: str):
        self.Path = os.path.join(value, self.Filename + self.Extension)

########################################################## FILENAME

    def __getFilename(self) -> str:
        p = os.path.splitext(self.Path)
        return os.path.basename(p[0]) if p[1] else ''
    
    def __setFilename(self, value: str):
        if not value:
            raise ValueError('Null Value was given')

        self.Path = os.path.join(self.Dir, os.path.basename(value) + self.Extension)

########################################################## EXTENSION

    def __getExtension(self) -> str:
        p = os.path.splitext(self.Path)
        return p[1] if p[1] else ''
    
    def __setExtension(self, value: str):
        value = value.strip('.')
        if not value:
            raise ValueError('Null Value was given')

        value = '.' + value
        self.Path = os.path.join(self.Dir, self.Filename + value.lower())

########################################################## TYPE

    def __getType(self) -> str:
        ex = self.Extension
        for t in self.__types:
            if ex in self.__types[t]:
                return t

        p = mimetypes.guess_type(self.Path)
        return p[0].split('/')[0] if p[0] else 'unknown'

########################################################## ARGUMENTS

    def getArguments(self, delim = '_', packer1 = '(', packer2 = ')', sep1 = '&', sep2 = ',') -> Tuple[List[str], Dict[str, List[str]]]:
        file_name = self.Filename
        if delim not in file_name:
            raise ValueError(f"File name '{file_name + self.Extension}' does not contain a valid argument format")

        args_str = file_name[:file_name.find(delim)]
        args = listStrip(args_str.split(sep1))

        arguments = []
        key_args = {}

        for arg in args:
            value = re.findall(f'\{packer1}(.*?)\{packer2}', arg)
            key = arg[:arg.find(packer1)].strip()

            if value:
                value = listStrip(value[0].split(sep2))

                if key in key_args:
                    k = key_args[key]
                    key_args[key] = removeDuplicates(k + value)

                else:
                    key_args[key] = removeDuplicates(value)
            else:
                value = arg
                arguments.append(value)

        arguments = removeDuplicates(arguments)

        # sorting
        arguments = sorted(arguments)
        key_args = dict(sorted(key_args.items()))
        return (arguments, key_args)