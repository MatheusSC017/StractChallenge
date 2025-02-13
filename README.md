# StractChallenge

## Installation

### On-premises installation
1. Clone the repository on your device

2. Go to the repository of the cloned project on your device

3. Create a virtual environment on your device and activate it (command for linux OS)
> python -m venv venv
> 
> . venv/bin/activate

4. Install the libraries saved in the requirements.txt file, if you are using the PIP package manager you can use the following command
> pip install -r requirements.txt

5. The final step is to run the application, to do this run the command below:
> flask --app clients run 

## Endpoints

### /
Profile

### /{{plataforma}}
All insights for the selected platform

### /{{plataforma}}/resumo
Sum of insights per account on the platform

### /geral
All insights for all platforms

### /geral/resumo
Sum of insights per platform

## Technologies

Key technologies employed in the construction of this API include:

- Flask
- Requests

