# pepper-openhab-sse-example
A simple example of how to implement the Pepper so that a button on the tablet binds to the status of an openHAB item. Among other things, the openHAB REST API is accessed via SSE for this purpose. Since the Pepper can use outdated JavaScript, a combination of Python and JavaScript must be used as a workaround.

# Installation

```
git clone https://github.com/Michdo93/pepper-openhab-sse-example
cd pepper-openhab-sse-example
mkdir -p /home/nao/.local/share/PackageManager/apps/openhab_ui
cp -r html/ /home/nao/.local/share/PackageManager/apps/openhab_ui
```

---

# Customization

## Python

Please edit the `openhab_sse.py`:

```
nano openhab_sse.py
```

Replace the `baseURL` with the url of your openHAB instance, for example:

```
baseURL = "http://192.168.0.5:8080"
```

You also have to replace the `itemName` with a openHAB `switch` item you want to controll:

```
itemName = "<itemName>"
```

At least you have to replace your `username` and `password` for your openHAB user, so you can request the openHAB REST API:

```
auth = requests.auth.HTTPBasicAuth("<username>", "<password>")
```

In this example, `Basic Authentication` is used. If you want to use token-based authentication, you must change the program code at this point.

## HTML

Please edit the `index.html`:

```
nano /home/nao/.local/share/PackageManager/apps/openhab_ui/html/index.html
```

There you have to adjust `BASE_URL` and `ITEM_NAME` accordingly:

```
    const BASE_URL = "http://192.168.0.5:8080";
    const ITEM_NAME = "iSmartHome_Hue_Lampen_Schalter";
```

---



````
