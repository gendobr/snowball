import requests
from urllib.parse import quote
import json
import time

titles = [
    'Critical Review of the Integration of Bim to Semantic Web Technology',
    'Exploring Bim and NLP Applications: A Scientometric Approach',
    'Buildings and Semantics: Data Models and Web Technologies for the Built Environment',
    'Building information modeling and ontologies: overview of shared representations',
    'Report on Open Standards for Regulations, Requirements and Recommendations Content',
    'Industry 4.0 for the Built Environment: Methodologies, Technologies and Skills',
    'Ontology in the AEC Industry A Decade of Research and Development in Architecture, Engineering, and Construction',
    'Building Information Modeling: Planning and Managing Construction Projects with 4D CAD and Simulations (McGraw-Hill Construction Series)',
    'BIM Handbook: A Guide to Building Information Modeling for Owners, Designers, Engineers, Contractors, and Facility Managers',
    'e-submission common guidelines for introduce BIM to building process',
    'Semantic web technologies in AEC industry: A literature overview',
    'Knowledge Graphs and Linked Data for the Built Environment',
    'D-COM: Digital COMpliance : Digitisation of Requirements, Regulations and Compliance Checking Processes in the Built Environment',
    'Unveiling the actual progress of Digital Building Permit: Getting awareness through a critical state of the art review',
    'Ontologies and Linked Data for structuring published BIM articles',
    'Domain Ontology for Processes in Infrastructure and Construction',
    'Automatic rule-based checking of building designs',
    'Analyzing BIM topics and clusters through ten years of scientific publications',
    'A comparative study to determine a suitable representational data model for UK building regulations',
    'A Comparative Analysis of Five Rule-Based Model Checking Platforms',
    'A bibliometric and scientometric mapping of Industry 4.0 in construction',
    'In Search of Open and Practical Language-Driven BIM-Based Automated Rule Checking Systems',
    'Modelling and accessing regulatory knowledge for computer-assisted compliance audit',
    'CRITICAL REVIEW OF THE INTEGRATION OF BIM TO SEMANTIC WEB TECHNOLOGY',
    'Introducing a Building Information Model (BIM)-based process for building permits in Estonia',
    'Semantic rule-checking for regulation compliance checking: an overview of strategies and approaches',
    'Knowledge Extraction and Discovery Based on BIM: A Critical Review and Future Directions',
    'Big data in building design: a review',
    'Construction 4.0: a survey of research trends',
    'A review of Building Information Modeling research for green building design through building performance analysis',
    'From BIM to digital twins: a systematic review of the evolution of intelligent building representations in the AEC-FM industry',
    'Building Information Modeling: Automated Code Checking and Compliance Processes',
    'A Review on BIM-based automated code compliance checking system',
    'Interoperability aims in Building Information Modeling exchanges: a literature review',
    'SEMANTIC WEB FOR INFORMATION EXCHANGE BETWEEN THE BUILDING AND MANUFACTURING INDUSTRIES: A LITERATURE REVIEW',
]

for title in titles:
    quoted_title = quote(f'"{title}"')
    url = f'https://api.openalex.org/works?filter=display_name.search:{quoted_title}'
    # print(url)
    articles = requests.get(url).json()
    # print(json.dumps(articles, indent=10))
    if 'results' in articles and len(articles['results']) > 0:
        article = articles['results'][0]
        id = str(article['id']).removeprefix("https://openalex.org/")
        print(f"{id}\t{article['id']}\t{article['publication_year']}\t{article['title']}")
    time.sleep(0.1)