#!/usr/bin/env groovy

node {

    stage 'clone'
    checkout scm

    stage 'build'
    sh "nosetests"
}