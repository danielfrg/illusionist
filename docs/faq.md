# F.A.Q

## How it compares to Voila / Dash / Shiny

Voila, Dash and Shiny are great tools thats allow users to create dashboards based
on Python and R code, they are served by and connected to a running Python or R process,
this allows for birectional communication between the frontend and the backend
and results in very dynamic dashboards.

This is great if you data changes constanty, are connecting to external data
sources or APIs, or have complex logic in your dashboards.
The annoying part comes when you try to deploy any built assets because it requires
to have a running Python or R process.
There are tons of solutions out there to make this process easier but the requirements
of a handling Python/R dependencies and a running process are always there
everytime you want to update or deploy an app.

We believe most dashboard and reports do not need a live Python or R process.
Most reports only need to be updated when the underlying data is updated.
Most of those are only going to be generated once!

Some of those reports could use some interactivity based on Widgets
that make that the user experience better. That's where illusionist comes in.
