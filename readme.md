# Standardized Failure Analysis Metadata Header Documentation
Visit website: [Failure Analysis Matedata Header Documentation](https://failure-analysis-metadata-header.github.io/)

In semiconductor failure analysis (FA), multiple analysis steps using different technologies are typically carried out to identify the causal failure. In order to enable a higher degree of automation, the machines used for the different analysis steps must be able to communicate with each other through a standardized interface. The goal of the standardized metadata header is to provide such an interface by providing a standard schema for the storage of metadata associated with analysis images or other measurement data types.

Each image created during a failure analysis should be accompanied by a JSON metadata header that adheres to the same schema. This will allow failure analysis software systems to easily incorporate the metadata in their databases and exchange these metadata between different analysis machines, thereby enabling increased automation as well as laying the ground for ML-based analysis of FA data.

This documentation describes the structure of the JSON Header and how the different sections shall be used. Furthermore, usage examples of the JSON Header are sketched out for better understanding.

The Header has a federal structure and contains standardized data fields/labels and non-standardized areas for multi-purpose data fields.

**Contents**

- [Header Sections](#header-sections)
  - [Customer](#customer)
  - [General](#general)
  - [Method](#method)
  - [Tool](#tool)
  - [Data Evaluation](#data-evaluation)
- [Manufacturer Information](#manufacturer-information)
- [JSON Header Workflow](#json-header-workflow)

## Header Sections

This section describes the different sections that make up the JSON Header and what they are used for.
In the future, further sections may be added. The modular schemas of the header allow extension and adding of new sections.
The following image gives an overview of the overall structure of the header:
![plot](documentation/images/Header_Overall_Structure_new.PNG)
The different sections are generated based on seperate JSON-Schema files (Each section has an own schema file). This allows easy interchangeability of new versions for different sub sections and also easy customization (e.g. Infineon and Bosch may have different CustomerSection-Schema Files without affecting the other sections)

### General

The general section contains all general information about the image to which the JSON Header relates. For example, this includes things like

- file format
- file size
- image height and width
- pixel size
- bit depth
- color mode
- file name
- ...

The general section with its data fields/labels is illustrated in the following graphic. The illustrations for the other sections can be found in the detailed report: **Link to Markos Report**

![plot](documentation/images/Header_GeneralSection_Overview.png)

Furthermore, the general section contains a **Coordinates Sub Section**, which should be used to store all coordinates needed to determine the position of a part on a standard holder. This includes stage coordinate marks, stage rotation and general stage coordinate system information. Transformed coordinates of marked objects on the image can also be saved in this section.
This coordinate sub section also contains the coordinates of the three alignment marks of the standardized sample holder (**Universal Sample Holder**). The following tools are thus able to align their coordinate system according to the alignment marks.
The following images show the Universal Sample Holder with its alignment marks (left) and an exemplary an excerpt of the alignment marks and the Coordinate Sub Section of the header:

<div align="center">
  <img src="documentation/images/UniversalSampleHolder-AlignmentMarks.png"/>
  <img src="documentation/images/Alignment_Marks_SubSection.PNG" width = "200" height="400"/>
  <img src="documentation/images/Stage_Coordinates.PNG" width = "250" height="400"/>  
</div>

<!-- ![plot](documentation/images/UniversalSampleHolder-AlignmentMarks.png) ![plot](documentation/images/Header_Example_AlignmentMarkSubSection.png) -->

### Method

The method section contains information that is specific for a certain analysis method, such as scanning electron microscopy (SEM), focused ion beam (FIB) or X-ray. For each method, the method section schema must be extended with a new object in the method section. The exemplary structure is as follows:

- Method Specific
  - SEM
    - Accelerating Voltage
    - Decelerating voltage
    - ...
  - FIB
  - Xray
  - <new method>

Existing metadata should be mapped to the data fields/labels in the respective method section.

_Hint_: Existing metadata with no matching data fields/labels could be stored in the private/tool specific section.

_Hint_: Each method has its own schema file. The schema files can be merged/combined into one global method specific schema file, if desired. Otherwise, within the header creation software, the respective schema needs to be selected.

### Tool

The tool section contains all information related to a specific tool which is not standardized in the tool's dedicated method section. The structure is similar to the Method Specific Section: for each tool, a new object, named by the name of the tool, must be inserted in the tool section schema. The tool vendors are responsible for filling the Tool Specific Section. The section must follow the overall JSON schema rules, but the individual data fields/labels can be determined by the tool vendor. This allows a high degree of freedom to the individual tool vendor.
_Hint:_ As optional step, the tool vendor can provide its JSON schema file of the Tool Specific Section to the customer, to enable and simplify the further usage of the tool specific meta-data.

### Data Evaluation

The data evaluation contains information about measurement evaluation. This includes, for example, points and regions of interests (POI and ROI, respectively) that have been marked on the associated image. There exists a **POI** and a **ROI** object in the **Data Evaluation** schema, which can be used accordingly. A POI is simply described by a name, it's x- and y-coordinates, label and ID. ROIs can be defined in the **ROI** section as either polygons or polylines and are defined by a name, multiple points, label, ID and additionally fill and stroke color as well as stroke width. Polygons require the additional area attribute.

### Customer

The customer section contains information that is specific to the customer. Here, customer typically refers to the analysis lab in which the JSON Header is used. The information contained in this section can be fully customized for the respective user/organization/company. Typical information would be internal sample IDs, order numbers or other information that is useful for processing of the sample.

## Manufacturer Information

This section contains information that is relevant for equipment manufacturers that want to integrate the JSON Header into their equipment.

In order to facilitate generation and usage of the FA4.0 JSON Header, any equipment machine must be able to both read and write JSON files that adhere to the FA4.0 JSON Header schema.

### Read JSON Header Files

The reading of JSON header files is necessary for several reasons. First, it allows to transfer information, stored in the JSON Header, between differnt tools. This could be POIs, ROIs and the location on the sample holder, for example. Moreover, in order for the tool to write a JSON file itself, it usually requires customer-specific information such as order or sample IDs that can be read via the JSON header. This information is crucial for identifying the resulting image and storing it properly in a database. Therefore, a tool user should be able to load a JSON file via the accompanying tool software.

Coordinate-related information in the JSON Header, such as stage coordinates, must also be aligned to the local tool coordinate system in order to allow transfer of POIs/ROIs between tools. If the tool should facilitate a sample holder-based workflow to allow for easy transfer of coordinates between tools, it must provide functionality to read the sample holder reference points and align the coordinate system accordingly with the coordinates defined in the JSON Header.

### Write JSON Header Files

Any JSON Header files that are created by the tool must adhere to a specified version of the FA4.0 JSON Header schema. Depending on the tool, the information will most likely be written to the sections General, Method and Tool. When saving an image after loading a JSON Header file, a new JSON Header file should the be automatically stored. The name of the JSON file must be identical to the image file except for the file extension. For example:

- my_example_image.png
- my_example_image.json

## JSON Header Workflow

The Standardized FA JSON Header is used for image meta data storage and can be used as a transfer file to exchange the meta data between different tools in a workflow. In the following an exemplary workflow is illustrated between a scanning acoustic microscope (tool A) and focused ion beam (tool B) using the JSON Header together with the Universal Sample Holder: 

- A Flip Chip (such as one illustrated in the image below) is analyzed after a thermal stress test which potentially induces delaminations between the solder bumps and the interconnection layer of the die. 
<div align="center">
  <img src="documentation/images/schematic_crossection.PNG" width="500" height="200" />
  <img src="documentation/images/sample_overview.jpg" width="300" height="200" />  
</div>

- The chip is attached to the Universal Sample Holder and it's alignment marks are automatically scanned at the scanning acoustic microscope (SAM).

- The SAM is able to generate images at different material interfaces in C-SAM mode. Possible delaminations or cracks within the chip appear white in the SAM image. In our case therefore, the delaminated regions at the interface between the solder bumps and the interconnection layer of the die show up as 'white bumps':
<div align="center">
  <img src="documentation/images/White_Bumps.jpg" width="500" height="350" />
</div>

- After inspecting the white bumps, the user saves the created SAM image together with its corresponding JSON file header which contains all general image and SAM specific meta data, but also the coordinates of the alignment marks from the Universal Sample Holder and the stage position of the SAM. The alignment marks and the stage position will be used for coordinate transformation between tool A and tool B. Optional: Upload the JSON file header and the image to an internal Database.

<div align="center">
  <img src="documentation/images/UniversalSampleHolder-AlignmentMarks.png"/>
  <img src="documentation/images/Alignment_Marks_SubSection.PNG" width = "200" height="400"/>
  <img src="documentation/images/Stage_Coordinates.PNG" width = "250" height="400"/>  
</div>

- Furthermore, an additional application can be used which reads the image and the JSON file header, where the user marks the inspected white bumps as, e.g. points of interest (POIs). The SAM coordinates of the POIs are saved under the Data Evaluation section in the JSON file header.

<div align="center">
  <img src="documentation/images/Xeia_Demo.PNG" height="450" />
</div>

- In the last step of the workflow, the user wants to perform a focused ion beam (FIB) cut at tool B to verify the root cause failure of the inspected white bumps in the SAM image. The Uiversal Sample Holder is inserted into the FIB and the alignment marks are again automatically scanned.
  
- The FIB tool can only generate images of the chip surface and not at different material interfaces like the SAM. Thus, it is difficult for the user to navigate to the explicit POIs, since they are not visible at the chip surface. 
- To navigate to the POIs, the FIB loads the JSON file header and reads the coordinates of the POIs and alignment marks in the SAM coordinates. It subsequently performs a coordinate transformation with the help of the alignment marks to retrieve the FIB coordinates of the POIs:

<div align="center">
  <img src="documentation/images/Coordinate_Transformation.png" />
</div>

- Finally the the user can navigate to the white bumps of interest and perform a FIB cut to verify the root cause failure:
<div align="center">
  <img src="documentation/images/autoxeia_move.png" width="350" height="350" />
  <center>
    --->
  </center>
  <img src="documentation/images/Final_FIB_Cut.png" width="350" height="350" />
</div>


<!-- Old Version: The JSON Header can be used for general image metadata storage and to transfer this metadata between different tools. An exemplary workflow could look like the following:

- Create initial JSON file from database
  - This initial JSON file would hold no image information but only customer-specific information such as order or part IDs
- Load initial JSON file to tool A
- Create Image with tool A
- Save JSON Header for image with tool A
  - This JSON header would contain information about the image as well as any image or sample holder related coordinates that were used while taking the image
- Optional: Upload JSON Header and Image to database
- Load JSON header with tool B
  - The JSON header to be loaded could either be newly created from the database (if information was uploaded), or the file that was created in the previous steps could be used directly
- Create image with tool B with the help of positional information stored in JSON Header
- Save new JSON Header with tool B

In this workflow, a set of certain POIs could be marked in the image taken with tool A and then be transferred to tool B, which can then take pictures of the same POIs based on the coordinates. This requires storing of all coordinate-related information and correct transformation between coordinate systems, if necessary. In case of using a sample holder, this workflow is greatly simplified as the coordinate system of the sample holder can be used. -->
