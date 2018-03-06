import boto3
import os
import logging

from datetime import datetime, timedelta

CLOUDWATCH_PERIOD = 300
AWS_REGION = os.environ['REGION']
INSTANCE_ID = os.environ['INSTANCE_ID']
THRESHOLD = os.environ['THRESHOLD']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    try:
        instance = event.get('instance')
    except Exception as e:
        return "Exception! Failed with: {0}".format(e)

    client = boto3.client('ec2', region_name = AWS_REGION)
    response = client.describe_instance_credit_specifications(InstanceIds=[INSTANCE_ID])
    credit_type = response['InstanceCreditSpecifications'][0]['CpuCredits']
    if credit_type == 'standard':
        print "Unlimited disabled"

    cw = boto3.client('cloudwatch', region_name=AWS_REGION)
    response = cw.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUCreditBalance',
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance
            }
        ],
        StartTime=datetime.utcnow() - timedelta(seconds=CLOUDWATCH_PERIOD),
        EndTime=datetime.utcnow(),
        Period=CLOUDWATCH_PERIOD,
        Statistics=['Average']
    )
    met = response['Datapoints'][0]['Average']

    if met < THRESHOLD:
        modify = client.modify_instance_credit_specification(
            DryRun=False,
            InstanceCreditSpecifications=[
            {
                'InstanceId': instance,
                'CpuCredits': 'unlimited'
            },
            ]
           )
        print "changed to unlimited"
    if credit_type == 'unlimited' and met > THRESHOLD:
        modify = client.modify_instance_credit_specification(
            DryRun=False,
            InstanceCreditSpecifications=[
                {
                    'InstanceId': instance,
                    'CpuCredits': 'standard'
                },
            ]
        )
        print "changed to standard"

    return 'Done'
