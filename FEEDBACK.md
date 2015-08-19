Feedback
==============================
This API provides an excellent developer platform; the sky's the limit in terms of its use cases. However, there was a bug in the sample application that the API tutorial provided (it might confuse future developers trying to use the Uber API). According to the Uber API documentation, the scopes parameter passed in during the authorization call should be a "Space delimited list" called `scope`. However, the sample application had it as a comma-separated list called "scopes." I tried creating a pull request to fix this, but I don't have permissions. The line at https://github.com/uber/Python-Sample-Application/blob/master/app.py#L57 should read:

```python
'scope': ' '.join(config.get('scopes'))
```

Also, small detail, but the sample app's README mentions the `profile` and `history` scopes in step 2, but its config.json's scopes value has `history_lite` instead of `history`.

These developer tools/features would facilitate debugging/testing:

1) Having a log of most recent (maybe 10 or so) API requests made and responses received may be helpful. 

2) A way to clear just the browser cache entries/cookies associated with Uber's oAuth process. That way, when developers want to test the OAuth flow of their apps again, they don't need to clear all of their cache and cookies (including ones for other sites they might want to keep).

3) A list of common errors and how to fix them in the API tutorial.