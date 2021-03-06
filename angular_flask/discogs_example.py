#!/usr/bin/env python
#
# This illustrates the call-flow required to complete an OAuth request
# against the discogs.com API. The script will download and save a single
# image from the discogs.com API as an example.
# See README.md for further documentation.
#
import json
import sys
import urlparse

import oauth2 as oauth

def get_posts():
    # Your consumer key and consumer secret generated by discogs when an application is created
    # and registered . See http://www.discogs.com/settings/developers . These credentials
    # are assigned by application and remain static for the lifetime of your discogs application.
    # the consumer details below were generated for the 'discogs-oauth-example' application.
    consumer_key = 'kYhodEsayfOCaQWktqBk'
    consumer_secret = 'pBCJIcEZBuAAOoeGBsqARDbPOXNJQriI'

    # The following oauth end-points are defined by discogs.com staff. These static endpoints
    # are called at various stages of oauth handshaking.
    request_token_url = 'https://api.discogs.com/oauth/request_token'
    authorize_url = 'https://www.discogs.com/oauth/authorize'
    access_token_url = 'https://api.discogs.com/oauth/access_token'

    # A user-agent is required with Discogs API requests. Be sure to make your user-agent
    # unique, or you may get a bad response.
    user_agent = 'discogs_api_example/1.0'

    # create oauth Consumer and Client objects using
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    # We're now able to fetch an image using the application consumer key and secret,
    # along with the verified oauth token and oauth token for this user.
    token = oauth.Token(key="qvFKFRtvofaBBvCtSWndFFggppAHSpIhqriKQUnN",
            secret="xznhBQqTvIHsgLeYDnjRNHfYPUmLETUHpmuPocja")
    client = oauth.Client(consumer, token)
    resp, content = client.request('https://api.discogs.com/images/R-40522-1098545214.jpg',
            headers={'User-Agent': user_agent})

    print ' == Authenticated API image request =='
    print '    * response status      = {0}'.format(resp['status'])
    print '    * saving image to disk = R-40522-1098545214.jpg'

    with open('R-40522-1098545214.jpg', 'w') as fh:
        fh.write(content)

    # With an active auth token, we're able to reuse the client object and request
    # additional discogs authenticated endpoints, such as database search.
    resp, content = client.request('https://api.discogs.com/database/search?release_title=House+For+All&artist=Blunted+Dummies',
            headers={'User-Agent': user_agent})

    if resp['status'] != '200':
        sys.exit('Invalid API response {0}.'.format(resp['status']))

    releases = json.loads(content)
    print '\n== Search results for release_title=House For All, Artist=Blunted Dummies =='
    posts = [{ "post": []}]
    for release in releases['results']:
        body = """
        \n\t== discogs-id {id} == \n
        \tTitle\t: {title}\n
        \tYear\t: {year}\n
        \tLabels\t: {label}\n
        \tCat No\t: {catno}\n
                     """.format(id=release['id'], title=release.get('title', 'Unknown'),
                                year=release.get('year', 'Unknown'),
                                label=', '.join(release.get('label', ['Unknown'])),
                                catno=release.get('catno', 'Unknown'))
        artist = {"body": body, "title": release.get('title', 'Unknown')}
        posts[0]['post'].append(artist)

    print posts
    return posts, resp['status']
