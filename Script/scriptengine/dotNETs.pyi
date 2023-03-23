
class Guid(object):
    """.Net's type System.Guid"""
    pass


class Version(object):
    """.Net#s type System.Version"""

    def Revision(self) -> int:
        pass

    def Revision(self) -> int:
        pass

    def Build(self) -> int:
        pass

    def Minor(self) -> int:
        pass

    def Major(self) -> int:
        pass

    def MinorRevision(self) -> int:
        pass

    def MajorRevision(self) -> int:
        pass

    def ToString(self) -> str:
        pass


class IPAddress(object):
    """.Net's type System.Net.IPAddress"""
    pass


class DateTime(object):
    """.Net's type System.DateTime"""


class TimeSpan(object):
    """.Net's type System.TimeSpan"""

    def ToString(self) -> str:
        pass


class Color(object):
    """.Net's type System.Drawing.Color"""
    pass


class Icon(object):
    """.Net's type System.Drawing.Icon"""
    pass


class Stream(object):
    """.Net's System.IO.Stream"""
    pass


class XmlElement(object):
    """.Net's System.Xml.XmlElement"""
    pass


class XmlWriter(object):
    """.Net's System.Xml.XmlWriter"""
    pass

class X509Certificate2(object):
    """.Net's System.Security.Cryptography.X509Certificates.X509Certificate2"""
    pass

class X509Chain(object):
    """.Net's System.Security.Cryptography.X509Certificates.X509Chain"""
    pass
