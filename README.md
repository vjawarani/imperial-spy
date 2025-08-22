# imperial-spy
I wrote a few AWS Lambda functions so that an HTML tracking embed I inserted into my emails would also track total email opens. The embed then swaps the image to show the number of email opens, clarifying to the recipients that I was aware of both their frenetic email-opening and their avoidant lack of response. It was meant to elicit a fear response in its purpose of privacy advocacy, alerting the recipient to just how much data they are giving away.

I have the [total number of opens](https://varunjawarani.com/imperial-spy) on my website.

The embed is similar to a tracking pixel, but is instead replaced with an image that will depict the number of opens inline. The image is one of 52: the numbers 0-50 stored in an S3 bucket, and one image that simply says '50plus'.

## Tools Used:
- AWS Lambda
- AWS S3
- AWS DynamoDB
- AWS Route53
- anime.js

## HTML Insert
```
<html>
  <body style="font-size:6pt; font-family:Arial, sans-serif;">
    <p>
      You have opened this email <img src="https://api.varunjawarani.com/open?id=<emailUUID>" alt="numEmailOpens"> times:<br>
    </p>
    <p>
      Email is insecure. 
      <a href="https://varunjawarani.com/imperial-spy">Learn more</a>.
    </p>
  </body>
</html>
```
