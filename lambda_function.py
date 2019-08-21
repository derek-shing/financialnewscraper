import boto3
import json

LAMBDA_ACCESS_POLICY_ARN = "arn:aws:iam::093500706723:policy/LambdaS3AcccessPolicy"
LAMBDA_ROLE = "Lambda_Execution_Role"

LAMBBDA_ROLE_ARN ="arn:aws:iam::093500706723:role/Lambda_Execution_Role"


def lambda_client():
    aws_lambda = boto3.client('lambda',region = 'eu-west-1')
    return aws_lambda


def iam_client():
    iam = boto3.client('iam')
    """:type: pyboto3.iam"""
    return iam

def create_access_policy_for_lambda():
    s3_access_policy_document ={
        "Version":"2012-10-17",
        "Statement":[
            {
                "Action":[
                    "s3:*",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Effect":"Allow",
                "Resource":"*"
            }
        ]
    }

    return iam_client().create_policy(
        PolicyName = "LambdaS3AcccessPolicy",
        PolicyDocument = json.dumps(s3_access_policy_document),
        Description = "Allows lambda function to access s3 resources"
    )

def create_execution_role_for_lambda():
    lambda_execution_assumption_role={
        "Version":"2012-10-17",
        "Statement" : [
            {
                "Effect":"Allow",
                "Principal":{
                    "Service": "lambda.amazonaws.com"
                },
                "Action":"sts:AssumeRole"
            }
        ]
    }

    return iam_client().create_role(
        RoleName = LAMBDA_ROLE,
        AssumeRolePolicyDocument = json.dumps(lambda_execution_assumption_role),
        Description = "Gives necessary permission for lambda to be exected"
    )

def attach_policy_to_exection_role():
    return iam_client().attach_role_policy(
        RoleName=LAMBDA_ROLE,
        PolicyArn=LAMBDA_ACCESS_POLICY_ARN
    )




if __name__ =="__main__":
    #print (create_access_policy_for_lambda())
    #print(create_execution_role_for_lambda())
    print(attach_policy_to_exection_role())

