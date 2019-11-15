"""
Author: John Pham
Company: Expose
Intent: To create a reusable program
"""
import configparser
import logging
import os
import sys
import time
from contextlib import contextmanager

import boto3
import fire
from db import *


class boto_client():
    def __init__(self):
        boto3.set_stream_logger("", logging.INFO)
        config = configparser.ConfigParser()
        absolute =  os.path.dirname(os.path.abspath(__file__)) + "/rds_upgrades.ini"
        config.read(absolute)
        dictionary = {}
        options = config.options("rds")
        for option in options:
            try:
                dictionary[option] = config.get("rds", option)
                if dictionary[option] == -1:
                    print("skip: %s" % option)
            except:
                print("Exception")
                dictionary[option] = None
        self.sn = dictionary["mfa_serial"]
        self.rolearn = dictionary["role_arn"]
        self.awsid = dictionary["aws_access_key_id"]
        self.secret = dictionary["aws_secret_access_key"]
        self.region = dictionary["region"]
        self.db = dictionary["dbinstanceidentifier"]
        self.service_type = dictionary["service_type"]
        self.mfa = str(input("Enter your MFA Code: "))
        try:
            self.login_aws = boto3.client("sts", aws_access_key_id= self.awsid, aws_secret_access_key= self.secret)
            self.assumed_role_object  = self.login_aws.assume_role(RoleArn= self.rolearn,
            RoleSessionName= "sessionname", SerialNumber= self.sn,TokenCode= self.mfa)
            self.temp_credentials = self.assumed_role_object["Credentials"]
            self.session = boto3.client(self.service_type, self.region,
                                        aws_access_key_id     = self.temp_credentials["AccessKeyId"],
                                        aws_secret_access_key = self.temp_credentials["SecretAccessKey"],
                                        aws_session_token     = self.temp_credentials["SessionToken"])
        except Exception as e:
            print("Error with details: ")
            print(e,sys.stdout)
            
    def restore_point_in_time(self,targetname,RestoreTime=None):
        try:
            pit = self.session.restore_db_instance_to_point_in_time(SourceDBInstanceIdentifier=self.db,TargetDBInstanceIdentifier=targetname,RestoreTime=RestoreTime)
            print(pit)
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)
            
    def restore_from_db_snapshot(self,Snapshot):
        try:
            snapshotdb = self.session.restore_db_instance_from_db_snapshot(DBInstanceIdentifier=self.db ,DBSnapshotIdentifier=Snapshot)
            print(snapshotdb)
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)

    def describe_db_engines_rds(self,Engine="postgres"):
        try:
            engines = self.session.describe_db_engine_versions(Engine=Engine)
            for engine in engines["DBEngineVersions"]:
                if engine["EngineVersion"] <= '9.4.19':
                    print(engine["EngineVersion"])
                    print(engine["DBEngineDescription"])
                    print(engine["DBEngineVersionDescription"])
                    print(engine["DBParameterGroupFamily"])
                    print("Supported Features : " + str(engine["SupportedFeatureNames"]))
                    print(engine["ValidUpgradeTarget"]["IsMajorVersionUpgrade"])
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)
          

    def describe_logfiles(self):
        try:
            logfiles = self.session.describe_db_log_files(DBInstanceIdentifier=self.db)
            for logs in logfiles["DescribeDBLogFiles"]:
                print("Log File Name: " + str(logs["LogFileName"]))
                print("Log File Last Written: " + str(logs["LastWritten"]))
                print("Log File Last Sizes: " + str(logs["Size"]))
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)

    def download_db_log_file_portion(self,log_name):
        try:
            download_logs = self.session.download_db_log_file_portion(DBInstanceIdentifier=self.db,LogFileName=log_name)
            return download_logs
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)
            
    def describe_snapshots(self):
        try:
            snapshots = self.session.describe_db_snapshots(DBInstanceIdentifier=self.db)
            try:
                for snapshot in snapshots["DBSnapshots"]:
                    print("DBSnapID: " + str(snapshot["DBSnapshotIdentifier"]))
                    print("DBID: " + str(snapshot["DBInstanceIdentifier"]))
                    print("DBSnapARN: " + str(snapshot["DBSnapshotArn"]))
                    print("SnapCreateTime: " + str(snapshot["SnapshotCreateTime"]))
                    print("isEncrypted: " + str(snapshot["Encrypted"]))
                    print("Engine Version: " + str(snapshot["EngineVersion"]))
                    print("Snapshot Type: " + str(snapshot["SnapshotType"]))
                    print("Availability Zone: " + str(snapshot["AvailabilityZone"]))
                    print("Status: " + str(snapshot["Status"]))
            except ValueError as V:
                print(V, sys.stderr)
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)

    @contextmanager
    def wait_for_availability(self, delay=160, retries=100):
        yield True
        try:
            waiter = self.session.get_waiter("db_instance_available")
            waiter.wait(DBInstanceIdentifier= self.db, WaiterConfig={"Delay": delay, "MaxAttempts": retries})
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)
            
    def modify_db_instance(self, version):
        try:
            with self.wait_for_availability():
                self.response = self.session.modify_db_instance(
                        DBInstanceIdentifier=self.db,
                        EngineVersion= version,
                        AllowMajorVersionUpgrade= True,
                        ApplyImmediately= True,
                    )
            self.describe_db_instances()
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)
           
    def describe_valid_db_instance_modifications(self):
        try:
            self.response = self.session.describe_valid_db_instance_modifications(
                    DBInstanceIdentifier=self.db)
            print(self.response["ValidDBInstanceModificationsMessage"])
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)
       
    def describe_db_instances(self):
        try:
            describe = self.session.describe_db_instances(DBInstanceIdentifier=self.db)
            for description in describe["DBInstances"]:
                print("Endpoint Address: " + str(description["Endpoint"]["Address"]))
                print("HostedZoneID: " + str(description["Endpoint"]["HostedZoneId"]))
                print("Endpoint Port: " + str(description["Endpoint"]["Port"]))
                print("Current Engine: " + str(description["Engine"]))
                print("Instance Class: " + str(description["DBInstanceClass"]))
                print("instance Status: " + str(description["DBInstanceStatus"]))
                print("Pending Modified Values: " + str(description["PendingModifiedValues"]))
                print("Engine Version: " + str(description["EngineVersion"]))
            oldversion = str(describe["DBInstances"][0]["EngineVersion"])
            time.sleep(10)
            print(time.ctime())
            describe = self.session.describe_db_instances(DBInstanceIdentifier=self.db)
            while describe["DBInstances"][0]["DBInstanceStatus"] != "available":
                print(describe["DBInstances"][0]["DBInstanceStatus"])
                print(describe["DBInstances"][0]["EngineVersion"])
                print(time.ctime())
                time.sleep(30)
                describe = self.session.describe_db_instances(DBInstanceIdentifier=self.db)
        except Exception as e:
            print("Error with details: ")
            print(e, sys.stderr)
        finally:
            print(time.ctime())
            print(describe["DBInstances"][0]["Endpoint"]["Address"])
            print(describe["DBInstances"][0]["EngineVersion"])
            print(describe["DBInstances"][0]["DBInstanceStatus"])
            newversion = str(describe["DBInstances"][0]["EngineVersion"])
            if oldversion == newversion:
                print("Engine has not upgraded")
                print("Old Version: " + oldversion)
                print("New Version: " + newversion)
            elif oldversion != newversion:
                print("engine Has upgraded")
                print("Old Version: " + oldversion)
                print("New Version: " + newversion)
            else:
                print(e, sys.stderr)

class s3_bucket(boto_client):
    def __init__(self):
        boto_client.__init__(self)
        config = configparser.ConfigParser()
        absolute =  os.path.dirname(os.path.abspath(__file__)) + "/rds_upgrades.ini"
        config.read(absolute)
        dictionary = {}
        options = config.options("s3")
        for option in options:
            try:
                dictionary[option] = config.get("s3", option)
                if dictionary[option] == -1:
                    print("skip: %s" % option)
            except:
                print("Exception")
                dictionary[option] = None
        self.bucket = dictionary["bucket"]
        self.object_name = dictionary["object_name"]
       
    def list_buckets(self):
        try:
            self.response = self.session.list_buckets()
            for bucket in self.response:
                print(bucket.name)
        except Exception as e:
            print("Error with details: ")
            print(e,sys.stderr)

    def list_objects(self):
        try:
            list = self.s3bucket.list_objects(bucket= self.bucket)
            for each in list:
                print(each)
        except Exception as e:
            print("Error with details: ")
            print(e,sys.stderr)

    def get_object(self):
        try:
            object = self.session.get_object(bucket= self.bucket,Key= self.object_name)
            return object["Body"]
        except Exception as e:
            print("Error with details: ")
            print(e,sys.stderr)

    def copy_to(self):
        try:
            self.response = self.s3bucket.copy_object()
        except Exception as e:
            print("Error with details: ")
            print(e,sys.stderr)

    def download_file(self,key,file):
        try:
            download = self.session.download_file(Bucket=self.bucket,key= key,Filename=file)
            return download
        except Exception as e:
            print("Error with details: ")
            print(e,sys.stderr)
if __name__ == "__main__":
    fire.Fire()
