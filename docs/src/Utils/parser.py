class Config:
    """
    Manages Model Card configuration info.
    """
    
    def __init__(self):
        self.model = None
        self.files = []
        self.sections = []

    def setModel(self, model):
        self.model = model
        
    def setSection(self, section):
        self.sections.append(section)
         
    def setFile(self, file):
        self.files.append(file)
    
    def getModel(self):
        return self.model
        
    def getSections(self):
        return self.sections
    
    def getFiles(self):
        return self.files


#-----------------------------------------------------------------------------------------
from yaml import YAMLError
from Utils.exceptions import ParserError
import yaml


def parser():
    """
    Parse config.yml file and reorganize the configuration using Config support class.
    Returns a list of configurations.
    """
    
    configs = []
    out = ""
    
    try:
        with open("docs/setup/config.yml", "r") as config:
            setup = yaml.safe_load(config)
    except YAMLError:
        raise ParserError("YAML sintax error")
    except FileNotFoundError:
        out = "config.yml does not exist"
        return configs, out
        
    if not setup:
        out = "config.yml is empty"
        return configs, out
    if not isinstance(setup, dict):
        raise ParserError("YAML sintax Error")

    for model_name, structure in setup.items():
        try:
            config = Config()
            
            if not model_name.startswith("structure "):
                raise ParserError("Commands have to begin with structure <model name>")
            
            name = model_name.replace("structure ", "")
            config.setModel(name)

            if not isinstance(structure, list):
                    raise ParserError(f"every item in {name} have to begin with -")
                
            try:
                for section in structure:
                    if isinstance(section, str):
                        config.setSection(section)
                    elif isinstance(section, dict) and len(section) == 1:  
                        file = {}
                        for key, value in section.items():
                            if not isinstance(value, dict) or "file" not in value:
                                raise ParserError(f"invalid file definition for section {key} in {name}")
                            if not value.get("file"):
                                raise ParserError(f"file has no value for section {key} in {name}")
                            
                            config.setSection(key)
                            file[key] = value.get("file")
                            config.setFile(file)
                    else:
                        raise ParserError(f"in {name} invalid section format")
            except TypeError:
                raise ParserError(f"{name} has an invalid format")

            basic = ["general information", "training details", "evaluation"]
            for section in config.getSections():
                if section.lower() not in basic:
                    found = False
                    for item in config.getFiles():
                        if section in item.keys():
                            found = True
                            break
                    if not found:
                        raise ParserError(f"specify file for {section} in {name}")
                    
            configs.append(config)
                            
            for dicts in config.getFiles():
                for file in dicts.values():
                    try:
                        open(f"docs/setup/{file}", 'r')
                    except FileNotFoundError:
                        raise ParserError(f"{file} file does not exist")

        except ParserError as e:
            out = str(e)
            configs.append(None)
    
    return configs, out