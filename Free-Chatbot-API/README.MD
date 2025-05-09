# Free Chatbot API

This project implements a Python web API that offers free access to three leading AI chatbots **ChatGPT**, **Google Bard**, and **Claude** through a single interface.

**Key features:**

-   Unified API endpoints allow seamlessly querying ChatGPT, Google Bard, and Claude from one integration.
-   Leverages the free web/browser versions of each AI service by managing cookies and sessions. Avoid costs of paid API access.
-   Simple API for text completion, question answering, and conversational queries. Integrate AI capabilities easily.
-   Lightweight Python server using FastAPI. Easily self-host locally or on your own infrastructure.
-   Full support for streaming responses.

<br>

-   ✅ **_Google Bard_** integration available now.
-   ✅ **_Claude-2_** integration is also fully implemented and available.
-   ✅ **_ChatGPT_** integration is fully complete and available now.

<br>

[![Image](assets/Endpoints-Docs-Thumb.png)](assets/Endpoints-Docs.png)

<br><br>

**NOTE:** This is a personal project involving the use of tools such as [ShellGPT](https://github.com/TheR1D/shell_gpt) , [ChatGPT Code Review](https://github.com/Amm1rr/ChatGPT-Code-Review) and...<br>
Please use them responsibly.

This repository is up-to-date.

<br>


### Prerequisites

Python version >= 3.10

Before using the APIs, sign up for free accounts to get access credentials if you don't already have them:

-   ChatGPT: https://openai.com/api/
-   Google Bard: https://bard.google.com/
-   Claude: https://claude.ai/

Then, add your token(s) to the [**`Config.conf`**](#configuration) file. (see [**Configuration**](#configuration) section).

**Note**: [**Claude**](https://claude.ai/) and [**Bard**](https://bard.google.com/) offer two authentication options - you can either log in through your browser and skip this step.
<br>

## Installation

<br>

### Step 1. Clone Repository

```bash
git clone https://github.com/Amm1rr/Free-Chatbot-API.git && cd Free-Chatbot-API

python -m venv .venv

source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows


pip install -r requirements.txt
```

<br>

### Step 2. Start Web Server

Navigate into the **`src`** directory, and run the web server:

```bash
cd src/

python main.py

```

<br>

Available **Endpoints:**

```bash
#---------- Google Bard

http://128.0.0.1:8000/bard


#---------- Claude

http://128.0.0.1:8000/claude


#---------- ChatGPT

http://128.0.0.1:8000/chatgpt


#---------- OpenAI ChatGPT JSON Response

http://128.0.0.1:8000/v1/chat/completions


```

<br><br>

**Input / Output**

```bash
# Input:
_____

    {
      "session_id": "session-ID",
      "message": "Hi, Who are you?",
      "stream": True
    }


--------------------


# Output:
_____

    {
      I am a Chatbot assistant :)
    }


--------------------


# OpenAI Response Output:
_____

# Streaming
  {
    "id": "chatcmpl-123",
    "object": "chat.completion.chunk",
    "created": 1677652288,
    "model": "gpt-3.5-turbo",
    "choices": [{
      "index": 0,
      "delta": {
        "content": "Hello",
      },
      "finish_reason": "stop"
    }]
  }


# Not Streaming
  {
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo",
    "choices": [{
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "\n\nHello there, how may I assist you today?",
      },
      "finish_reason": "stop"
    }]
  }



```

<br>

## Example

try **Claude** with **cURL**

Once you have launched the webserver using **[`src\python main.py`](#step-2-start-web-server)** , run this cURL command in a terminal window:

```bash
curl -X 'POST' \
  'http://localhost:8000/claude' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "who are you?",
  "session_id": "",
  "stream": true
}'

```

**Note**: The **`session_id`** is configured in the [**Config.conf**](#configuration) file. If you send this variable empty, it will use the [Config.conf](#configuration)

<br><br>

## Usage

#### How to Find Your Tokens

**Note**: [**Claude**](https://claude.ai/) and [**Bard**](https://bard.google.com/) offer two authentication options - you can either log in through your browser and skip this step, or you can follow the instructions below to configure the authentication.

<br>

First you need to add your tokens to the [**`Config.conf`**](#configuration) file (see [**Configuration**](#configuration) section).

<br>

<details>

  <summary>

**Google Bard**

  </summary>

[![Image](assets/Bard-Thumb.jpg)](assets/Bard.jpg)

_`Google Bard:`_ Please obtain the cookies mentioned here from an authorized session on bard.google.com. The cookies can be used to
send POST requests to the /bard endpoint along with a message in a JSON payload. It is important that the **session_id**,
which is your **Secure-1PSID** cookie, is included in the request. ([Screenshot](assets/Bard.jpg))

1. Login to [bard.google.com](https://bard.google.com)
2. Open `Developer Tools` (Press **F12**)
3. Go to `Application Tab`
4. Go to `Cookies Tab`
5. Copy the content of `__Secure-1PSID` and `__Secure-1PSIDTS`. Copy the value of those cookie.
6. Set in **[Config.conf](#configuration)** file.
 </details>
 <br><hr><br>

<details>

  <summary>

**Claude 2**

  </summary>

[![Image](assets/Claude-Thumb.jpg)](assets/Claude.jpg)

**Method 1:** <br>
For Claude, all you need to do is [login](https://claude.ai/) to your account using your web browser. (Firefox, Chrome, Safari)

**Method 2:** <br>
_`Claude:`_ You can get cookie from the browser's developer tools network tab ( see for any [claude.ai](https://claude.ai/) requests check out cookie ,copy whole value ) or storage tab ( You can find cookie of claude.ai ,there will be four values ) ([Screenshot](assets/Claude.jpg))

1. Login to [claude.ai](https://claude.ai/)
2. Open `Developer Tools` (Press **F12**)
3. Go to `Network Tab`
4. Select an ajax request (like step 3 in [picture](assets/Claude.jpg))
5. Copy the content of `Cookie`
6. Set in **[Config.conf](#configuration)** file.

</details>

<br><hr><br>

<details>

  <summary>

**ChatGPT**

  </summary>

[![Image](assets/ChatGPT-Thumb.jpg)](assets/ChatGPT.jpg)

_`ChatGPT:`_ Please obtain the sessions mentioned here from an authorized session on chat.openai.com. The sessions can be used to
send POST requests to the /chatgpt endpoint along with a message in a JSON payload. It is important that the session_id,
which is your `Authorization` header session, is included in the request. ([Screenshot](assets/ChatGPT.jpg))

1. Login to [chat.openai.com](https://chat.openai.com)
2. at least ask any question.
3. Open `Developer Tools` (Press **F12**)
4. Go to `Network Tab`
5. Select an ajax request (like step 4 in [picture](assets/ChatGPT.jpg))
6. Copy the content of `Authorization`
7. Set in [**Config.conf**](#configuration) file.

</details>

<br><hr>

## Configuration

[How to Find Your Tokens](#usage)

**Note**: Claude and Bard presents two authentication options - logging in through your browser or configuring Claude using the provided config file.

#### Config File Path:

-   Free-Chatbot-API\src\Config.conf

```bash
# Case-Sensative

[Claude]
COOKIE=[YOURS]

[Bard]
SESSION_ID=[YOURS]
SESSION_IDTS=[YOURS]

[ChatGPT]
ACCESS_TOKEN=[YOURS]


```

<br>

## Sources

[Google Bard API](https://github.com/ra83205/google-bard-api) | [Claude API](https://github.com/KoushikNavuluri/Claude-API) | [revChatGPT](https://github.com/acheong08/ChatGPT/)

<br>

## Licensing

This project is licensed under the MIT License. Feel free to use it however you like.

<br>

[![](https://visitcount.itsvg.in/api?id=amm1rr&label=V&color=0&icon=2&pretty=true)](https://github.com/Amm1rr/)
