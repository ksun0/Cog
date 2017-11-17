# Cog Extensions

## Flow process
A cog extension is made by a flow of steps. There may either be one or multiple steps. Each step is comprised of an input from the previous step to an out to the user. On the first step, there is no input.

## Inputs
Each step in an extension's flow has an argument 'data'. Data will always contain 4 fields: uuid, step, data, and request. 

## Outputs
In the majority of cases, the output will be a rendered template. In most cases, it is just a django form.

## Redirects
If you'd like to redirect to external authentication, use JSONResponse. There should be one key, 'redirect', and one value, the url to redirect to. If the url redirected to will redirect back to a url, use GET data in the url to redirect back to the correct place.

## Creating new extension
Create a subdirectory in the Extensions folder. 
Inside there, the only necessary file is a views.py file.
Inside the views.py file, there are three required fields: steps, name, description.
Steps is an ordered list of functions that make up the flow.
Once completed, run `python manage.py migrate_extensions` to migrate extensions.