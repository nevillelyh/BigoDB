#!/usr/bin/env python

import os

import bigodb

def main():
    bigodb.scan()
    bigodb.gc()

if __name__ == '__main__':
    main()
