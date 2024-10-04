from constants.project_constants import data_path
from utils.organizer import Organizer
from generators.html_generator import HtmlGenerator

if __name__ == "__main__":
    Organizer(data_path)
    HtmlGenerator('formatted_data.json')