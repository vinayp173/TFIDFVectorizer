# TFIDFVectorizer
  This an django project is short demo of TFIDFVectorizer from sklearn library
# what it can do ?
  This project take large corpus of documents in it's media\documents\allDocuments\combo folder.
  Which then get processed and TF-IDF weights are calculated and stored in database which then can be used for searching with provided keywords.
# Configure
  We have used mysql database "XYZ.sql" import this file in mysql. it is alreday filled with the information which is extarcted from it's inbuilt corpus.
# how to start new ?
  just truncate old database and replace documents from media\documents\allDocuments\combo folder with yours and done.
# how it will work ?
  >it's UI is not well designed so it's extraction and search module can only be accessible using URL's
  > if your running this django project on default configuration then<br>
     URL's are, Extraction 127.0.0.1:8000/TF<br>
     for searching module  127.0.0.1:8000/search
