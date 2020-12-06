# Smart-list
## Original idea:
The goal of our application is to create an online shopping list which would make the process of keeping track of your purchases more convenient, as well as providing additional features about shopping behaviour.
To do this we though about features which would correspond to the purchasing behaviour of users in real life. As an example, we noticed that for most of us, there was a certain pattern in the things that we purchase on a regular basis and wanted to integrate this pattern in the purchasing behaviour into how people would make lists.
The basic features include the necessary functionalities to make shopping lists online, as well as convenience features such as the displaying of the most frequently bought items.
For the additional features, we wanted to implement some of the more advanced functionalities which we have covered in class to make the user experience smoother and to provide basic analytical features.



## Basic Features:
The very basic functionality is a simple shopping list which would provides the user with a personalised list of items for the current list, as well as accounts of past lists, all based on a registered account. The items are added on one by one and saved with a unique session ID as soon as the list is finished. These session ID's would be used to provide Users access to their past lists as well as for our analytics.

As mentioned before, we noticed that most people keep buying the same couple of items when they went shopping. To Make use of this behaviour, SmartList calculates the 5 most frequently bought items of a user and displays them while making new lists. The amount of items displayed in this way can be modified on the "my profile" page to the users liking.

Making the application aesthetically pleasing was also one of the basic features necessary. The site layout and composition of the cards are written in CSS. Additionally we decided to add images of the groceries along the items card. To do this, we made use of the unsplash API.   

Naturally, we also had to host the application and the corresponding SQL database on  GCP to make it accessible online.   


## Additional features:
For the additional features, we tried to experiment with some of the functionalities we have covered in class to make the user experience as smooth as possible.

The "Scan Receipt" utilises Optical Image Recognition API to upload past shopping lists to the users database. In this way, the user's suggested items can be optimised without the hassle of typing in each item individually.

While the "Scan Receipt" function is meant to improve the items suggested to an user in a convenient way, the "find recipe" feature is meant to make finding the desired ingredients for a recipe easier and directly integrated into the process of making shopping lists. It asks the user about what he wants to cook, as well as dietary preferences and allergies amongst others. Making use of an API it then returns a list of ingredients which can be directly added to the current shopping list.

Furthermore, the analytics page provides the user with a comprehensive overview of their buying behaviour at a quick glance. It includes information about the composition of items bought.    
=======
Furthermore, the analytics page provides the user with a comprehensive overview of their buying behaviour at a quick glance. It includes information about the composition of items bought amongst others.

## How to run Smartlist:
To Launch the application on your machine, you need to run the startup.py first to initiate the database. Subsequently you need to install the necessary python packages we have utilised such as flask, datetime and OS, amongst many others. After you have installed the packages you should be able to run the application by executing main.py through the command line.  

## How to use Smartlist
Smartlist provides you with everything you need to write, modify and view shopping lists. Additionally, SmartList provides you with a list of your most frequently bought items, functionalities to add items based on recipes and a basic analytics page.

To make use of these features, you first of all need to make an account by clicking on the _register_ button found in the Navbar. After the registration and login, head to the main page to make your first SmartList!

The items you wish to put onto your list are added one by one trough the _add product_  


## Challenges and Issues:
The additional features are the ones we think will be more time consuming and more difficult to implement. Therefore, as a beginning, we plan on having a site which analyses previous purchases (manually inputted by user) and outputs a possible shopping list for the user. Then, the additional features will serve to better the user experience by requiring less or no manual input. Also, some features that add recipes from databases to the shopping list are planned. In addition, the food intake analysis can become more advanced.
