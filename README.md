# flask-auth
This is a reusable JWT-based authentication template for Flask to quickly bootstrap auth-backed apps. To use, clone into your repo, and register the auth blueprint. You can initialize the db as shown, and modify it to use another database system of your choice. Then, `login`, `logout` and `register` handlers will begin to work on `/auth/` endpoints. 

To add more parameters to the User model, just add them to the model and pass it in as keyword arguments to `create_user` inside the registration handler. Finally, you can use the `@login_required` event handler to automatically authenticate, redirect and pass in the user object as a function argument.
