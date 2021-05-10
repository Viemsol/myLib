#pip install ini-parser
import configparser
def getAllSections(config):
    return(config.sections())
    
def getAllTagsInSection(config,section):
    return(config[section])
    
def sectionExist(config,section):
    return(section in config)
    
def tagExist(config,section,tag):
    return(tag in config[section])
    
def getTagValue(config,section,tag):
    return(config[section][tag])
    
def creatSection(config,section):
    config[section] = {}
    
def setTagValue(config,section,tag,value):
    config[section][tag] = value

def writeConfig(file):
    with open(file, 'w') as configfile:
        config.write(configfile)
        
config = configparser.ConfigParser()
config.read('test.ini')
print(*getAllSections(config))
print(sectionExist(config,'database'))
print(*getAllTagsInSection(config,'database'))
print(sectionExist(config,'database1'))
print(tagExist(config,'paths.default','datadir'))
print(tagExist(config,'paths.default','datadir2'))
print(getTagValue(config,'paths.default','datadir'))

creatSection(config,'db')
setTagValue(config,'db','dbtag1','new value')
print(getTagValue(config,'db','dbtag1'))
writeConfig('test.ini')