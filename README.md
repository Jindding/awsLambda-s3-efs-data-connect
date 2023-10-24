# awsLambda-s3-efs-data-connect

## Table of Contents
1. [Overview](#overview)
2. [Purpose](#purpose)
3. [Configuration](#configuration)
4. [Test Cases](#test-cases)

## Overview

This feature allows for the replication of files and directories uploaded to or deleted from an S3 bucket to an EFS system. 

## Purpose

This function was developed to enable Windows PC users to upload or delete files on an EFS system. EFS cannot be directly mounted on Windows Local PCs. Therefore, by using the Storage Gateway to connect S3 via SMB, users can upload files to S3 through the connected folders.

## Configuration

![image](https://github.com/Jindding/awsLambda-s3-efs-data-connect/assets/49447802/5c27debc-41e4-4fc6-a982-155724df5b3a)


## Test Cases

(List the test cases relevant to this feature)

