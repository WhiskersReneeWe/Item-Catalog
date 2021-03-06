# Item Catalog - A Udacity project 
## This is my second Full Stack Project-Based learning experience using Flask ([First Experience here](https://github.com/WhiskersReneeWe/keras_image_classifer))

# Introduction

This is a Flask Web Application that displays items for a sports store! This is a very basic web app where a user can add, edit, or delete an item within his/her chosen category. This web app allows a user sign in and sign out but only using Google accounts. I use OAuth to authenticate users to grant them the capabilities to add, edit, and delete items they have created before. 

The webpage design is at its bare minimum because the focus of this project is on its backend. I will learn more about the frontend design later on.


# Usage
## Note, it is recommended to set up an Anaconda environment to get this app start running. 


0. Download all files from this repository to your local computer and store them in one directory.
1. Fire up an Anaconda Prompt, use the following command to create a virtual environment.
    * cd `your local directory` (change the working directory to where you store all the downloaded files in step 0)
    * `conda create -n itemcatalog_project --file itemcatalog_env.yml` (This creates a virtual environment named itemcatalog_project using python packages within itemcatalog_env.yml)


2. run the following commands,
   * `python app.py` 
   
3. When it is up and running, go to http://127.0.0.1:5000
4. The display should be like this,

![itemHome](https://user-images.githubusercontent.com/43501958/57992640-180ae500-7a6a-11e9-9467-1d80a7bdf0a1.JPG)


# Acknowledgement

* Udacity Mentor Tim Nelson
* Udacity Full Stack Nanodegree group
* [Cited this for various aspects of my development process](https://github.com/rrjoson/udacity-item-catalog)
