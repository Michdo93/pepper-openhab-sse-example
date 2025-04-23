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

Sure! Here's a clear and structured explanation in **Markdown** that describes how the HTML page and the Python script work together using **NAOqi**, **openHAB**, and **ALMemory** to create a real-time smart lighting control interface on a Pepper robot’s tablet:

---

# 🧠 How NAOqi, HTML, and Python Work Together to Control an openHAB Switch Item

This system consists of two main parts:

1. A **Python backend** running on the robot, communicating with openHAB.
2. An **HTML-based user interface** shown on the Pepper tablet, allowing users to control lights and see status changes.

---

## 📱 HTML Page (Tablet UI)

### Purpose:
- Acts as the **frontend interface** for the user.
- Provides a **button** to toggle light state (ON/OFF).
- Dynamically updates the button label based on the light’s current state.

### Key Concepts:
- Uses `qimessaging.js` to communicate with **Pepper's ALMemory**.
- Fetches the current light state from `ALMemory`.
- Subscribes to real-time updates via `lampStatusChanged` event.
- Sends commands to openHAB using `fetch()` and a REST API.

### Workflow:
```plaintext
[User taps Button] → [fetch() sends POST to openHAB] → [openHAB switches light]
                                            ↓
                         [Python backend receives light state change via SSE]
                                            ↓
                      [Backend updates ALMemory, triggers lampStatusChanged]
                                            ↓
                   [HTML receives event via subscriber.signal → updates Button]
```

---

## 🐍 Python Program (Robot Backend)

### Purpose:
- Acts as a **middleware** between the Pepper robot and openHAB.
- Listens for state updates from openHAB (via SSE).
- Updates `ALMemory` with the latest light status.
- Shows the HTML UI on the Pepper tablet.

### Important Functions:

#### `getState()`
- Queries openHAB REST API for the current light state.
- Stores it in `ALMemory` under the key `"lampStatus"`.

#### `ItemStateEvent()`
- Uses **Server-Sent Events (SSE)** to subscribe to changes of a specific item.
- When openHAB emits a change (e.g. lamp turns ON/OFF), it:
  - Extracts the new state from the payload.
  - Updates `ALMemory` using `memory.insertData("lampStatus", state)`
  - Triggers `lampStatusChanged` using `memory.raiseEvent(...)` for real-time updates.

#### `main()`
- Connects to NAOqi via `qi.Session()`.
- Retrieves `ALMemory` and `ALTabletService`.
- Sets initial light state using `getState()`.
- Starts SSE event thread using `ItemStateEvent()`.
- Displays the HTML interface on the tablet using:
  ```python
  tabletService.showWebview("http://198.18.0.1/apps/openhab_ui/index.html")
  ```

---

## 🔁 Real-Time Sync with ALMemory

| Component | Method | Description |
|----------|--------|-------------|
| **Python** | `memory.insertData("lampStatus", state)` | Writes the new state into ALMemory |
| **Python** | `memory.raiseEvent("lampStatusChanged", state)` | Triggers an event that notifies subscribers |
| **HTML** | `memory.getData(...)` | Reads the current state on load |
| **HTML** | `memory.subscriber(...).signal.connect(...)` | Listens to state changes via `lampStatusChanged` |

This allows the UI to **immediately reflect any changes** to the light's state, whether triggered via the UI itself or externally (e.g. openHAB automations).

---

## 🧠 NAOqi Services Used

### `ALMemory`
- A key-value store with pub/sub capability.
- Used to **share light status** between the backend and frontend.
- Enables **event-driven communication** (via `.raiseEvent()` and `.subscriber()`).

### `ALTabletService`
- Displays the HTML interface on Pepper's tablet.
- Method used:
  ```python
  tabletService.showWebview("http://198.18.0.1/apps/openhab_ui/index.html")
  ```

---

## ✅ Summary

| Element | Role |
|--------|------|
| **HTML Page** | User interface for controlling lights |
| **JavaScript (qimessaging.js)** | Binds UI to Pepper’s internal memory (ALMemory) |
| **Python Script** | Middleware: REST + SSE handling, updates ALMemory |
| **openHAB** | Home automation backend (REST + events) |
| **ALMemory** | Real-time data layer (light status + events) |
| **ALTabletService** | Displays HTML page on the Pepper tablet |

---

