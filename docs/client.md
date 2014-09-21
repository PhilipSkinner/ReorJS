ReorJS Node Clients
=============================

The ReorJS package comes with two Node clients. One is powered by node.js and the other is for embedding into websites.

Node.js
-------

The node.js package comes with all of the required node.js libraries to run without installing any requirements. The only requirement is having node installed on the host machine.

To run the node client, simply run:

node reor-node.js

The node client will attempt to discover the ReorJSd service on your local network.

Further configuration for the node.js client is not yet standardised, but can be achieved by modifying the reor-node.js script to scan a different IP range etc.

Browser
-------

The browser client includes the javascript file to be included on your website, plus an optional HTML document incase you want to secure your script through running it in an IFRAME.

There is more information about configuration of the browser plugin to be found in the HOWTO document located in the browser client directory.
