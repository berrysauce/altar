<img src="https://berrysauce.dev/altar/assets/img/default.webp" alt="Altar icon" height=64>

# Altar
Altar is a tiny API for the generation of identicons ([Wikipedia](https://en.wikipedia.org/wiki/Identicon)). Altar always generates the same image from the same input through hashing and simple calculations.

This means that you can use Altar to generate profile pictures for users based on their username, or any other unique identifier.

Altar was built from the ground up with few dependencies, but is inspired from GitHub's Identicons and [minidenticons](https://github.com/laurentpayot/minidenticons).

Due to its small size, Altar is very fast. Local Waiting / Local Time To First Byte times are usually between 3-4 ms.

## Installation
- **Locally** – install Altar wherever Python is supported by cloning the repository, installing all dependencies with `pip install -r requirements.txt` and running `main.py`
- **Cloud** – run your own instance of Altar on Vercel. Just click the button below and you'll be guided through the setup.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fberrysauce%2Faltar&project-name=altar&repository-name=altar&demo-title=Altar%20Demo&demo-description=A%20site%20using%20altar%20to%20dynamically%20generate%20identicons.&demo-url=https%3A%2F%2Fberrysauce.me%2Faltar%2F)

### 🔐 Restrict Access
It is possible to restrict the access to your Altar instance. To do that, simply create a `.env` file in the directory where Altar is and add `API_KEY` as a variable. 

If you're hosting Altar on Vercel, go to Settings → Environment Variables and add `API_KEY` there. Choose a key for your Altar instance and set it as the value of the environment variable.

To make authenticated requests to Altar, use the `x-api-key` HTTP header with the `API_KEY` as the value.


## How to use
An API request to Altar only requires the data you want to use to generate the identicon. There are overrides (e.g. for the file size and color) which can be found in the documentation.

```http
GET  https://altar.berrysauce.dev/generate?data=example
```

![Uptime](https://uptime.berrysauce.dev/api/badge/9/uptime)

Altar currently has two public endpoints:
- **Origin:** https://altar.berrysauce.dev
- **🚀 CDN:** https://altarcdn.berrysauce.dev

> [!NOTE]  
> As Altar always generates the same image based on your input, it's recommendet to use the CDN endpoint for better performance.

> [!WARNING]  
> Altar is just a small project, therefore security cannot always be guaranteed. It's only recommended to pass on usernames or unique identifiers to Altar, which do not include or grant access to personal information.

### Headers

| Header        | Type    | Description                                                                            | Required              |
| :-------------|:--------|:---------------------------------------------------------------------------------------| :---------------------|
| `x-api-key`   | String  | API Key for authentication, if it was set as an environment variable.                  | no (if set, yes  ⚠️)      |

### Query Parameters

| Query         | Type    | Description                                                                            | Required |
| :-------------|:--------|:---------------------------------------------------------------------------------------| :--------|
| `data`        | String  | Data to be used for identicon generation                                               | yes ⚠️    |
| `color`       | String  | HEX Color to be used for the identicon foreground without '#' (default: generated based on input) | no       |
| `background`  | String  | HEX Color to be used for the identicon background without '#' prefix (default: none/transparent)  | no       |
| `size`        | Integer | Width & Height of the scaled SVG (default: 250)                                        | no       |
| `padding`     | Integer | Padding for the identicon (default: 0)                                                 | no       |

## Development
1. Install Altar wherever Python is supported by cloning the repository
2. Install all dependencies with `pip install -r requirements.txt`
3. Run `main.py` with `python main.py`

> [!NOTE]
> Altar is built with Python 3.9.x, but should work with any Python version above 3.6

## License
Altar is licensed under the MIT license.

Copyright (c) 2023 Paul Haedrich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
