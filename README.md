# AWS_RDS_boto_client
 the intent of this script is to help automate some things via a python script, but it has become clear that people want to turn towards the console to have inputs instead of writing hard code - this script now offers command line inputs for certain functions

# To get started
Install Python3.7 and above, if you have python2 installed, you will need to make sure that your commands contain python3 so it can recognise which python it is trying to access.

__https://www.python.org/downloads/__ 
and install python 3 from there.

After you git clone this repo, afterwards you need to type into the cmd the following:

__pip install -r requirements__

This will install the dependencies for what is needed to run this program

# libraries:
__Boto3__ 
--------
is a low level client designed to help automate infrastructure by connecting to different resources on the AWS API.

__Psycopg2__ 
--------
is a low level client designed to interact with databases.

__configparser__ 
--------
allows the ini file type to be used as a dictionary.

__os__ 
--------
module is a standard python3 library to work around working directory

__contextlib__ 
--------
is a wrapper designed to use other functions of of your class into each other.

__fire__ 
--------
is a heavily used library by google, used to interact with your program from the command prompt.

# Workflow:

__configure__ rds_upgrades.ini to your current credentials are the region you are wanting to sign into
__check__ database version so you can prep your steps
__postgis__ check your extension
__main.py__ decide on where you want to upgrade to via the main.py steps

__example__ i have a 9.4 db that has nothing upgraded yet including postgis, so what i would do is go into the rds_upgrades.ini file and set the configuration strings, afterwards i would go into the predefined methods on the main.py file and pick whole_migration:

python main.py whole_migration [database1,database2,database3]


__2nd example__ i have a message hub db that has no postgis, and want to upgrade to 10.10:
into the rds_upgrades.ini file and set the configuration strings, then i would use the method on the aws_rds.py like so:

python aws_rds.py modify_db_instance "10.10"


__3rd example__ i know that my database is on version 9.6, and i know my postgis is up to the max for that database version, now i want to go to 10.10:
go into the rds_upgrades.ini file and set the configuration strings, then i would use multiple different methods on the


python aws_rds.py modify_db_instance "10.10"

OR if you know your postgis is not up to date and you don't wannt to do it manually:

python main.py migration_96_to_1010 [db123.db213.db1231]



# Tips:

__Make__ sure that your arguments in the command line have square brackets
__Make__ sure that you do your configuration strings properly in the rds_upgrades.ini



# Files:
--------
__aws_rds.py__ is a config file used to interact with the boto3 client, it is a skeleton class used to manipulate things for use on the __main.py__ file


main.py is the file used to run the code, at the bottom is where the code will run based on the sequencing of what is required to get to 9.4 to 10.10.
Currently it iterates 3 databases in 1 instance.

__rds_upgrades.ini__ is where your configuration strings will be staying, you will need to have these changed per database or rds server instance everyt ime.

# Things needed:
You will need to get your security keys from AWS console, in settings -> my security credentials -> create access key - save the CSV into your local machine Afterwards you will need to Alter the line of configuration to match up with your __rds_upgrades.ini__ file

# To get your Security MFA Virtual arn:
Go to my security credentials, and scroll down to mfa - you will find something like this:
__arn:aws:iam::12312312365323423432:mfa/username__ -> get this and save it inside your ini file


# Commands example:

__If you want to describe your current Database instance based on your INI file:__
__type in the command line__
------------------------
#### python aws_rds.py boto_client describe_db_instances

__If you want to check your postgis version for the current database in your INI file:__
---------------------------
#### python aws_rds.py database_credentials execute_checkpostgis


__if you want to upgrade message hub that has no postgis to the non-mvp(10.10)__
#### python aws_rds.py boto_client modify_db_instance "10.10" 


__if you want to modify the database engine based on a custom version you want, you can enter the following in the command prompt:__
-------------------------------------
#### python aws_rds.py boto_client modify_db_instance "database_version"

__if you want to describe where you can upgrade to in the database in general based on your ini db instance file:__
---------------------------------------
#### python aws_rds.py boto_client describe_valid_db_instance_modifications

__if you want to see if your database is avaliable for use, you can run the following commmand:__
-----------------------------------
#### python aws_rds.py boto_client describe_db_instances

__if you want to upgrade a db with several databases, all to 10.10, you can run the following:__
----------------------------------
#### python main.py customdb_upgrade [db1,db2,db3,db4]

# Things to be aware of

Your INI config file is a very important tool, you will need to remember to init it properly via entering the right connection strings.
For the Database_credentials class - please make sure that if you want to iterate through a whole list of databases, please make sure that the INI looks like the following:

__dbname =__  
__so that way the database_credentials class can iterate.__

# INI requirements:


# [db_details]
-------------------
__dbname__ =
 __NOT REQUIRED__ 

__user__ =
 __REQUIRED__ 

__password__ =
 __REQUIRED__ 

__host__ =
 __REQUIRED__ 

__port__ =
 __REQUIRED__ 


# [rds]
-------------------
__role_arn__ =
 __REQUIRED__ 

__mfa_serial__ =
 __REQUIRED__ 

__region__ =
 __REQUIRED__ 

__aws_access_key_id__ =
 __REQUIRED__ 

__aws_secret_access_key__ =
 __REQUIRED__ 

__dbinstanceidentifier__ =
 __REQUIRED__ 

__service_type__ =
 __REQUIRED__ 



[s3]
----------------
__Bucket__ =
 __REQUIRED__ 

__object_name__ =
 __REQUIRED__ 



# Classes and Functions within:


There are currently 2 classes in the __aws_rds.py__ and none of these have any inheritance, under each class has specific functions to perform for database upgrades and checking the current database


# class boto_client
-----------------------
##  functions:
----------------------
__wait_for_availability__ = 
----------------
a context manager that enables a with statement

__modify_db_instance__ = 
----------------
modifies a db based on the ini file where the user specifies the version to upgrade

__describe_valid_db_instance_modifications__ = 
----------------
describes valid modifications

__describe_db_instances__ = 
----------------
a custom waiter that queries the describe db api and utilising a while loop to query each 30 seconds


__describe_logfiles__ = 
-------------------
Outputs all logfiles for Database instance based on INI file


__describe_snapshots__ =
------------------------
Outputs database snapshots for Database Instance based on INI file



__describe_db_engines_rds__ =
----------------------
Outputs the rds databases with information on them



__download_db_log_file_portion__ = 
------------------------------

Downloads a log to your local pc









# class database_credentials
------------------------
## functions:


__execute_query__ = 
------------------------
this is used mainly as a function within a function to provide an execution

__execute_checkpostgis__ = 
------------------------
this is to check the current postgis status of the current ini file settings

__execute_checkdbnames__ = 
------------------------
this is to check the current db names with the following statement -> "select datname from pg_database where datistemplate = false and datname  != 'rdsadmin';"


__alter_postgis_version__ = 
------------------------
alters a db with custom dbs in a list that alters the postgis based on the version a user specifies using a for each loop -> args = [sep.join(args)] -> 
ALTER EXTENSION postgis UPDATE TO '{}'""".format(str(version)) where {} is the users argument for the function.


# MAIN.PY functions

-----------------------------


__whole_migration__ =

----------

Whole migration does a 9.4 to 10.10 including postgis updates for the databases, it uses a predefined database list that is iterated via a tuple


__migration_94_to_95__ =


---------


migration_94_to_95 is a function that does an upgrade of 9.4 to 9.5 on a predefined list of databases including postgis updates.


__migration_95_to_96__ =


--------


migration_95_to_96 is a function that does an upgrade of 9.5 to 9.6 on a predefined list of databases including postgis updates


__migration_96_to_1010__ = 


--------

migration_96_to_1010 is a function that does an upgrade of 9.6 to 10.10 on a predefined list of databases including postgis updates



__customdb_upgrade__ =


----------


customdb_upgrade lets you pick what databases to upgrade from 9.4 to 10.10 using a custom list argument




__checkdb__ = 


-----



checkdb uses the class function to describe the current database




__auto_minor_upgrade__


-----


automatically upgrade the current database instance inside the rds_upgrade.ini file to the mvp

__auto_makor_upgrade__

-----


automatically upgrade the current database instance inside the rds_upgrade.ini file to the non mvp of 11




Copyright 2021 John Pham

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

