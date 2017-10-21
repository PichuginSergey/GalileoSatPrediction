import xml.sax.handler
TAGS = ["SVID", "aSqRoot", "ecc", "deltai", "omega0", "omegaDot", "w",
        "m0", "af0", "af1", "iod", "t0a", "wna", "statusE5a", "statusE5b",
        "statusE1B"]
class GalParser(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.curTag = ""
        self.data = {name : [] for name in TAGS}
        self.fIssueDate = False
        self.issueDate = ""
        
    def startElement(self, name, attributes):
        if name in TAGS:
            self.curTag = name
            return
        if name == 'issueDate':
            self.fIssueDate = True
            
    def characters(self, content):
        if self.curTag != "":
            self.data[self.curTag].append(content)
            self.curTag = ""
            return
        if self.fIssueDate == True:
            self.issueDate = content
            self.fIssueDate = False
            
    def endDocument(self):
        fp = open("data.txt", "w")
        for tag in TAGS:
            fp.write(tag + ": ")
            for elm in self.data[tag]:
               fp.write(str(elm) + " ")
            fp.write("\n")
            
    def getData(self):
        return (self.issueDate, self.data)

class GalAlmParser():
    def __init__(self): 
        self.handler = GalParser()
        self.parser = xml.sax.make_parser()
        self.parser.setContentHandler(self.handler)
        
    def parse(self, name):
        self.parser.parse(name)
        return self.handler.getData()
