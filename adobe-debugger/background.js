
var debug = true;

chrome.browserAction.onClicked.addListener(
    function(tab) {

        debug = !debug;

        chrome.browserAction.setTitle({
            title: debug ? 'Adobe Analytics debugger is ON' : 'Adobe Analytics debugger is OFF'
        });

        chrome.browserAction.setIcon({
            path: debug ? 'icon.png' : 'icon-off.png'
        });

        //chrome.tabs.update(tab.id, {url: tab.url, selected: tab.selected}, null);
        //chrome.webRequest.handlerBehaviorChanged();

    }
);


chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
        if (debug) {
            chrome.tabs.query({active: true, currentWindow: true},function(tabs) {
                if(details.method == 'POST' && details.requestBody && details.requestBody.raw) {
                    details.post_query = '';
                    for(var i=0; i<details.requestBody.raw.length; i++){
                        details.post_query += String.fromCharCode.apply(null, new Uint8Array(details.requestBody.raw[i].bytes));
                    }
            	}
                chrome.tabs.sendMessage(details.tabId, details);
            });
        }
    },
    { urls: ["*://*/b/ss/*"] }, ['requestBody', 'blocking']
);
