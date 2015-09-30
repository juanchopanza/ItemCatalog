# A few notes about this project

## Known improvements

Some of the code that has been written by hand for educational purposes could be removed
by using 3rd party libraries. For example:

* Form handling with [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/). This has
its own CSRF handling for forms.

* CSRF with e.g. [Flask-SeaSurf](https://flask-seasurf.readthedocs.org/en/latest/). I
have implemented my own code to handle CSRF in a way that seems adequate, but it still
has some security holes (tokens can be passed as request arguments and intercepted,
or as hidden form fileds, in which case they can be seen in the source. However, tokens
are generated after each request, which mitigates these vulnerabilities. Still, better
trust the experts in real code.)

Some code can be improved:

* Refactor Oauth2 authentication/authorization code. Some re-factoring has been
performed, but there still is some duplication. This is probably the ugliest part
of the code-base. Again, in real code I'd explore 3rd party solutions. 

* Re-factor JSON/ATOM end-point view code. There is duplication.

## Known issues

* Facebook login results in a warning about screen sizes and pop-ups.
Apparently this would not happen in production, but it is annoying nonetheless.

* Secrets in public repo. In order to make the app easily testable and usable by 3rd
parties, the client secrets are stored in this public repository. That isn't ideal
from a security point of view. If and when this app gets put online new secrets will
have to be generated and stored elsewhere.

## Notes on Functionality

Although many of the "exceeds expectations" criteria are related to CRUD with images,
I have not implemented that. I do not feel it is different enough from the already
implemented CRUD operations. I have concentrated instead on making the app
self-consistent, secure and well behaved, on implementing CSRF and JSON and XML
end-points, and on allowing sign-in with more than one 3rd party Oauth privider. 
I can easily add images if deemed necessary, but I would prefer adding the
following first:

* Category description
* Creation timestamps for categories and items
* Edit category
* User pages.
* More 3rd party oauth providers (github, twitter, amazon...)
