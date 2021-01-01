# Equation Symbol Visualization

Equation Symbol Visualization is a [__dash app__](http://dash.plotly.com) created to create a visual representation of information flow for 
systems of equations. It is presumed that the leftmost symbol on the left hand side of the equation represents 
assignment.

## Website Demo
A demo is currently being hosted very slowly at [__eqsymviz.azurewebsites.net__](http://eqsymviz.azurewebsites.net/).
_Please be patient with the website as it can take up to 3 or 4 minutes to load._

## Local Installation in a Debian based Linux distribution

Clone the project using Git.

Create a virtual environment from within the Equation-Symbol-Visualization folder.  
```bash
<SomePC>$ pip3 install virtualenv (if not installed, use sudo apt install python3-pip)
<SomePC>$ mkdir virtualenv
<SomePC>$ python3 -m virtualenv virtualenv
<SomePC>$ source ./virtualenv/bin/activate
(virtualenv)<SomePC>$ 
```

Use the package manager [__pip__](https://pip.pypa.io/en/stable/) to install dash and numpy.
```bash
(virtualenv)<SomePC>$ pip3 install dash
(virtualenv)<SomePC>$ pip3 install plotly
(virtualenv)<SomePC>$ pip3 install numpy
(virtualenv)<SomePC>$ pip3 install gunicorn
```
Alternatively, one may use the popular method shown below.
```bash
(virtualenv)<SomePC>$ pip3 install -r requirements.txt
```
Run the application.py using python 3.7 or above or use gunicorn.
```bash
(virtualenv)<SomePC>$ gunicorn --workers=2 application:app
```
Note that the '--workers=2' will allow you to run 2 instances of the webpage.

Please note that full compatibility versions is not known at the time, but it was originally written with Python 3.7.

## Usage

Simply navigate from home to the "Equation Symbol Visualization".

Enter equations with one symbol on the left hand side for assignment and one or more symbols on the right hand side

For example, if the following were entered in the text box:  
y = 3\*x+u  
z = 4\*x + 8\*y + 9\*v  
w = z+y^9+v  
v = -y+x  

The following graph data structure as a python dictionary / JSON representation would be produced:  
{'y': \['x', 'u'], 'z': \['x', 'y', 'v'], 'w': \['z', 'y', 'v'], 'v': \['y', 'x']}

Where the visualization would show the following:  
* x and u would point to y
* x, y and v would point to z
* z, y and v would point to w
* y and x would point to v

Also, a visualization of the equations will be produced below the textbox of the equations which uses the dash and
plotly packages.

## Notes

* Symbols such as '9bears' are considered illegal since the first character contains a number. However, the symbol 
'bears9' is perfectly acceptable

* In the current implementation, note that in the event that more than one symbol appears on the left hand side, 
it will be treated as if the leftmost symbol were used for assignment and the other symbol(s) were moved to the 
right hand side. For example:  
   >y = 3\*x+u  
   >x+v = 8\*y + u  
   >z = v + y  
   >
   >Will produce the following graph data structure of symbols:
   >{'y': \['x', 'u'], 'x': \['y', 'u', 'v'], 'z': \['v', 'y']}
   >
   >Since both x and v are found in _x+v_ on the left hand side, x is leftmost symbol, v is moved over to the right 
   >hand side.
   >
   >In this case, the visualization would show the following:  
   >* x and u would point to y
   >* y, u and v would point to x
   >* v and y would point to z

## Future Improvements
Desired improvements would be as follows:
* Support for functions inside equations, such as 'f' in z = x^2 + 6*f(x,y)
* Visual representation for reflexive expressions used in coding statements, like x = x + 1
* More meaningful support for multiple assignments on the left hand side 
* Support for inequality statements, e.g. <=, >=
* A user input to help identify unnecessary variables or unnecessary equations
* Ambitiously, some form of support for LaTeX

## Usefulness
Utilizing the graphical representation of a system of equations can be helpful from the standpoint of identifying
relations between symbols, sub-systems of equations and identifying unnecessary equations.

## Code Snippet Citations
Portions of this code are borrowed from [Jiahui Wang's project](https://github.com/jhwang1992/network-visualization).
Most notably, it borrows from the idea that the visualization of a graph data structure consists of nodes drawn as a 
scatter plot in plotly and the edges of the graph are drawn as lines.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)