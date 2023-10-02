# Webserver config

There are two ways to host this app:

- `nginx-split-path.conf`: backend and frontend are served at different URLs
- `nginx-same-path.conf`: backend and frontend use the same base URL

Both examples use `/srv/http/my-domain/` as the base folder, make sure it exists.
The server will create files at these locations:


```sh
/srv/http/my-domain/  # base folder, make sure it exists
/srv/http/my-domain/backend_data/  # holds the encrypted json files
/srv/http/my-domain/backend_static/  # holds static js files (mostly django admin)
/srv/http/my-domain/frontend/  # place your frontend html here (e.g. content of example-html)
/srv/http/my-domain/root/  # root-level files ("/") (only split-path)
```


## Split path

Since both parts are served separately, you can host the server on two different machines (or two different subpaths). The frontend is a purely static server. You can use a CDN if you want.

If you serve the backend on a subpath (not root "/"), you need to pass that subpath to the env file. E.g., `URL_SUBPATH=my/sub/path`.

If you use two different servers, you have to transfer the encryted json files to the frontend server somehow (e.g., with rsync or a tiny REST API). Or use the integrated API `api/json/<org>/<uuid>` (disabled by default). Though the other way (pushing data from backend to frontend) is more favorable. That way you will not expose the backend server to the public.


## Same path

With this config, both – frontend and backend – are served from the root of the domain ("/"). You can still serve them from two different servers, but its easy to guess the url and discover the other server.

If you use two different servers, you will need to declare the exception explicitly (namely, `edit`, `upload`, `static`, and `api`). If the backend URLs change, you will need to update the config too. But in the given example, nginx will fallback to the backend server whever a file cannot be found.

**Note:** you can not have files in your frontend which are named like any of the backend URLs. For example, if you create a static `upload` or `edit` folder in your frontend code, it would probably break the administration backend (precedence).


## Comparison

Assuming we configured the split-path config to use `frontend="card"` and `backend="hidden-service"` the URLs would be:


|        | Split path                   | Same path     |
|--------|------------------------------|---------------|
|Frontend| /card/#org/id/pw             | /#org/id/pw   |
|Backend | /hidden-service/edit/        | /edit/        |
|Static  | /hidden-service/static/      | /static/      |
|Data    | /card/data/org/id            | /data/org/id/ |
|API     | /hidden-service/api/json/... | /api/json/... |
|Root    | /other-service/              | –             |


## Security considerations

A dynamic server (like Django) is always a security risk. You should limit public access wherever possible. For example:

- If you are the only person managing member cards, you can run the backend in a local-only environment and just sync the changes with rsync to a static frontend server.

- If you run the backend as a public server, you can try to limit the access. For example, by allowing only known IP Adresses (again, only if there are few people managing the cards and/or the connection location is fixed, e.g., business network).

- If your backend is public, at least do not use common URL paths. For example, `/admin/` is easy to guess and most crawlers will try these locations.

- Both configs allow you to run the backend and frontend on separate servers. This separates the sensitive data (Django app with unencrypted raw data) from the publicly accessible data (encrypted json).

- If you need to communicate between both servers, try to push the data from backend to frontend instead of the other way around. This way your frontend stays static and an attacker will not discover the backend server just by analyzing the web traffic. (attention: you may still expose it through Certificate Transparency Logs)

- Needless to say, communication between servers must be authenticated. Or else someone can just create new member cards arbitrarily.
