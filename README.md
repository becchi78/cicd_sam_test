# cicd_sam_test

samを使ってLambda関数をデプロイするtemplateです。

## 実行方法

```bash
sam package --output-template-file packaged.yaml --s3-bucket $S3_BUCKET_NAME
sam deploy --template-file s3://$S3_BUCKET_NAME/packaged.yaml --stack-name <your-stack-name> --capabilities CAPABILITY_IAM
```

## CI/CD

CodePipeline による CI/CD を実行する場合には以下のリソースを作成する。

### CodePipeline

`aws codepipeline get-pipeline --name cicd-sam-test`

``` json
{
    "pipeline": {
        "name": "cicd_sam_test",
        "roleArn": "arn:aws:iam::571634110936:role/CodePipelineServiceRole",
        "artifactStore": {
            "type": "S3",
            "location": "codepipeline-ap-northeast-1-691348252728"
        },
        "stages": [
            {
                "name": "Source",
                "actions": [
                    {
                        "name": "Source",
                        "actionTypeId": {
                            "category": "Source",
                            "owner": "AWS",
                            "provider": "CodeStarSourceConnection",
                            "version": "1"
                        },
                        "runOrder": 1,
                        "configuration": {
                            "BranchName": "develop",
                            "ConnectionArn": "arn:aws:codeconnections:ap-northeast-1:571634110936:connection/5a4bc021-cfb9-4969-be8e-581867599351",
                            "DetectChanges": "false",
                            "FullRepositoryId": "becchi78/cicd_sam_test",
                            "OutputArtifactFormat": "CODE_ZIP"
                        },
                        "outputArtifacts": [
                            {
                                "name": "SourceArtifact"
                            }
                        ],
                        "inputArtifacts": [],
                        "region": "ap-northeast-1",
                        "namespace": "SourceVariables"
                    }
                ]
            },
            {
                "name": "Build",
                "actions": [
                    {
                        "name": "Build",
                        "actionTypeId": {
                            "category": "Build",
                            "owner": "AWS",
                            "provider": "CodeBuild",
                            "version": "1"
                        },
                        "runOrder": 1,
                        "configuration": {
                            "ProjectName": "Codebuild-cicd-sam-test"
                        },
                        "outputArtifacts": [
                            {
                                "name": "BuildArtifact"
                            }
                        ],
                        "inputArtifacts": [
                            {
                                "name": "SourceArtifact"
                            }
                        ],
                        "region": "ap-northeast-1",
                        "namespace": "BuildVariables"
                    }
                ]
            },
            {
                "name": "Deploy",
                "actions": [
                    {
                        "name": "Deploy",
                        "actionTypeId": {
                            "category": "Deploy",
                            "owner": "AWS",
                            "provider": "CloudFormation",
                            "version": "1"
                        },
                        "runOrder": 1,
                        "configuration": {
                            "ActionMode": "CREATE_UPDATE",
                            "Capabilities": "CAPABILITY_IAM,CAPABILITY_NAMED_IAM,CAPABILITY_AUTO_EXPAND",
                            "RoleArn": "arn:aws:iam::571634110936:role/CodePipelineServiceRole",
                            "StackName": "cicd-sam-test",
                            "TemplatePath": "BuildArtifact::packaged.yaml"
                        },
                        "outputArtifacts": [],
                        "inputArtifacts": [
                            {
                                "name": "BuildArtifact"
                            }
                        ],
                        "region": "ap-northeast-1",
                        "namespace": "DeployVariables"
                    }
                ]
            }
        ],
        "version": 4,
        "executionMode": "QUEUED",
        "pipelineType": "V2",
        "triggers": [
            {
                "providerType": "CodeStarSourceConnection",
                "gitConfiguration": {
                    "sourceActionName": "Source",
                    "push": [
                        {
                            "branches": {
                                "includes": [
                                    "develop"
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    },
    "metadata": {
        "pipelineArn": "arn:aws:codepipeline:ap-northeast-1:571634110936:cicd_sam_test",
        "created": "2024-08-13T12:25:07.401000+09:00",
        "updated": "2024-08-19T11:07:39.848000+09:00"
    }
}
```

### CodeBuild

`aws codebuild batch-get-projects --names Codebuild-cicd-sam-test`

```json
{
    "projects": [
        {
            "name": "Codebuild-cicd-sam-test",
            "arn": "arn:aws:codebuild:ap-northeast-1:571634110936:project/Codebuild-cicd-sam-test",
            "source": {
                "type": "CODEPIPELINE",
                "buildspec": "buildspec.yml",
                "insecureSsl": false
            },
            "secondarySources": [],
            "secondarySourceVersions": [],
            "artifacts": {
                "type": "CODEPIPELINE",
                "name": "Codebuild-cicd-sam-test",
                "packaging": "NONE",
                "encryptionDisabled": false
            },
            "secondaryArtifacts": [],
            "cache": {
                "type": "NO_CACHE"
            },
            "environment": {
                "type": "LINUX_CONTAINER",
                "image": "aws/codebuild/amazonlinux2-x86_64-standard:5.0",
                "computeType": "BUILD_GENERAL1_SMALL",
                "environmentVariables": [],
                "privilegedMode": false,
                "imagePullCredentialsType": "CODEBUILD"
            },
            "serviceRole": "arn:aws:iam::571634110936:role/Codebuild-cicd-sam-test",
            "timeoutInMinutes": 60,
            "queuedTimeoutInMinutes": 480,
            "encryptionKey": "arn:aws:kms:ap-northeast-1:571634110936:alias/aws/s3",
            "tags": [],
            "created": "2024-08-13T12:22:49.324000+09:00",
            "lastModified": "2024-08-13T12:35:30.093000+09:00",
            "badge": {
                "badgeEnabled": false
            },
            "logsConfig": {
                "cloudWatchLogs": {
                    "status": "ENABLED"
                },
                "s3Logs": {
                    "status": "DISABLED",
                    "encryptionDisabled": false
                }
            },
            "fileSystemLocations": [],
            "projectVisibility": "PRIVATE"
        }
    ],
    "projectsNotFound": []
}
```

`aws codebuild batch-get-projects --names Codebuild-DriftDetection-cicd-sam-test`

```json
{
    "projects": [
        {
            "name": "Codebuild-DriftDetection-cicd-sam-test",
            "arn": "arn:aws:codebuild:ap-northeast-1:571634110936:project/Codebuild-DriftDetection-cicd-sam-test",
            "source": {
                "type": "CODEPIPELINE",
                "insecureSsl": false
            },
            "secondarySourceVersions": [],
            "artifacts": {
                "type": "CODEPIPELINE",
                "name": "Codebuild-DriftDetection-cicd-sam-test",
                "packaging": "NONE",
                "encryptionDisabled": false
            },
            "cache": {
                "type": "NO_CACHE"
            },
            "environment": {
                "type": "LINUX_CONTAINER",
                "image": "aws/codebuild/amazonlinux2-x86_64-standard:5.0",
                "computeType": "BUILD_GENERAL1_SMALL",
                "environmentVariables": [],
                "privilegedMode": false,
                "imagePullCredentialsType": "CODEBUILD"
            },
            "serviceRole": "arn:aws:iam::571634110936:role/service-role/Codebuild-DriftDetection-cicd-sam-test",
            "timeoutInMinutes": 60,
            "queuedTimeoutInMinutes": 480,
            "encryptionKey": "arn:aws:kms:ap-northeast-1:571634110936:alias/aws/s3",
            "tags": [],
            "created": "2024-08-14T10:22:10.357000+09:00",
            "lastModified": "2024-08-14T10:22:10.357000+09:00",
            "badge": {
                "badgeEnabled": false
            },
            "logsConfig": {
                "cloudWatchLogs": {
                    "status": "ENABLED"
                },
                "s3Logs": {
                    "status": "DISABLED",
                    "encryptionDisabled": false
                }
            },
            "projectVisibility": "PRIVATE"
        }
    ],
    "projectsNotFound": []
}
```

### IAM role

`aws iam get-role --role-name Codebuild-cicd-sam-test`

```json
{
    "Role": {
        "Path": "/",
        "RoleName": "Codebuild-cicd-sam-test",
        "RoleId": "AROAYKGAMKHMPNLOYF4U4",
        "Arn": "arn:aws:iam::571634110936:role/Codebuild-cicd-sam-test",
        "CreateDate": "2024-08-13T03:32:55+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "codebuild.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        },
        "Description": "",
        "MaxSessionDuration": 3600,
        "RoleLastUsed": {
            "LastUsedDate": "2024-08-19T02:24:38+00:00",
            "Region": "ap-northeast-1"
        }
    }
}
```

`aws iam get-role --role-name Codebuild-DriftDetection-cicd-sam-test`

```json
{
    "Role": {
        "Path": "/service-role/",
        "RoleName": "Codebuild-DriftDetection-cicd-sam-test",
        "RoleId": "AROAYKGAMKHMK3PCS4BX4",
        "Arn": "arn:aws:iam::571634110936:role/service-role/Codebuild-DriftDetection-cicd-sam-test",
        "CreateDate": "2024-08-14T01:22:03+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "codebuild.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        },
        "MaxSessionDuration": 3600,
        "RoleLastUsed": {}
    }
}
```

## IAM Policy

CodeBuildBasePolicy-Codebuild-cicd-sam-test-ap-northeast-1

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Resource": [
                "arn:aws:logs:ap-northeast-1:571634110936:log-group:/aws/codebuild/Codebuild-cicd-sam-test",
                "arn:aws:logs:ap-northeast-1:571634110936:log-group:/aws/codebuild/Codebuild-cicd-sam-test:*"
            ],
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ]
        },
        {
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::codepipeline-ap-northeast-1-*"
            ],
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "codebuild:CreateReportGroup",
                "codebuild:CreateReport",
                "codebuild:UpdateReport",
                "codebuild:BatchPutTestCases",
                "codebuild:BatchPutCodeCoverages"
            ],
            "Resource": [
                "arn:aws:codebuild:ap-northeast-1:571634110936:report-group/Codebuild-cicd-sam-test-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::cicd-sam-test-artifacts-bucket",
                "arn:aws:s3:::cicd-sam-test-artifacts-bucket/*"
            ]
        }
    ]
}
```

CodeBuildBasePolicy-Codebuild-DriftDetection-cicd-sam-test-ap-northeast-1

``` json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Resource": [
                "arn:aws:logs:ap-northeast-1:571634110936:log-group:/aws/codebuild/Codebuild-DriftDetection-cicd-sam-test",
                "arn:aws:logs:ap-northeast-1:571634110936:log-group:/aws/codebuild/Codebuild-DriftDetection-cicd-sam-test:*"
            ],
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ]
        },
        {
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::codepipeline-ap-northeast-1-*"
            ],
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "codebuild:CreateReportGroup",
                "codebuild:CreateReport",
                "codebuild:UpdateReport",
                "codebuild:BatchPutTestCases",
                "codebuild:BatchPutCodeCoverages"
            ],
            "Resource": [
                "arn:aws:codebuild:ap-northeast-1:571634110936:report-group/Codebuild-DriftDetection-cicd-sam-test-*"
            ]
        }
    ]
}
```