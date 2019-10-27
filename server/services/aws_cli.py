# import subprocess

class AwsCli(object):

    def getRecorceRecordValueByRecordSetName(recordSetName):
        # TODO: Get current RecordSetIP based on the name        
        return '1.2.4.5'

    def updateResourceRecord(ip_address):
        # TODO: Don't manually build this whole response. Get all the values but IP address by doing a GET on the the RecordSet
        update_string_json = """{
            "HostedZoneId": "Z7B5GAEZJQY49",
            "ChangeBatch": {
                "Comment": "Test - batch",
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": "nicky.domcc3.com",
                            "Type": "A",
                            "TTL": 300,
                        "ResourceRecords": [
                            {
                            "Value": "%s"
                            }
                        ]
                        }
                    }
                ]
            }
        }""" % ip_address
        # change_id = "/change/CWJXCGIWWEQT8"

        update_command = "aws route53 change-resource-record-sets --cli-input-json '{}'".format(update_string_json)
        # get_status_command = "aws route53 get-change --id {}".format(change_id)

        # print(update_command)
        
        # Actually update the AWS record
            # subprocess.call(update_command, shell=True) #might need to verify there is no shell injection

        return True