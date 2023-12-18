# mooc-cyber-security-base-project1
LINK: https://github.com/emiliarantonen/mooc-cyber-security-base-project1

Registered users:

Username: alice

Password: redqueen


Username: bob

Password: squarepants

FLAW 1: SQL Injection
FLAW: https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L25

FIX: https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L31

SQL injection is a vulnerability that poses a significant risk to web applications. Injection vulnerabilities occur when application doesn’t properly handle data provided by users. This could lead to unauthorized access or manipulation of sensitive data in the database. In my application, an attacker might bypass authentication checks or access data that they are not supposed to by injecting SQL commands into the ‘username’ input field. [1]

To fix this flaw, one possible way is to use parametrized queries and Django’s built in methods like ‘filter’ to construct queries safely. This method constructs the query internally and safely handles the parameter of users id. When using the ‘filter’ method, it is retrieving the notes belonging to logged in user from database safely, and user cannot manipulate the process.

FLAW 2: Broken Access Control
FLAW: https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L46

FIX: https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L48

Broken access control refers to a security vulnerability where users can access resources or perform actions that they don’t have permission in an application. This might lead to unauthorized access to sensitive data or functionalities. In my application due to broken access control a user that doesn’t own the note, can edit the data in it. That might happen because the application doesn’t check that the user owns the note before allowing to edit it. The application retrieves the note that will be edited based on notes id, and that has nothing to do with logged in user. [2]

To fix this flaw in my notes application there is implemented a verification step to ensure that the user editing the note is actually owner of that note. This permission is verified before allowing any edits to be made. If the user is not same, user gets message that tells there is no permission to edit that note.

FLAW 3: Broken Authentication
FLAW: https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L67

FIX: https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L68

Broken Authentication means weaknesses in user identification, authentication, and session management. It might lead to unauthorized access due to weak password policies, inadequate session management or exposing session identifiers. This enables attackers to gain unauthorized entry or control user sessions. In my application broken authentication implements in password policies. There are no strict criteria for password creation, allowing users to set common and weak passwords without any restrictions.[3]

To fix this flaw, there has been created a function called ‘registration’. This can be used in Django shell while creating new users. The function ensures that new passwords adhere to stronger validation criteria. To implement this there is used Django’s built in functions to validate password for example certain length and including letters and numbers. Using this function, when creating new users, helps to avoid common or weak passwords. 

FLAW 4: CSRF (Cross-Site Request Forgery)
FLAW:  https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/templates/homePage.html#L10

https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L25

https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/templates/edit.html#L10

https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L50


FIX: https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/templates/homePage.html#L11

https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L27

https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/templates/edit.html#L11

https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/views.py#L53


Cross-site Request Forgery (CSRF) is an attack that allows a different site to send fake requests to web application you are logged in. When you visit another site, your browser may unknowingly send you authentication token to the web app you are currently using. This lets the attackers access the data as they were you. In my application I don’t have ‘csrf_token’ tag in my homepage and editing views. That means these views don’t check if the incoming POST requests has a valid CSRF token. I also have ‘csrf_exempt’ tag in my home, edit and delete functions, which removes CSRF protection from the view. Due to that my application is vulnerable to POST requests being made from other sites.[4]

To fix this flaw the ‘csrf_exempt’ tag has to be changed to ‘csrf_protect’ tag. Additionally ‘csrf_token’ tag need to be added in my homepage and edit views html files. This makes sure, due to Django’s built in models, that homepage and editing views check that incoming POST requests has a valid CSRF token. 


FLAW 5: Cross-Site Scripting
FLAW: https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/templates/homePage.html#L25

 https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/templates/edit.html#L16


FIX: https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/templates/homePage.html#L26

 https://github.com/emiliarantonen/mooc-cyber-security-base-project1/blob/main/notes/templates/edit.html#L17


Cross-Site Scripting (XSS) is a vulnerability that allows users to inject malicious scripts into website which executes on other users’ machines. The malicious content can be stored permanently in the web application for example in databases. User-generated content has a higher risk of being malicious. Therefore it is essential to focus more on preventing that. These attacks can enable session hijacking, allowing attackers to impersonate users. In my application XSS occurs when user-provided content while editing notes is not sanitized. I have used ‘safe’ filter while inserting content. When using that, Djangos built in automated escape is turned off. That means the content is setted ’safe’ and it will not be escaped. It allows an attacker to inject and execute malicious scripts. [1][4]

To fix this flaw I have removed ‘safe’ filters and added Django templates ‘escape’ filter instead. This is used in user-generated contents of notes. This is used in both adding and editing notes. This will escape special characters preventing any code or malicious content being executed in the browser. 

Sources:
1.	 OWASP Top 10, A03:2021 Injection (2021) https://owasp.org/Top10/A03_2021-Injection/
2.	OWASP Top 10, A01:2021 Broken Access Control (2021), https://owasp.org/Top10/A01_2021-Broken_Access_Control/
3.	OWASP Top 10, A07:2021 Identification and Authentication Failures (2021), https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
4.	MOOC Cyber Security Base 2023, Most Common Security Vulnerabilities, https://cybersecuritybase.mooc.fi/module-2.3/1-security


