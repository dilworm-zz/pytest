#-*-encoding=utf8-*-
import xml.etree.ElementTree as ET

def testutf8():
    print "*"*30
    et = ET.parse("./xmlfiles/utf8.xml")
    root = et.getroot()
    root.find("root")
    ch = root.get("ch")
    print ch
    #root.get("ch")

def testgbk():
    print "*"*30
    #xp = ET.XMLParser(encoding="utf-8")
    #print xp
    #et = ET.parse("./xmlfiles/gbk.xml", parser=xp)
    #root = et.getroot()
    #root.find("root")
    #ch = root.get("ch")
    #print ch
    #root.get("ch")
    f = open('./xmlfiles/gbk.xml','rb')
    lines = f.read()
    print type(lines.decode("gbk"))
    l = lines.decode("gbk").encode("utf-8")
    l = l.replace('gbk', 'utf-8')
    #r = ET.fromstring(lines.decode("gbk").encode("utf-8"))
    r = ET.fromstring(l)

def main():
    #testutf8()
    testgbk()

if __name__ == "__main__":
    main()
