from mlflow.tracking import MlflowClient
from Utils.exceptions import NoModelException
from Utils.utility import convertTime, extractInfoTags
from Utils.utility import extratDatasetName, getPath, templateRender
from Utils.parser import Config
from Utils.logger import Logger

import os, warnings
warnings.filterwarnings("ignore")

class ModelCardGenerator:
    def __init__(self, uri):
        self.client = MlflowClient(uri, uri)
        self.output = Logger()
    
    def getOutput(self):
        return self.output

    def modelLineage(self):
        """
        Returns a list of models stored in MLflow's Model Registry. 
        It prefers versions marked with the alias "champion"; if none exist, 
        it returns the latest available version of each model.
        """
        
        modelRegistry = self.client.search_registered_models()
        
        modelsName = []
        for model in modelRegistry:
            modelsName.append(model.name)

        models = []
        for name in modelsName:
            latest = True
            modelVersions = self.client.search_model_versions(f"name='{name}'")
            for model in modelVersions:
                if "champion" in model.aliases:
                    models.append(model)
                    if not model.version == self.client.get_latest_versions(name)[0].version:
                        modelInfo = f"_{model.name} v{model.version}_"
                        self.output.warning(f" {modelInfo}: `@ Champion` model is not the latest")
                    latest = False
            if latest:
                latestVersion = self.client.get_latest_versions(name)[0]
                models.append(latestVersion)

        if not models:
            raise NoModelException("No Model in Model Registry")
        
        return models


    def fetchData(self, model):
        """
        Trace information about an experiment tracked in the MLflow Tracking. 
        Once the corresponding run is obtained, retrieve the relevant information.
        """

        # Get run_id from model
        runID = model.run_id

        if not runID:
            raise NoModelException("No Experiment in MLflow Tracking")

        # Extract information through the run
        run = self.client.get_run(runID)
        self.name = str(model.name.split("_")[1] 
                            if "_" in model.name else model.name)
        name = self.name
        version = model.version
        params = run.data.params
        author = run.info.user_id
        metrics = run.data.metrics
        estimator = run.data.tags.get("estimator_name", None)
        py, lib, libv = extractInfoTags(run.data.tags)
        startTime = convertTime(run.info.start_time)
        endTime = convertTime(run.info.end_time)
        datasetName = extratDatasetName(run.inputs.dataset_inputs)

        info = f"_{name} v{version}_"
        if not params:
            self.output.warning(f"{info}: Missing parameters in Model Card generation")
        if not metrics:
            self.output.warning(f"{info}: Missing metrics in Model Card generation")
        if not datasetName:
            self.output.warning(f"{info}: Missing dataset information in Model Card generation")
        if not estimator:
            self.output.warning(f"{info}: Missing estimator information in Model Card generation")
        if "" in [author, py, lib, libv, startTime, endTime]:
            self.output.warning(f"{info}: Missing info in Model Card generation, check the Model Card for any details.")

        self.title = {
            "modelName": name,
            "version": version,
        }
        
        self.generalinformation = {
            "author": author,
            "modelType": estimator,
            "library": lib,
            "libraryVersion": libv,
            "pythonVersion": py,
        }
        
        self.trainingdetails = {
            "datasetName": datasetName,
            "parameters": params,
            "startTime": startTime,
            "endTime": endTime,
        }
        
        self.evaluation = {"evaluations": metrics}

        return None


    def ModelCard(self, model, config : Config = None):
        """
        Create a Model Card by instantiating predefined 
        templates using the retrieved information and config file.
        """
        
        try:
            data = self.fetchData(model)
        except NoModelException as e:
            self.output.error(f"Check if models exist: {str(e)}")
            return None

        if config:
            instance = templateRender("title_template.md", self.title)
        
            processed = set()
            for section in config.getSections():
                auto = True
                
                for file in config.getFiles():
                    if section in file.keys():
                        # Uses file to generate a section
                        file = file[section]
                        with open(f"docs/setup/{file}", 'r') as part:
                            text = part.read()        
                        assemble = {"title": section, "text": text}    
                        instance += templateRender("_part.jinja", assemble)
                        processed.add(section.lower())
                        auto = False
                        break

                if auto:
                    # Uses MLflow informations to generate a section
                    basic = ["general information", "training details", "evaluation"]
                    part = section.lower()
                    if part in basic and part not in processed:
                        file = part.replace(' ', '')
                        template = f"{file}_template.jinja"
                        attribute = getattr(self, file)
                        if attribute:
                            instance += templateRender(template, attribute)
                            processed.add(part)
                        
        else:
            # Default if no configuration is given
            data = self.title | self.generalinformation | self.trainingdetails | self.evaluation
            instance = templateRender("modelCard_template.jinja", data)
            out = f"No configuration provided for _{self.name}_: generated a deafult Model Card"
            self.output.warning(out)

        path, file = getPath(self.title)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as modelCard:
            modelCard.write(instance)
            self.output.log(f"Model Card {file} created")  
        
        return None
    