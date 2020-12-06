# Smart-list
## Original idea:
The goal of our application is to create an online shopping list which would make the process of keeping track of your purchases more convenient, as well as providing additional features about shopping behaviour.
To do this we though about features which would correspond to the purchasing behaviour of users in real life. As an example, we noticed that for most of us, there was a certain pattern in the things that we purchase on a regular basis and wanted to integrate this purchasing behaviour into how people would make lists.
The basic features include the necessary functionalities to make shopping lists online, as well as convenience features such as the displaying of the most frequently bought items.
For the additional features, we wanted to implement some of the more advanced functionalities which we have covered in class,       


## Basic Features:
The very basic functionality is a simple shopping list which would provides the user with a personalised list of items for the current shopping list, as well as accounts of past lists based on a registered account. The items are added on one by one and saved with a unique session ID as soon as the list is finished. These session ID's would be used to provide access Users access to their past lists as well as for our analytics.
As mentioned before, we noticed that most people keep buying the same couple of items when they went shopping. To Make use of this behaviour, SmartList calculates the 5 most frequently bought items of a user and displays them while making new lists. The amount of items displayed in this way can be modified on the "my profile" page to the users liking.
Naturally, we also had to host the application through GCP to make it accessible online.   


## Additional features:
For the additional features, we tried to experiment with some of the functionalities we have covered in class to provide the user with more convenience while making shopping lists.

The "Scan Receipt" utilises Google's Vision API to upload past shopping lists to the users database. In this way, the user's suggested items could be  optimised without the hassle of typing in each item individually.

While the "Scan Receipt" function is meant to improve the items suggested to an user in a convenient way, the "find recipe" feature is meant to make finding the desired ingredients for a recipe easier and directly integrated into the process of making shopping lists. It asks the user about what he wants to cook, as well as dietary preferences and allergies amongst others. Making use of an API it then returns a list of ingredients which can be directly added to the current shopping list.

Furthermore, the analytics page provides the user with a comprehensive overview of their buying behaviour at a quick glance. It includes information about the composition of items bought.    

## Comments :
The additional features are the ones we think will be more time consuming and more difficult to implement. Therefore, as a beginning, we plan on having a site which analyses previous purchases (manually inputted by user) and outputs a possible shopping list for the user. Then, the additional features will serve to better the user experience by requiring less or no manual input. Also, some features that add recipes from databases to the shopping list are planned. In addition, the food intake analysis can become more advanced.
