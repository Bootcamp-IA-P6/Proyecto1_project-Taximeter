# project-Taximeter

En este proyecto vamos a realizar una app que nos indique 
el costo a la hora de elgir un proyecto s

MIDDLE LEVEL
    1. Implement a logging system for code traceability
    2.Add unit tests to ensure the program works correctly.
    3.Create a historical record of past trips in a plain text file
    4.It allows you to configure prices to adapt to current demand 

 Advanced level 
 1 Refactor the code using an object-oriented approach (OOP).
2 Implement a password-based authentication system to protect access to the program.
3 Develop a graphical user interface (GUI) to make the program more user-friendly.

2 Implement a password-based authentication system to protect access to the program.
The `authenticate()` function

Requests a username and password upon startup.

Compares them against the authorized values ​​(in this example, admin/1234).

Returns `True` if authentication is successful and `False` if it fails.

Integration into the main flow

Before `TaximeterApp.run()` starts, `authenticate()` is called.

The application only runs if authentication is successful.

If it fails, the program terminates immediately.

Immediate benefits

Protects your taximeter without modifying trip logic, storage, or logging.

Maintains the modularity and object-oriented programming (OOP) of your code.