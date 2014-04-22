djangoShop
==========

This is a Django shop that sells bikes, books and music. [Expanded University Project]

The project has no database, to use it you should type `$ ./manage.py syncdb`


You can access the demo on heroku:

>http://pabloparejo.herokuapp.com

> want to try the admin?
    Just type :
        ```http://pabloparejo.herokuapp.com/admin
        
            user = admin
            pass = admin
        ```


Product popularity:
------------------

Gets bigger when:

    1) You watch it (+1)
    2) You buy it   (+quantity)

Reduces when:

    1) You don't watch it