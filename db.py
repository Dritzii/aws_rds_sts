import configparser
import logging
import os
import sys

import fire
import psycopg2
import psycopg2.extras
from boto_client import *


class database_credentials():
    def __init__(self,dbname=None):
        self.connection = None
        config = configparser.ConfigParser()
        absolute =  os.path.dirname(os.path.abspath(__file__)) + "/rds_upgrades.ini"
        config.read(absolute)
        dictionary = {}
        options = config.options("db_details")
        for option in options:
            try:
                dictionary[option] = config.get("db_details", option)
                if dictionary[option] == -1:
                    print("skip: %s" % option)
            except Exception as Er:
                print(Er)
                dictionary[option] = None
        user = dictionary["user"]
        password = dictionary["password"]
        host = dictionary["host"]
        port = dictionary["port"]
        try:
            self.connection = psycopg2.connect(
                    dbname = dbname,
                    user = user,
                    password = password,
                    host = host,
                    port = port)
            logging.info("Connection opened successfully.")
            self.connection.autocommit = True
        except psycopg2.DatabaseError as e:
            logging.error(e)
            sys.exit(16)

    def check_db_closed(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed.")

    def execute_query(self,query):
        self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
        self.cursor.execute(query)

    def execute_checkpostgis(self):
        try:
            db = database_credentials()
            records = []
            db.execute_query(""" SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%'; """)
            details = db.cursor.fetchall()
            for row in details:
                records.append(row)
            for i in range(len(records)):
                s = ",".join(records[i])
                print(s)
        except psycopg2.DatabaseError as e:
            print(e,sys.stderr)

    def execute_checkdbnames(self):
        try:
            db = database_credentials()
            records = []
            db.execute_query(""" select datname from pg_database where datistemplate = false and datname  != 'rdsadmin'; """)
            details = db.cursor.fetchall()
            for row in details:
                records.append(row)
            for i in range(len(records)):
                single = ",".join(records[i])
                yield single
        except psycopg2.DatabaseError as e:
            print(e,sys.stderr)
        
    def auto_checkpostgisnames(self):
        try:
            for each in self.execute_checkdbnames():
                db = database_credentials(dbname=each)
                print("DB details for : " + each)
                db.execute_query(""" SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%'; """)
                details_db = db.cursor.fetchall()
                records = []
                for rows in details_db:
                    records.append(rows)
                new_records = []
                if records[0][2] is None:
                    print("No Postgis")
                    print(records[0][2])
                    if records[1][2] is None:
                        print("No Topology")
                        print(records[1][2])
                        if records[2][2] is None:
                            print("No Tiger Geocoder")
                            print(records[2][2])
                else:
                    for record in records:
                        print(record[0] + " = " + record[1] + " : " + record[2])
                    if records[0][2] != None:
                        new_records.append(each)
                    for i in new_records:
                        print("End details for : " + i)
                        yield i
        except psycopg2.DatabaseError as e:
            print(e,sys.stderr)

    def auto_alter_postgis_version(self):
        try:
            for each in self.auto_checkpostgisnames():
                db = database_credentials(dbname=each)
                records = []
                db.execute_query("""SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%' ;""")
                details = db.cursor.fetchall()
                for row in details:
                    records.append(row)
                print(records)
                version = records[0][1]
                db.execute_query(""" ALTER EXTENSION postgis UPDATE TO '{}' """.format(str(version)))
                db.execute_query(""" ALTER EXTENSION postgis_topology UPDATE TO '{}' """.format(str(version)))
                db.execute_query(""" ALTER EXTENSION postgis_tiger_geocoder UPDATE TO '{}' """.format(str(version)))
                result = []
                db.execute_query("""SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%';""")
                results = db.cursor.fetchall()
                for rows in results:
                    result.append(rows)
                if records[0][1] == result[0][2]:
                    print(str(records[0][0]) + " Successful")
                    print(str(records[0][0]) + " before: {}".format(str(records[0][1])))
                    print(str(records[0][0]) + " after: {}".format(str(result[0][2])))
                    if records[1][1] == result[1][2]:
                        print(str(records[1][0]) + " successful")
                        print(str(records[1][0]) + " before: {}".format(str(records[2][1])))
                        print(str(records[1][0]) + " after: {}".format(str(result[2][2])))
                        if records[2][1] == result[2][2]:
                            print(str(records[2][0]) + " successful")
                            print(str(records[2][0]) + " before: {}".format(str(records[2][1])))
                            print(str(records[2][0]) + " after: {}".format(str(result[2][2])))
                        else:
                            print(str(records[2][0]) + " Failed")
                            print(str(records[2][0]) + " : {}".format(str(result[2][2])))
                    else:
                        print(str(records[1][0]) + "  failed")
                        print(str(records[1][0]) + " : {}".format(str(result[1][2])))
                else:
                    print(str(records[0][0]) + " failed")
                    print(str(records[0][0]) + " : {}".format(str(result[0][2])))
        except psycopg2.DatabaseError as e:
            print(e,sys.stderr)
            
    def manual_checkpostgisnames(self,dbnames):
        try:
            if dbnames is None:
                print("Invalid Db Name",sys.stderr)
                return
            if len(dbnames) == 0:
                db = database_credentials(dbname=dbnames)
                print("DB details for : " + dbnames)
                db.execute_query("""SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%';""")
                details_db = db.cursor.fetchall()
                records = []
                for rows in details_db:
                    records.append(rows)
                if records[0][2] is None:
                    print("No Postgis")
                    print(records[0][2])
                    if records[1][2] is None:
                        print("No Topology")
                        print(records[1][2])
                        if records[2][2] is None:
                            print("No Tiger Geocoder")
                            print(records[2][2])
                else:
                    for record in records:
                        print(record[0] + " = " + record[1] + " : " + record[2])
            else:
                for each in dbnames:
                    db = database_credentials(dbname=each)
                    print("DB details for : " + each)
                    db.execute_query("""SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%';""")
                    details_db = db.cursor.fetchall()
                    records = []
                    for rows in details_db:
                        records.append(rows)
                    if records[0][2] is None:
                        print("No Postgis")
                        print(records[0][2])
                        if records[1][2] is None:
                            print("No Topology")
                            print(records[1][2])
                            if records[2][2] is None:
                                print("No Tiger Geocoder")
                                print(records[2][2])
                    else:
                        for record in records:
                            print(record[0] + " = " + record[1] + " : " + record[2])
        except psycopg2.DatabaseError as e:
            print(e,sys.stderr)
        finally:
            self.check_db_closed()
            
    def alter_postgis_version(self,version,dbnames):
        try:
            if dbnames is None:
                print("Invalid Db Name",sys.stderr)
                return
            if len(dbnames) == 0:
                db = database_credentials(dbname=dbnames)
                records = []
                db.execute_query("""SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%';""")
                details = db.cursor.fetchall()
                for row in details:
                    records.append(row)
                print(records)
                db.execute_query(""" ALTER EXTENSION postgis UPDATE TO '{}' """.format(str(version)))
                db.execute_query(""" ALTER EXTENSION postgis_topology UPDATE TO '{}' """.format(str(version)))
                db.execute_query(""" ALTER EXTENSION postgis_tiger_geocoder UPDATE TO '{}' """.format(str(version)))
                result = []
                db.execute_query("""SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%';""")
                results = db.cursor.fetchall()
                for rows in results:
                    result.append(rows)
                if records[0][1] == result[0][2]:
                    print(str(records[0][0]) + " Successful")
                    print(str(records[0][0]) + " before: {}".format(str(records[0][1])))
                    print(str(records[0][0]) + " after: {}".format(str(result[0][2])))
                    if records[1][1] == result[1][2]:
                        print(str(records[1][0]) + " successful")
                        print(str(records[1][0]) + " before: {}".format(str(records[2][1])))
                        print(str(records[1][0]) + " after: {}".format(str(result[2][2])))
                        if records[2][1] == result[2][2]:
                            print(str(records[2][0]) + " successful")
                            print(str(records[2][0]) + " before: {}".format(str(records[2][1])))
                            print(str(records[2][0]) + " after: {}".format(str(result[2][2])))
                        else:
                            print(str(records[2][0]) + " Failed")
                            print(str(records[2][0]) + " : {}".format(str(result[2][2])))
                    else:
                        print(str(records[1][0]) + "  failed")
                        print(str(records[1][0]) + " : {}".format(str(result[1][2])))
                else:
                    print(str(records[0][0]) + " failed")
                    print(str(records[0][0]) + " : {}".format(str(result[0][2])))
            else:
                for each in dbnames:
                    db = database_credentials(dbname=each)
                    records = []
                    db.execute_query("""SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%';""")
                    details = db.cursor.fetchall()
                    for row in details:
                        records.append(row)
                    print(records)
                    db.execute_query(""" ALTER EXTENSION postgis UPDATE TO '{}' """.format(str(version)))
                    db.execute_query(""" ALTER EXTENSION postgis_topology UPDATE TO '{}' """.format(str(version)))
                    db.execute_query(""" ALTER EXTENSION postgis_tiger_geocoder UPDATE TO '{}' """.format(str(version)))
                    result = []
                    db.execute_query("""SELECT name,default_version,installed_version from pg_available_extensions where name LIKE 'postgis%';""")
                    results = db.cursor.fetchall()
                    for rows in results:
                        result.append(rows)
                    if records[0][1] == result[0][2]:
                        print(str(records[0][0]) + " Successful")
                        print(str(records[0][0]) + " before: {}".format(str(records[0][1])))
                        print(str(records[0][0]) + " after: {}".format(str(result[0][2])))
                    if records[1][1] == result[1][2]:
                        print(str(records[1][0]) + " successful")
                        print(str(records[1][0]) + " before: {}".format(str(records[2][1])))
                        print(str(records[1][0]) + " after: {}".format(str(result[2][2])))
                        if records[2][1] == result[2][2]:
                            print(str(records[2][0]) + " successful")
                            print(str(records[2][0]) + " before: {}".format(str(records[2][1])))
                            print(str(records[2][0]) + " after: {}".format(str(result[2][2])))
                        else:
                            print(str(records[2][0]) + " Failed")
                            print(str(records[2][0]) + " : {}".format(str(result[2][2])))
                    else:
                        print(str(records[1][0]) + "  failed")
                        print(str(records[1][0]) + " : {}".format(str(result[1][2])))
                else:
                    print(str(records[0][0]) + " failed")
                    print(str(records[0][0]) + " : {}".format(str(result[0][2])))
        except psycopg2.DatabaseError as e:
            print(e,sys.stderr)
        finally:
            self.check_db_closed()

if __name__ == "__main__":
    fire.Fire()
