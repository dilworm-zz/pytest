#!/bin/bash
g++ addressbook.pb.h addressbook.pb.cc readaddress.cpp -o readaddr -lprotobuf -lpthread
g++ addressbook.pb.h addressbook.pb.cc writeaddress.cpp -o writeaddr -lprotobuf -lpthread
