# CS361_README
# Joonbum Kang
# communication contract

# How to request data from Microservice A
1. To request data from Microservice A, you need "MA_pn.py" which is provided in this repository.
2. Make sure python is installed in your environment with additional extensions.
   For example, Python can be installed using the command "pip install python" 
3. Run the file with the microservice on seperate terminals and it'll request the data of username and action about their post.

# How to receive data from Microservice A
1. After the file is run, leave the file running on the terminal so that it's in the infinite loop to receive a post notification from the microservice.
   If either a post is uploaded or deleted in the microservice, you'll receive the requested data from it.
2. When a post is uploaded or deleted, on the terminal, you'll receive a message saying "user {username} has {created/deleted} a post"
