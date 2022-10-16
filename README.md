# Parsing-the-map-selenium-
Parsing the advertisements of the map using Selenium


1-Part:
collecting the dataset of ID each apartments from the site



1-Step: 
import necessary libraries

installing:
1:
pip install pandas
2:
pip install selenium
3:
pip install UserAgent
4:
pip install pymssql
5:
pip install sqlalchemy 
6:
pip install urllib3
7:
pip install warnings
8:
pip install sleep

2-Step:
Finding weak points of the site. For example, clickable areas that have many needed the pieces of data. 

3-Step:
Inspecting the site. For example, discovering the classnames.

4-Step:
Gathering data in the framework. In my case, I used "Pandas".

5-Step:
Sending the framework to SQL Server. I used MS SQL(Azure in MacOS). 

6-Step:
Manipulateing and sorting the data. 

7-Step:
Recognising that it is not legal method.



2-part:
Collecting descriptions and information about each apartments requesting ID
In the way, I will bypass CAPTCHA




1-Step: 
import necessary libraries

installing:
1:
pip install tensorflow
2:
pip install google.cloud


2-Step:
Analyzing the site, what we need fisrtly and so on. Collecting 5-10 patterns and setting the column types for SQL server

3-Step:
Setting sleep(2) after each parsing apartment not to be caught 

4-Step:
If I meet CAPTCHA, I need to pass it with predicting images or audio. After each passing successfully CAPTCHA, I can easily parse 15-20 apartments without CAPTCHA.

5-Step:
Sending the framework to SQL Server. I used MS SQL(Azure in MacOS). 

6-Step:
Manipulateing and sorting the data. 

7-Step:
Recognising that it is not legal method.

