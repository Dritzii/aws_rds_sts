import configparser
import logging
import os
import sys
import time

import fire
from boto_client import *
from db import *

db = database_credentials()
client = boto_client()

def test_db(args):
    db.execute_checkpostgisnames(args)

def major_migration(args):
    startm = str(time.time())
    print(startm)
    migration_94_to_95(args)
    migration_95_to_96(args)
    migration_96_to_1010(args)
    endm = str(time.time())
    print("started : " + startm)
    print("ended : " + endm)

def minor_migration(args):
    startm = str(time.time())
    print(startm)
    migration_94_to_95(args)
    endm = str(time.time())
    print("started : " + startm)
    print("ended : " + endm)

def messagehub_minor():
    client.describe_db_instances()
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()

def messagehub_major():
    client.describe_db_instances()
    client.modify_db_instance('10.10')
    client.describe_db_instances()

def api_minor():
    startm = str(time.time())
    args = ['', '','']## todo
    db.execute_checkpostgisnames(args)
    client.describe_db_instances()
    db.alter_postgis_version('2.1.8',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    db.alter_postgis_version('2.2.5',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    endm = str(time.time())
    print("started : " + startm)
    print("ended : " + endm)


def edu_minor():
    startm = str(time.time())
    args = ['whispir_old', 'whispir','postgres']
    db.execute_checkpostgisnames(args)
    client.describe_db_instances()
    db.alter_postgis_version('2.1.8',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    db.alter_postgis_version('2.2.5',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    endm = str(time.time())
    print("started : " + startm)
    print("ended : " + endm)

def us_minor():
    startm = str(time.time())
    args = ['whispir','postgres','whispir_original']
    db.execute_checkpostgisnames(args)
    client.describe_db_instances()
    db.alter_postgis_version('2.1.8',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    db.alter_postgis_version('2.2.5',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    endm = str(time.time())
    print("started : " + startm)
    print("ended : " + endm)

def us_major():
    startm = str(time.time())
    args = ['whispir','postgres','whispir_original']
    db.execute_checkpostgisnames(args)
    client.describe_db_instances()
    db.alter_postgis_version('2.1.8',args)
    client.describe_db_instances()
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.alter_postgis_version('2.2.5',args)
    client.describe_db_instances()
    client.modify_db_instance('9.6.15')
    client.describe_db_instances()
    db.alter_postgis_version('2.3.7',args)
    client.describe_db_instances()
    client.modify_db_instance('10.10')
    client.describe_db_instances()
    db.alter_postgis_version('2.4.4',args)
    client.describe_db_instances()
    endm = str(time.time())
    print("started : " + startm)
    print("ended : " + endm)

def edu_major():
    startm = str(time.time())
    args = ['whispir_old', 'whispir','postgres']
    db.execute_checkpostgisnames(args)
    client.describe_db_instances()
    db.alter_postgis_version('2.1.8',args)
    client.describe_db_instances()
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.alter_postgis_version('2.2.5',args)
    client.describe_db_instances()
    client.modify_db_instance('9.6.15')
    client.describe_db_instances()
    db.alter_postgis_version('2.3.7',args)
    client.describe_db_instances()
    client.modify_db_instance('10.10')
    client.describe_db_instances()
    db.alter_postgis_version('2.4.4',args)
    client.describe_db_instances()
    endm = str(time.time())
    print("started : " + startm)
    print("ended : " + endm)

def api_major():
    startm = str(time.time())
    args = ['whispir_old', 'whispir','postgres']## todo
    db.execute_checkpostgisnames(args)
    client.describe_db_instances()
    db.alter_postgis_version('2.1.8',args)
    client.describe_db_instances()
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.alter_postgis_version('2.2.5',args)
    client.describe_db_instances()
    client.modify_db_instance('9.6.15')
    client.describe_db_instances()
    db.alter_postgis_version('2.3.7',args)
    client.describe_db_instances()
    client.modify_db_instance('10.10')
    client.describe_db_instances()
    db.alter_postgis_version('2.4.4',args)
    client.describe_db_instances()
    endm = str(time.time())
    print("started : " + startm)
    print("ended : " + endm)

def auto_migration_94_to_95():
    db.auto_alter_postgis_version()
    db.execute_checkpostgisnames()
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.auto_alter_postgis_version()
    db.execute_checkpostgisnames()

def migration_94_to_95(args):
    db.execute_checkpostgisnames(args)
    client.describe_db_instances()
    db.alter_postgis_version('2.1.8',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    db.alter_postgis_version('2.2.5',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)

def migration_95_to_96(args):
    db.execute_checkpostgisnames(args)
    client.describe_db_instances()
    db.alter_postgis_version('2.2.5',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    client.modify_db_instance('9.6.15')
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)
    db.alter_postgis_version('2.3.7',args)
    client.describe_db_instances()
    db.execute_checkpostgisnames(args)

def migration_96_to_1010(args):
    client.describe_db_instances()
    db.alter_postgis_version('2.3.7',args)
    client.describe_db_instances()
    client.modify_db_instance('10.10')
    client.describe_db_instances()
    db.alter_postgis_version('2.4.4',args)
    client.describe_db_instances()

def migration1010_1105(args):
    db.alter_postgis_version('2.4.4',args)
    client.describe_db_instances()
    client.modify_db_instance('11.5')
    client.wait_for_availability()
    client.describe_db_instances()

def customdb_upgrade(args):
    db.alter_postgis_version('2.1.8',args)
    client.describe_db_instances()
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.alter_postgis_version('2.2.5',args)
    client.describe_db_instances()
    client.modify_db_instance('9.6.15')
    client.describe_db_instances()
    db.alter_postgis_version('2.3.7',args)
    client.describe_db_instances()
    client.modify_db_instance('10.10')
    client.describe_db_instances()
    db.alter_postgis_version('2.4.4',args)
    client.describe_db_instances()
    client.modify_db_instance('11.5')
    client.describe_db_instances()

def auto_minor_upgrade():
    db.auto_alter_postgis_version()
    client.describe_db_instances()
    client.modify_db_instance('9.5.19')
    client.describe_db_instances()
    db.auto_alter_postgis_version()
    db.check_db_closed()

def auto_major_upgrade():
    db.auto_alter_postgis_version()
    db.execute_checkpostgis()
    client.describe_db_instances()
    client.modify_db_instance('9.5.19')
    db.execute_checkpostgis()
    client.describe_db_instances()
    db.auto_alter_postgis_version()
    db.execute_checkpostgis()
    client.describe_db_instances()
    client.modify_db_instance('9.6.15')
    client.describe_db_instances()
    db.execute_checkpostgis()
    db.auto_alter_postgis_version()
    db.execute_checkpostgis()
    client.describe_db_instances()
    db.execute_checkpostgis()
    client.modify_db_instance('10.10')
    client.describe_db_instances()
    db.execute_checkpostgis()
    db.auto_alter_postgis_version()
    db.execute_checkpostgis()
    client.describe_db_instances()
    client.modify_db_instance('11.5')
    client.describe_db_instances()
    db.auto_alter_postgis_version()

if __name__ == "__main__":
    fire.Fire()
