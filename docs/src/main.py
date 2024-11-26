from Utils.logger import Logger
from Utils.parser import parser
from generator import ModelCardGenerator
from mlflow.exceptions import MlflowException
from Utils.exceptions import NoModelException, ParserError

def generator():
    output = Logger("Model Cards Generation")
    try:
        generator = ModelCardGenerator("https://dagshub.com/donatooooooo/MLflow_Server.mlflow")
        lineage = generator.modelLineage()

        parsedConfigs = []
        try:
            parsedConfigs, out = parser()
            output.error(out) if out else None
        except ParserError as e:
            output.error(str(e))

        for model in lineage:
            default = True
            if parsedConfigs:
                for config in parsedConfigs:
                    if config is None:
                        break

                    name = str(model.name.split("_")[1] 
                                if "_" in model.name else model.name)
                    if config.getModel() == name:
                        generator.ModelCard(model, config)
                        default = False
                        break
            if default:
                generator.ModelCard(model)

        output.merge(generator.getOutput())
    except MlflowException as e:
        output.error(f"Check MLflow Server status: {str(e)}")
    except NoModelException as e:
        output.error(f"Check if models exist: {str(e)}")
    except FileNotFoundError as e:
        output.error(f"Check file path, {str(e).split('] ')[1]}")
    except Exception as e:
        output.error(f"Exception caused by: {str(e)}")
    finally:
        output.display()

if __name__ == "__main__":
    generator()
