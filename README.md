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

The "Scan Receipt" utilises an OCR API to upload past shopping lists to the users database. In this way, the user's suggested items can be optimised without the hassle of typing in each item individually.

While the "Scan Receipt" function is meant to improve the items suggested to an user in a convenient way, the "find recipe" feature is meant to make finding the desired ingredients for a recipe easier and directly integrated into the process of making shopping lists. It asks the user about what he wants to cook, as well as dietary preferences and allergies amongst others. Making use of an API it then returns a list of ingredients which can be directly added to the current shopping list.

Furthermore, the analytics page provides the user with a comprehensive overview of their buying behaviour at a quick glance. It includes information about the composition of items bought amongst others.

## How to run Smartlist:
To Launch the application on your machine, you need to run the startup.py first to initiate the database. Subsequently you need to install the necessary python packages we have utilised such as flask, datetime and OS, amongst many others. After you have installed the packages you should be able to run the application by executing main.py through the command line.  

## How to use Smartlist
Smartlist provides you with everything you need to write, modify and view shopping lists. Additionally, SmartList provides you with a list of your most frequently bought items, functionalities to add items based on recipes and a basic analytics page.

### Navigating the Main Page



To make use of these features, you first of all need to make an account by clicking on the _register_ button found in the Navbar. After the registration and login, head to the main page to make your first SmartList!

The items you wish to put onto your list are added one by one under the _add a product to your Shoppinglist_ subheader. To add the product to the list simply click the _submit_ button.

After you are finished with the Shopping List click the _save list_ button at the bottom of the page. From now on your most frequently bought items will be displayed under the _the items you most often buy_ subheader. You can adapt the amount of items displayed in this way on the _my profile_ page, accessible through the navbar. On the Navbar you will also find _upload receipt_. Through this functionality you can upload past shopping receipts to improve the items it will suggest to you in the future!




## Challenges and Issues:
During our work process, we encountered numerous issues relating to the scope of the features and also to how we could effectively collaborate online.

Especially for the advanced features, we severely underestimated the effort of implementing some of them as we originally intended. As an example, we originally intended the analytics page to be unique to each user. However, we were not able to exclusively select the data from one user and were not able to correct this due to time constraints.
Similarly, we had to do away with other advanced features, such as a functionality which would allow users to search for a recipe based on a picture. In general, these problems were due to our underestimation of how the complexity of the code rose exponentially with the more features we wanted to implement. The revisions to the database and other parts of the code which were necessary to implement additional features took considerably more time than implementing the basic features.
However, we found priority lists and the division of functionalities into the _necessary_ basic ones and the _nice to have_ advanced ones to be useful to mitigate these issues.
For any future projects, we think that we could improve on such issue by having a clear priority list, but also by formulating potential additional features in a more concise way from the beginning onwards. By having a clearer idea of what could be added in the next stages, the code could be written in a way to accommodate these features from the beginning.  


As for our work process, we also found it more difficult than expected to successfully collaborate online. Especially during the process of articulating the ideas, the challenge of successfully conveying what we wanted the features to be and how we could implement them, was made considerably more difficult by being restricted to online channels. When we were able to physically meet in St. Gallen, we found that our ideas of how to go about realising the features where sometimes considerably different.
Getting used to collaborating on Github also took some time to get used to. We experienced some issues with getting everyone on the same repository, as well as the habits of pushing changes regularly and merging conflicts in the beginning. We also found it challenging to work on the same features in parallel, which we did away with by more clearly dividing up the tasks. In Conclusion, GitHub proved itself to be an invaluable asset for collaborating online after we got used to it.
For future projects, it could be useful to look into additional online communication tools to visually convey our ideas.
