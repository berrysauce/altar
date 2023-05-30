<img src="https://raw.githubusercontent.com/berrysauce/altar/master/templates/assets/img/altar-identicons.svg" alt="altar spelled in identicons" height=64>

# altar

Altar is a tiny API for the generation of identicons (Wikipedia). Altar always generates the same image from the same input through hashing and simple calculations.

This means that you can use Altar to generate profile pictures for users based on their username, or any other unique identifier.

Altar was built from the ground up with few dependencies, but is inspired from GitHub's Identicons and minidenticons.

## How to use
An API request to Altar only requires the data you want to use to generate the identicon. There are overrides (e.g. for the file size and color) which can be found in the documentation.

```http
GET  https://altar.berrysauce.me/generate?data=example
```

> **Warning**: Altar is just a small project, therefore security cannot always be guaranteed. We recommend to only pass on usernames or unique identifiers to Altar, which do not include or grant access to personal information.
