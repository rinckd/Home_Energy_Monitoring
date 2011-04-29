<%
# I use this mako template when I want to quickly dump values to screen
# Simply use the test function in views.py and write your values out to the variable 'logging'
# then go to url /tests

context.write(logging) 
%>

header("Content-Type: text/plain"); 