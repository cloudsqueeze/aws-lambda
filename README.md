# T2 unlimited lambda

Trigger Lambda that enables T2 unlimited when CPUCreditBalance is below a threshold 
Lambda is invoked by SNS triggered Alarm

# How to use

Deploy the application and specify threshold, instance id and region.

Since AWS SAM does not support custom IAM policies you will need to create an Inline policy and attach it to the role that is being used by lambda.
Policy should contain:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:ModifyInstanceCreditSpecification",
                "ec2:DescribeInstanceCreditSpecifications",
                "ec2:ModifyInstanceCreditSpecification",
                "cloudwatch:GetMetricStatistics"
            ],
            "Resource": "*"
        }
    ]
}
```


## License

MIT License (MIT)
