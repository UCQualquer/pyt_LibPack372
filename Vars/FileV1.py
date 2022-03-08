#### INCOMPLETO ####

import os, pathlib, re
from My_Pack.Essentials import *
from . import *

class File():
    file: str = None

    def __init__(self, file_name: str):
        ensureType(file_name, str, 'file_name')

        self.file = file_name
        self.__setup()
    

    def __setup(self):
        self.file = os.path.abspath(self.file)
    

    def getFilename(self, include_extension: bool = True, include_path: bool = True, include_arguments: bool = False) -> str:
        ensureType(include_extension, bool, 'include_extension')
        ensureType(include_path, bool, 'include_path')
        ensureType(include_arguments, bool, 'include_arguments')

        base = self.getBasename()
        path = self.getPath()

        if '_' in base:
            args = base[:base.find('_') + 1]
        else:
            args = None

        extension = self.getExtension()

        sp = 0 if isNone(args) else base.find('_') + 1 #start point
        if isNone(extension): base = base[sp:]
        else: base = base[sp:base.rfind('.')]


        final_f: str = ''


        if include_extension:
            final_f = f'{base}{extension}'

        if include_arguments:
            final_f = f'{args}{final_f}'
        
        if include_path:
            final_f = os.path.join(path, final_f)
        
        return final_f
    
    def getExtension(self) -> str:
        e = pathlib.Path(self.file).suffix
        return e if e else None
    
    def getPath(self) -> str:
        return os.path.dirname(self.file)
    
    def getBasename(self) -> str:
        return os.path.basename(self.file)
    
    def getArgs(self, transform = False, rules = ('&', '(', ',', ')', '_')) -> Union[str, Tuple]:
        appender, groupS, kwarg_sep, groupE, delim = rules

        if not len(rules) == 5: return ValueError('[Rules] need to have 5 chars: appender, group_start, kwarg_sep, group_end, delim')
        file = self.getFilename(False, False, True)

        if delim in file:
            if transform:
                base = self.getBasename()
                args_str = base[:base.find(delim)]
                a = listStrip(args_str.split(appender))
                args: str = []
                kwargs: Dict[str, List[str]] = {}

                for arg in a:
                    value = re.findall(f'\{groupS}(.*?)\{groupE}', arg)
                    key = arg[:arg.find(groupS)].strip()

                    if value:
                        value = listStrip(value[0].split(kwarg_sep))

                        if key in kwargs:
                            k = kwargs[key]
                            kwargs[key] = removeDuplicates(k + value)

                        else:
                            kwargs[key] = removeDuplicates(value)
                    else:
                        value = arg
                        args.append(value)
                
                return (args, kwargs)
            else:
                return file[:file.find(delim)]

        else:
            return None

    def getSize(self) -> int:
        if os.path.exists(self.file):
            return os.path.getsize(self.file)
        
        else:
            return None

