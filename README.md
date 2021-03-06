Data Anonymization Tool
=======================


There is an overlap of fields that you'll see on online application and the offline tool. Following describes what these fields represent and how you should go about populating them (in the offline tool, i.e.) : 

**Field name** | **Default Value** | **Comment(s)**
:-----------------: | :-------------------------: | :----------:
Input file's path | Input/census-income_1K.txt     | The sample input file can be viewed at the default location - as stated in the *Default value* column. If you intend to anonymize a dataset of your choice, you should provide the entire path of your dataset in the field.
Output file's name | Output/Output-*(algorithm)*.txt | The output is generated in the folder named `Output` with name of the resulting dataset defined as Output-*(algorithm)*_*(format type)*.txt . Also, should you feed a custom value to this field, make sure that the name is in format : **(name).(some-extension)** - there has to be a **.** in the output file's name for generating generalized dataset in *anatomy* format.
Separator | **,** | In the sample text provided, the separator (delimiter) used for differentiating one attribute from other (in a record) is ','.
TXT Path | config/config.txt | This is the file using which an configuration XML is generated which essentially controls the tool's behavior. You can view the default file being used by clicking on 'TXT Path' on the application. More about writing you own config file after this table.
k | 10 | The k value from k-anonymization algorithms. The value of k should be an integral value greater than or equal to 1.
t | 0.2 | The t value defines the threshold value for algorithm implementing t-closeness. The value of t should be a real number between 0 and 1.
Suppression Threshold | k | This number defines the maximum number of tuples which can be suppressed.
Output Type | genVals | The output for anonymization can be produced in one of three available formats : *genVals*,*genValsDist*,*anatomy*
Anonymize | -NA- | The tool produces result in *genVals* format (by default). In order to explore other formats, choose the format of your choice (from the dropdown menu) and click on *Anonymize*.

##Writing your own config file

**Format** : *(Attribute Type)* *(Column number of attribute)* ...

Following types of attributes are supported by the application:

1. Hidden (hid) : *e.g.* hid (Col1),(Col2),...
2. Sensitive (sens) : *e.g.* sens cat (Col1) ...
3. Quasi-Identifiers (qid) : *e.g.* qid cat/hei (Col1) ...

Quasi-identifiers can have either :

1.Categorical attributes (cat) - These attributes require mapping to an integral value. These mappings have to be explicitly mentioned in the config file. The general convention, behind creating these maps, is to allocate a value of 0 to one of the attributes' values and then incrementing and allocating values to subsequent values. **Note:** These attribute types are also supported by sensitive attributes.

2.Hierarchical attributes (hei) - These attributes have **VGH**(*value generalized hierarchies*). These hierarchies can be represented in the following format *Root node*,*Left subtree*,*Right subtree*. 

In the sample dataset, one of the fields (Column# **0**) have the following VGH - 

					 		0:100
							/   \
					   0:50		 50:100
					  /    \	 /     \		
					0:25  25:50 50:75 75:100
			
This can be transalated as : **0:100,0:50-0:25-25:50,50:100-50:75-75:100** - The *Root node* is represented by 0:100. *Root node* has three nodes in its left subtree: 0:50, 0:25 and 25:50. In the left subtree, 0:50 represents the root of the left subtree whereas 0:25 and 25:50 represent the left (leaf) child and the right (leaf) child, respectively. Similarly, *Root node* has three nodes in its right subtree: 50:100, 50:75 and 75:100. In the right subtree, 50:100 represents the root of the right subtree whereas 50:75 and 75:100 represent the left (leaf) child and the right (leaf) child, respectively. The attributes in this category are generalized bottom-up. With the generalization, they are transformed from their *original* (more specific) values to *generalized* (more general) values until they conform to the requirements mandated by the algorithm, in practice.

##A little about the output formats:
* **genVals** : This format produces the expected anonymized output.
* **genValsDist** : This format provides information pertaining distribution (padded to Quasi-identifier attributes) 
	1.	Statistical information (i.e. mean and variance) for the numerical attributes 
	2.	For categorical attributes, the format yields complete distribution. 

* **anatomy** : This format yields two tables at the end of the process - both tables having the same number of tuples as the original dataset. 
	1.	The first table (a.k.a. ST) consists of tuples with their Quasi-Identifiers replaced by the *Equivalence Class* that they belong to. 
	2.	The second table (a.k.a. QIT) contains the replaced attribute values (same as above) along with the most specific quasi-identifier values.

##Requirements for offline tool:
1. **Python 2.6**
2. **xml.etree.cElementTree** (Built-in Python module)
3. **Tkinter** (Try importing Tkinter in your python interpreter. If import is successful - you're all set, else : Open terminal -> `sudo apt-get install python-tk`)

##Running the offline tool
1. Download the [offline tool](http://data-anonymization-tool.herokuapp.com/static/Tool.tar.gz).
2. Go to the download location and unzip the tarball.
3. Open terminal -> chmod a+x application.py
4. *From terminal* -> ./application.py

	i.	If you have your customized config.xml prepared, you can enter the path of your XML file (in **Config file's path**) and the tool will use that for creating the anonymized dataset.

	ii.	If not, click on the drop-down menu. Fill in the necessary fields (the application comes setup with default values) -> **Anonymize**!


##Constraints
1. As of now, the tool only support **VGH** binary trees of height **2**.
2. Only categorical sensitive attributes are supported.
3. Only one sensitive attribute could be accommodated with the current algorithm.
4. The input file should be an unstructured text file - interfacing with commonly used database systems (SQLite, Postgres, etc.) is not possible, as of now.


**The Online application is hosted [here](http://data-anonymization-tool.herokuapp.com/).**
