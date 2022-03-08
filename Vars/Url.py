import re
from typing import Union, List
from urllib.parse import urlparse, urlencode, parse_qsl, urlunparse, ParseResult


class Url(object):
    __url: str = None
    __default_scheme: str = 'http'
    __parser: ParseResult = None

########################################################## INIT

    def __init__(self, url: str):
        self.__url = url
        self.__setup()

########################################################## SETUP

    def __setup(self):
        if self.__url:
            self.__url = self.__url.strip('/')
            self.__parser = urlparse(self.__url)
            self.__parser = self.__parser._replace(path = re.sub('//+', '/', self.__parser.path.strip('/')))

            if not (self.Netloc):
                self.__url = f'{self.__default_scheme}://{self.__url}'
                self.__setup()

            if not (self.Scheme):
                self.__parser = self.__parser._replace(scheme = self.__default_scheme)
    
        else:
            raise ValueError("Null 'url' was given")



########################################################## PARSER

    @property
    def Parser(self) -> ParseResult:
        return self.__getParser()

########################################################## URL

    @property
    def Url(self) -> str:
        return self.__getUrl()
    
    @Url.setter
    def Url(self, url: str):
        self.__setUrl(url)

########################################################## SCHEME

    @property
    def Scheme(self) -> str:
        return self.__getScheme()
    
    @Scheme.setter
    def Scheme(self, value: str):
        self.__setScheme(value)
    
########################################################## PATH

    @property
    def PathL(self) -> Union[list, None]:
        return self.__getPathL()

    @PathL.setter
    def PathL(self, value: List[str]):
        self.__setPathL(value)

    @property
    def Path(self) -> Union[str, None]:
        return self.__getPath()
    
    @Path.setter
    def Path(self, value: Union[str, list]):
        self.__setPath(value)

########################################################## HOSTNAME | PORT

    @property
    def Hostname(self) -> str:
        return self.__getHostname()

    @property
    def Port(self) -> int:
        return self.__getPort()

########################################################## NETLOC

    @property
    def Netloc(self) -> str:
        return self.__getNetloc()
    
    @Netloc.setter
    def Netloc(self, value: str):
        self.__setNetloc(value)

########################################################## QUERY

    @property
    def Query(self) -> Union[dict, None]:
        return self.__getQuery()

    @Query.setter
    def Query(self, value: dict):
        self.__setQuery(value)



########################################################## PARSER

    def __getParser(self) -> ParseResult:
        return self.__parser

########################################################## URL
    
    def __getUrl(self) -> str:
        return self.__parser.geturl()
    
    def __setUrl(self, url: str):
        self.__url = url
        self.__setup()

########################################################## SCHEME

    def __getScheme(self) -> str:
        return self.__parser.scheme
    
    def __setScheme(self, value: str):
        u = list(urlparse(self.Url))
        u[0] = value
        self.Url = urlunparse(u)

########################################################## PATH

    def __getPath(self) -> Union[str, None]:
        p = self.__parser.path.strip('/')
        return p if p else None
    
    def __getPathL(self) -> Union[list, None]:
        p = self.Path

        if p:
            p = p.strip('/').split('/')
            return p if p else None

        else:
            return None

    def __setPath(self, value: Union[str, list]):
        if type(value) == str:
            value = re.sub('//+', '/', value)
            self.__parser = self.__parser._replace(path = value)

        elif type(value) == list:
            self.__parser = self.__parser._replace(path = '/'.join(value))
        
        else:
            raise TypeError

    def __setPathL(self, value: List[str]):
        self.Path = '/'.join(value)

########################################################## HOSTNAME | PORT

    def __getHostname(self) -> Union[str, None]:
        p = self.__parser.hostname
        return p if p else None
    
    def __getPort(self) -> Union[int, None]:
        p = self.__parser.port
        return int(p) if p else None
    
########################################################## NETLOC

    def __getNetloc(self) -> Union[str, None]:
        p = self.__parser.netloc
        return p if p else None
    
    def __setNetloc(self, value: str):
        u = list(urlparse(self.Url))
        u[1] = value
        self.Url = urlunparse(u)

########################################################## QUERY

    def __getQuery(self) -> Union[dict, None]:
        p = self.__parser.query
        return dict(parse_qsl(p)) if p else None
    
    def __setQuery(self, value: dict):
        u = list(urlparse(self.Url))
        u[4] = urlencode(value)
        self.Url = urlunparse(u)



########################################################## STATIC

    @staticmethod
    def urlEncode(url: str) -> str:
        return urlencode(url)