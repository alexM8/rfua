# What Is This
This is a client for Raiffaisen Bank UA. It was reverse-engineered from iPhone application.
https://online.aval.ua/bfo/channel/web/loginframe.jsp 

# How To Use
1. Create file `credentials.py` with this content:
```python
string = {"Login":"LOGIN_STRING","Password":"PASSWORD_STRING"}
```
2. Launch ```python3``` shell in the project directory and issue
```
import main
```
3. New object ```main.session``` will be created
4. Object initialization creates session with RF UA API and fetches all availible info
5. Data is accessible from these objects:
	- main.session.Info
	- main.session.Cards
	- main.session.Accounts
	- main.session.Holds
	- main.session.History
6. When the object is deleted, destructor method performs logoff

# Other Info
The API interface at ```online.aval.ua``` is very unstable.
That's why every request is performed in a loop with timeout counter.
Counter can be configured in ```config.py```
