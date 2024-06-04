import modules.azureConnection as Azure
import modules.automationAux as Aux


if __name__ == "__main__":
    Aux.Main.setLanguage(language='pt_BR')
    Azure.AzureConnection().startRun()
