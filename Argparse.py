from argparse import ArgumentParser, Action
from typing import Union, List, Tuple, Dict


class Argument(object):
    def __init__(self, *names: str, action: Union[Action, str] = 'store', **kwargs):
        """

        Args:
            action (Union[Action, str], optional): Defaults to 'store'. Consulte a documentação de [argparse] se quiser informações.
        
        Rules:
            - Em argumentos posicionais (não iniciados com '-'), [dest] é ignorado e [required] é [True].
        """


        if len(names) == 1:
            if not names[0].startswith('-'):
                kwargs.pop('required', None)
                kwargs.pop('dest', None)

        self.names = names
        self.action = action
        self.kwargs = kwargs

class Argparse(object):
    parser: ArgumentParser = None

    def __init__(self, *args, **kwargs):
        self.parser = ArgumentParser(*args, **kwargs)

    def addArgument(self, argument: Argument):
        self.parser.add_argument(*argument.names, action = argument.action, **argument.kwargs)
        
    def addExclusiveArguments(self, arguments: Union[List[Argument], Tuple[Argument]], **kwargs):
        if len(arguments) < 2: raise ValueError('[arguments] must be at least 2')
        kwargs.setdefault('required', False)

        g = self.parser.add_mutually_exclusive_group(required = kwargs['required'])

        for arg in arguments:
            arg.kwargs['required'] = False
            g.add_argument(*arg.names, action = arg.action, **arg.kwargs)

    def getArgs(self, *args, **kwargs) -> Dict[str, object]:
        return vars(self.parser.parse_args(*args, **kwargs))
    
    def getAllArgs(self, *args, **kwargs) -> Tuple[List[str], Dict[str, List[str]]]:
        parser = ArgumentParser(add_help = False)
        parser.add_argument('args', nargs = '*')

        _, unknown = parser.parse_known_args(*args, **kwargs)

        already_used = []

        for arg in unknown:
            if arg.startswith(('-', '--')):
                if arg not in already_used:
                    already_used.append(arg)
                    parser.add_argument(arg.split('=')[0], nargs = '*', type = str)
        
        args = vars(parser.parse_args(*args, **kwargs))

        for arg in args.copy():
            if not args[arg]:
                args[arg] = True

        for key in args.copy():
            v = ''
            add = False

            values: list = args[key]
            if type(list) == bool: continue

            for value in values:
                if not type(value) == str: continue

                value: str = value

                if value.startswith(('"', "'")):
                    v += value + ' '
                    add = True
                
                elif value.endswith(('"', "'")):
                    v += value
                    add = False
                    args[key] = v.strip('"').strip("'")

                elif add:
                    v += value + ' '
                    continue

        kwargs = args
        args = kwargs['args']
        kwargs.pop('args', None)
        kwargs = dict(sorted(kwargs.items()))
        return (args, kwargs)
