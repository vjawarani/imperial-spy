# [imperial-spy](https://www.duneimperiumassets.com/assets/imperium_card/Imperial%20Spy)
I wrote a few AWS Lambda functions so that an HTML tracking embed I inserted into my emails would also track total email opens. The embed then swaps the image to show the number of email opens, implicitly informing both users how frequently the email is observed. It is meant to act as a polite reminder to value privacy.

I have the [total number of opens](https://varunjawarani.com/imperial-spy) on my website.

The embed is similar to a tracking pixel, but is instead replaced with an image that will depict the number of opens inline.

The setup was simple:
- AWS (Lambda, S3, DynamoDB, Route 53)
- anime.js

## HTML Insert
```
<html>
  <body style="font-size:6pt; font-family:Arial, sans-serif;">
    <p>
      We have opened this email <img src="https://api.varunjawarani.com/open?id=<emailUUID>" alt="this many"> times.<br>
      Email is insecure. 
      <a href="https://varunjawarani.com/imperial-spy">Learn more</a>.
    </p>
  </body>
</html>
```
