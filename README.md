# Got Work?
## Group Members
Aryan Osqueezadeh, Bryce Flammer, Jacob Holbrook, Matthew Hill

## Workspace Origanization
The Got Work? app will be stored in this repository. Database files will NOT be stored in this repo, so database migrations for testing purposes will be created.
Jira Software's Agile Board, through Atlassian, will be used to keep track of issues, sprints, and responsibilities of group members using an Agile process. [Agile Board](https://super-awesome-lawnmowers.atlassian.net/jira/software/c/projects/SAL/boards/1)

### Name Scheme
- Directories
    - Underscores between words
    - lowercase
    - Names will be as short as possible.
- Files
    - Underscores between words
    - lowercase
    - Maximum 6 words in file name
- Code formatting
    - Follow standard coding practice.
    - Variables and functions/methods are named in lowerCamelCase, with descriptive names.
    - Classes are named in UpperCamelCase, with descriptive names.
- Database formatting
    - Data objects are named in UpperCamelCase, with descriptive names.
    - Data fields are named in lowerCamelCase, with descriptive names.
- CSS
    - Use the BEM naming convention:
        - blocks are word separated by "-". 
        - elements are separated from the rest by "__"
        - modifiers are separated from the rest by "--"
        
## Version-Control Procedures
Aryan has the main repository; everyone else forked from his repo through github. We will make pull requests to Aryan's repo, and anyone can review and merge those requests. Aryan will make pull requests from a branch seperate from `main`.
Aryan will look at and approve/deny any outstanding pull requests every Tuesday/Thursday around class time. 
The repository link is available to the GTA.

## Tool stack description and setup procedure
- Jira Software's Agile Board
    - Used to keep track of issues, sprints, and responsibilities using an Agile method.
- HTML
    - Used in combination with CSS and JS to create the front end of the website.
- CSS
    - CSS is used for front end layout and visual design.
- Javascript with Vue.js
    - JS is sed for front end behaviour and interactive updates to the DOM. Vue.js provides a clean framework to do so, one which we all have experience with.
- Django
    - Used for backend and database interactions. All members in the group have experience with Django.
- Draw.io
    - UML Diagramming software. Used to create diagrams such as class diagrams, use case diagrams, and activity diagrams.
- Pixilart.com
    - Simple pixlel art web program. May use for icons and other graphics.
- octopus.do
    - Used for wireframe prototype(s).
- freefavicon.com
    - Used to download the favicon used for the website.

## Build instruction

1. Clone the [repo](https://github.com/AryanUSU/5-Super-Awesome-Lawnmowers "SAL Repo")
2. CD into the repo `5-Super-Awesome-Lawnmowers/app/gotwork`
3. (Optional) Run `python manage.py makemigrations` and then `python manage.py migrate`
4. Run `python manage.py runserver`
5. In a browser, navigate to `localhost:8000`
6. Enjoy the app! Because no database files are kept within the repo, use the migrations provided for testing purposes.

## Unit Testing instructions
1. Clone the [repo](https://github.com/AryanUSU/5-Super-Awesome-Lawnmowers "SAL Repo")
2. Run `python manage.py test` from the command line from within the repo at `5-Super-Awesome-Lawnmowers/app/gotwork`. This will run automated unit tests that test some of the functions within utility.py
3. If no errors or failures appear in testing, it should say "OK" along with other debug info
4. If errors of failures appear in testing, it will describe them. Please let us know if any of the tests fail :).
5. **Don't over refresh the worker home page.** The API used to see if a job is too far away from a worker only allows 10 queries per hour with a free plan. As broke students, that's the option we went for. Therefore, the unit test `test_get_worker_pending_jobs` will fail after 10 queries to the API. This also effects loading a worker's home page. In a real deployment, there would be a budget, so this would not be a problem.
 

## System Testing instructions
1. Clone the [repo](https://github.com/AryanUSU/5-Super-Awesome-Lawnmowers "SAL Repo")
2. Run `python manage.py migrate` from the command line from within the repo at `5-Super-Awesome-Lawnmowers/app/gotwork`. This sets up some data with which to test, inlcuding example users and jobs. 
    1. There are three customer users: Logan, Boise, and Manhattan.
        - Logan's login: Username: Logan | Password: Logan
        - Boise's login: Username: Boise | Password: Boise
        - Manhattan's login: Username: KingOf | Password: Manhattan
    2. There are four worker users: Billy, Tommy, Sam, and Wolf
        - Billy's login: Username: billyjoel | Password: billyjoel
        - Sam's login: Username: sammy | Password: sammy
	    - Wolf's login: Username: wolf| Password: ofwallstreet
	    - Tommy's login: Username: Tommyboy| Password: Tommyboy
	    - All workers have avaliable times set up except Tommy. His can be set up in his respective settings page.
    3. There is one owner user: Owner
        - Owner's login: Username: owner | Password: owner
    4. There are three job types:
        - Lawn Mowing
        - Snow Blowing
        - Leaf Raking
    5. There are four jobs available to be worked:
        - A job for Lawn Mowing:
            - zipCode: 83261 (Paris, Idaho)
            - Customer: Logan
        - A job for Leaf Raking:
            - zipCode: 84321 (Logan)
            - Customer: Logan
        - A job for Snow Blowing:
            - zipCode: 83709 (Boise)
            - Customer: Boise
	- A job for Lawn Mowing:
	    - zipCode: 10001 (New York City)
	    - Customer: Manhattan
    6. There is one active job:
	- A job for Snow Blowing
	    - zipCode: 84332
	    - Customer: Logan
	    - Worker: Tommy
     7. There is one job with a refund request pending
	- A job for Snow Blowing
	    - zipCode: 10001
	    - Customer: Manhattan
	    - Worker: Wolf
    
3. Follow the build instructions provided previously.
4. Navigate to `localhost:8000` to go to the home page. You can use the provided info above to log in and test the home pages, settings pages, and other pages. You can also sign up to create a new user to test as well.
5. Customers can create jobs, and all settings can be changed to test different senarios.
6. **Don't over refresh the worker home page.** The API used to see if a job is too far away from a worker only allows 10 queries per hour with a free plan. As broke students, that's the option we went for. Therefore, the worker home page will not display correctly if too many requests are made too fast. This also effects the unit test `test_get_worker_pending_jobs`. In a real deployment, there would be a budget, so this would not be a problem.
